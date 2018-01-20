"""
Subcontroller module for Alien Invaders

This module contains the subcontroller to manage a single level or wave in the Alien
Invaders game.  Instances of Wave represent a single wave.  Whenever you move to a
new level, you are expected to make a new instance of the class.

The subcontroller Wave manages the ship, the aliens and any laser bolts on screen.  
These are model objects.  Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or models.py.
Whether a helper method belongs in this module or models.py is often a complicated
issue.  If you do not know, ask on Piazza and we will answer.

Debasmita Bhattacharya (db758) and Amelia Myers (arm293)
2 December 2017
"""
from game2d import *
from consts import *
from models import *
import random

# PRIMARY RULE: Wave can only access attributes in models.py via getters/setters
# Wave is NOT allowed to access anything in app.py (Subcontrollers are not permitted 
# to access anything in their parent. To see why, take CS 3152)


class Wave(object):
    """
    We discussed how to choose the correct alien image with Anishka Singh.
    
    This class controls a single level or wave of Alien Invaders.
    
    This subcontroller has a reference to the ship, aliens, and any laser bolts on screen. 
    It animates the laser bolts, removing any aliens as necessary. It also marches the
    aliens back and forth across the screen until they are all destroyed or they reach
    the defense line (at which point the player loses). When the wave is complete, you 
    should create a NEW instance of Wave (in Invaders) if you want to make a new wave of 
    aliens.
    
    If you want to pause the game, tell this controller to draw, but do not update.  See 
    subcontrollers.py from Lecture 24 for an example.  This class will be similar to
    than one in how it interacts with the main class Invaders.
    
    #UPDATE ME LATER
    INSTANCE ATTRIBUTES:
        _ship:   the player ship to control [Ship]
        _aliens: the 2d list of aliens in the wave [rectangular 2d list of Alien or None] 
        _bolts:  the laser bolts currently on screen [list of Bolt, possibly empty]
        _dline:  the defensive line being protected [GPath]
        _lives:  the number of lives left  [int >= 0]
        _time:   The amount of time since the last Alien "step" [number >= 0]

    
    As you can see, all of these attributes are hidden.  You may find that you want to
    access an attribute in class Invaders. It is okay if you do, but you MAY NOT ACCESS 
    THE ATTRIBUTES DIRECTLY. You must use a getter and/or setter for any attribute that 
    you need to access in Invaders.  Only add the getters and setters that you need for 
    Invaders. You can keep everything else hidden.
    
    You may change any of the attributes above as you see fit. For example, may want to 
    keep track of the score.  You also might want some label objects to display the score
    and number of lives. If you make changes, please list the changes with the invariants.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
        _direction: the direction that the aliens are moving in [right, down, left]
        _alienfire: The number of steps until the aliens fire
        _score: the current game score
    
    """
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    
    # INITIALIZER (standard form) TO CREATE SHIP AND ALIENS
    def __init__(self):
        """ Initializer to create ship and aliens.
        This method initializes the ship and alien wave in the game by constructing them.
        """
        acc1 = []
        for row in range(ALIEN_ROWS):
            acc2 = []
            for alien in range(ALIENS_IN_ROW):
                if alien != None:
                    y = GAME_HEIGHT - ALIEN_CEILING - 0.5*ALIEN_HEIGHT - (ALIEN_ROWS -1)*ALIEN_V_SEP - (ALIEN_ROWS -1)*ALIEN_HEIGHT
                    vert = ALIEN_V_SEP + ALIEN_HEIGHT
                    if row%6 == 0 or row%6 ==1:
                        source = ALIEN_IMAGES[0]
                    elif row%6 == 2 or row%6 ==3:
                        source = ALIEN_IMAGES[1]
                    elif row%6 == 4 or row%6 ==5:
                        source = ALIEN_IMAGES[2]
                    acc2.append(Alien((alien+1)*ALIEN_WIDTH + alien*ALIEN_H_SEP, y +row*vert, ALIEN_WIDTH, ALIEN_HEIGHT, source))
            acc1.append(acc2)
        self._aliens = acc1
        self._ship = Ship(x=GAME_WIDTH/2, bottom = SHIP_BOTTOM, width=SHIP_WIDTH, height=SHIP_HEIGHT, source='ship.png')
        self._dline = GPath(points=[0, DEFENSE_LINE, GAME_WIDTH, DEFENSE_LINE], linewidth = 1, linecolor = cornell.WHITE)
        self._direction = 'right'
        self._time = 0
        self._bolts = []
        self._alienfire = random.randint(1, BOLT_RATE)
        self._lives = 3
        self._score = 0
        
        
    # UPDATE METHOD TO MOVE THE SHIP, ALIENS, AND LASER BOLTS
            
    def update(self, input, dt):
        """ Moves the ship, aliens, and laser bolts
        
        This procedure makes use of helper functions that move the ship, aliens, and laser bolts from both the ship and the aliens
        
        Parameter dt: time in seconds since the last call to the update method
        Precondition: dt is a number"""
        
        self.ship_movement(input)
        self.alien_wave(dt)
        self.fireBolt(input)
        self.alien_bolt(dt)
        if self._ship != None:
            for bolt in self._bolts:    
                if self._ship.ship_collides(self._bolts[0]) == True:
                    self._ship = None
                    self._lives -= 1
                    del self._bolts[0]           
        if self._aliens != None:
            for row in range(len(self._aliens)):
                for alien in range(len(self._aliens[row])):
                    for bolt in self._bolts:
                        if self._aliens[row][alien] != None: 
                            if self._aliens[row][alien].alien_collides(bolt) == True:
                                self._aliens[row][alien] = None
                                pos = self._bolts.index(bolt)
                                del self._bolts[pos]
                                self._score += 10
        
    
    # DRAW METHOD TO DRAW THE SHIP, ALIENS, DEFENSIVE LINE AND BOLTS
    def draw_aliens(self, view):
        """ Draws the alien wave on the screen
        
        This procedure draws each alien in the wave on the screen""" 
        for row in self._aliens:
            for alien in row:
                if alien != None:
                    alien.draw(view)
    
    def draw_ship(self, view):
        """ Draws the ship on the screen
        
        This procedure draws the player's ship on the screen""" 
        if self._ship != None:
            self._ship.draw(view)
        
    def draw_dline(self,view):
        """ Draws the defense line on the screen
        
        This procedure draws the defense line on the screen""" 
        self._dline.draw(view)
        
    def draw_bolt(self, view):
        """ Draws a bolt on the screen
        
        This procedure draws a bolt on the screen""" 
        for x in self._bolts: 
            x.draw(view)
        
    # HELPER METHODS FOR COLLISION DETECTION
    
    def fireBolt(self, input):
        """
        We discussed how to implement this method with Lawrence Li
        
        Fires a bolt from the ship
        
        This procedure fires a bolt from the player's ship after the spacebar key is pressed.
        We extended this section by adding a sound every time the player shoots a bolt""" 
        list = []
        for x in self._bolts:
            list.append(x.isPlayerBolt())
        if True not in list:
            if input.is_key_down('spacebar'):
                if self._ship != None:
                    self._bolts.append(Bolt(x=self._ship.x, bottom = SHIP_BOTTOM + SHIP_HEIGHT,
                                        width = 5, height = 20, linecolor= cornell.BLUE,
                                        fillcolor = cornell.BLUE, velocity = BOLT_SPEED))
                    pewSound = Sound('pew2.wav')
                    pewSound.play()
        self.move_bolt()
                
    def move_bolt(self):
        """ Moves the bolt.
        This helper method to fireBolt moves the bolt image a certain distance when called.
        Parameter velocity: the distance to move the bolt
        Precondition: velocity is a number"""
        for x in self._bolts:
            if x.GetBoltVelocity() >0:
                x.SetBoltY(BOLT_SPEED)
            if x.GetBoltVelocity() <0:
                x.SetBoltY(-BOLT_SPEED)
            if x.GetBoltY() > GAME_HEIGHT + BOLT_HEIGHT/2 or x.GetBoltY() < BOLT_HEIGHT/2:
                pos = self._bolts.index(x)
                del self._bolts[pos]
    
      
    def alien_bolt(self, dt):
        """ We discussed how to implement the final for loop with Lawrence Li
        
        Fires a bolt from an alien
        
        This procedure randomly fires a bolt from a non-empty alien in the alien wave""" 
        count = 0
        if self._time >= ALIEN_SPEED and self._direction == 'right':
            for row in self._aliens:
                for alien in row:
                    if alien != None:
                        alien.move_aliens_right(); self._time = 0; count += 1
        if self._time >= ALIEN_SPEED and  self._direction =='left':
            for row in self._aliens:
                for alien in row:
                    if alien != None:
                        alien.move_aliens_left(); self._time = 0; count += 1
        self._time += dt
        if count > self._alienfire:
            list = []
            for x in self._bolts:
                list.append(x.isAlienBolt())
            if True not in list:
                for col in range(ALIENS_IN_ROW):
                    for row in range(len(self._aliens)):
                        random_col = random.randint(0, ALIENS_IN_ROW -1)
                        if self._aliens[row][random_col] is None:
                            pass
                        elif self._aliens[row][random_col] != None:
                            self._bolts.append(Bolt(x = self._aliens[row][random_col].x,
                                                    bottom = self._aliens[row][random_col].y
                                                    - 0.5*ALIEN_HEIGHT - BOLT_HEIGHT -2, width = 5,
                                                    height = 20, linecolor= cornell.GREEN,
                                                    fillcolor = cornell.GREEN, velocity = -BOLT_SPEED))
                            self.move_bolt(); self._alienfire = random.randint(1, BOLT_RATE) 
                            return ''
                        
    def aliens_dead(self):
        """Returns: False if there are still live aliens in the alien wave
        
        This method checks to see if there are still live aliens in the alien wave. If there are none, it returns False.
        """ 
        for row in self._aliens:
            for alien in row:
                if alien != None:
                    return False
                #if this doesn't work append True and False to a list and then check the list
    
    def aliens_win(self):
        """Returns: True if an alien dips below the defense line
        
        This method checks to see if any aliens have dipped below the defense line by checking each y coordinate
        """
        for row in range(len(self._aliens)):
                for alien in range(len(self._aliens[row])):
                    if self._aliens[row][alien] != None:
                        row_as_list = self._aliens[row]
                        alien_as_object = row_as_list[alien]
                        if alien_as_object.y < DEFENSE_LINE + 0.5*ALIEN_HEIGHT:
                            return True 
                        
    def ship_movement(self, input):
        """ Moves the ship left or right
        This procedure moves the player's ship left or right depending on which arrow key was pressed
        """
        if input.is_key_down('left') and self._ship != None:
            self._ship.move_ship((-1)*SHIP_MOVEMENT)
        if input.is_key_down('right') and self._ship != None:
            self._ship.move_ship(SHIP_MOVEMENT)
            
    def alien_wave(self, dt):
        """ Creates the alien and moves the aliens across the screen
        
        This procedure creates a wave of aliens on the screen and moves them across and down over time
        Parameter dt: time in seconds since the last call to the update method
        Precondition: dt is a number"""
        if self._time >= ALIEN_SPEED and self._direction == 'right':
            for row in self._aliens:
                for alien in row:
                    if alien != None:
                        alien.move_aliens_right()
                        self._time = 0
        if self._time >= ALIEN_SPEED and self._direction =='left':
            for row in self._aliens:
                for alien in row:
                    if alien != None:
                        alien.move_aliens_left(); self._time = 0
        self._time += dt
        min = 0.5*ALIEN_WIDTH + ALIEN_H_SEP
        max = GAME_WIDTH - 0.5*ALIEN_WIDTH - ALIEN_H_SEP
        if self._aliens[0][-1] != None:
            if self._aliens[0][-1].x >= max:
                self._direction = 'down'
                for row in self._aliens:
                    for alien in row:
                        if alien != None:
                            alien.move_aliens_down(); self._direction = 'left'
            if self._aliens[0][0] != None:
                if self._aliens[0][0].x <= min:
                    self._direction = 'down'
                    for row in self._aliens:
                        for alien in row:
                            if alien != None:
                                alien.move_aliens_down()
                    self._direction = 'right'
                       
    def restartShip(self):
        """ Reconstructs the ship after it is destroyed
        
        This method reconstructs the ship after gameplay is resumed following the loss of a life"""
        if (self._lives>0):
            self._ship = Ship(x=GAME_WIDTH/2, bottom = SHIP_BOTTOM,
                              width=SHIP_WIDTH, height=SHIP_HEIGHT, source='ship.png')
            
            
    def checkGameOver(self):
        """ Returns: True if the game is over
        
        This method checks if the game is over due to all player lives being lost"""
        if (self._ship == None and self._lives == 0):
            return True
        else:
            return False
        
        
    def checkPaused(self):
        """ Returns: True if the game is paused
        
        This method checks the state of the game for being paused"""
        if (self._ship == None and self._lives > 0):
            return True
        else:
            return False
    

