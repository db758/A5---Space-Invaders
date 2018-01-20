"""
Models module for Alien Invaders

This module contains the model classes for the Alien Invaders game. Anything that you
interact with on the screen is model: the ship, the laser bolts, and the aliens.

Just because something is a model does not mean there has to be a special class for
it.  Unless you need something special for your extra gameplay features, Ship and Aliens
could just be an instance of GImage that you move across the screen. You only need a new 
class when you add extra features to an object. So technically Bolt, which has a velocity, 
is really the only model that needs to have its own class.

With that said, we have included the subclasses for Ship and Aliens.  That is because
there are a lot of constants in consts.py for initializing the objects, and you might
want to add a custom initializer.  With that said, feel free to keep the pass underneath 
the class definitions if you do not want to do that.

You are free to add even more models to this module.  You may wish to do this when you 
add new features to your game, such as power-ups.  If you are unsure about whether to 
make a new class or not, please ask on Piazza.

Debasmita Bhattacharya (db758) and Amelia Myers (arm293)
2 December 2017
"""
from consts import *
from game2d import *

# PRIMARY RULE: Models are not allowed to access anything in any module other than 
# consts.py.  If you need extra information from Gameplay, then it should be
# a parameter in your method, and Wave should pass it as a argument when it
# calls the method.


class Ship(GImage):
    """
    A class to represent the game ship.
    
    At the very least, you want a __init__ method to initialize the ships dimensions.
    These dimensions are all specified in consts.py.
    
    You should probably add a method for moving the ship.  While moving a ship just means
    changing the x attribute (which you can do directly), you want to prevent the player
    from moving the ship offscreen.  This is an ideal thing to do in a method.
    
    You also MIGHT want to add code to detect a collision with a bolt. We do not require
    this.  You could put this method in Wave if you wanted to.  But the advantage of 
    putting it here is that Ships and Aliens collide with different bolts.  Ships 
    collide with Alien bolts, not Ship bolts.  And Aliens collide with Ship bolts, not 
    Alien bolts. An easy way to keep this straight is for this class to have its own 
    collision method.
    
    However, there is no need for any more attributes other than those inherited by
    GImage. You would only add attributes if you needed them for extra gameplay
    features (like animation). If you add attributes, list them below.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    
    # INITIALIZER TO CREATE A NEW SHIP
    def __init__(self, x, bottom, width, height, source):
        """ Initializer for a ship.
        This method initializes the ship image in the game.
        Attributes:
        x: the x-coordinate of the middle of the ship image [int or float]
        bottom: the y coordinate of the bottom edge of the ship image [int or float]
        width: the width of the ship image [int]
        height: the height of the ship image [int]
        source: the image file of the ship image [png]"""
        
        super().__init__(x=GAME_WIDTH/2, bottom = SHIP_BOTTOM, width=SHIP_WIDTH,
                         height=SHIP_HEIGHT, source='ship.png')
        
    # METHODS TO MOVE THE SHIP AND CHECK FOR COLLISIONS
    def move_ship(self, distance):
        """ Moves the ship.
        This helper method moves the ship image a certain distance when called.
        Parameter distance: the distance to move the ship each time the method is called
        Precondition: distance is a number"""
        
        self.x += distance
        
        min = SHIP_WIDTH//2
        max = GAME_WIDTH - SHIP_WIDTH//2
        if self.x < min:
            self.x = min
        if self.x > max:
            self.x = max
            
    def ship_collides(self, bolt):
        """ Return: True is the bolt was fired by an alien and collides with the ship.
        
        Parameter bolt: The laser bolt to check
        Precondition: bolt is of class Bolt"""
        
        if bolt.isAlienBolt() and (self.contains((bolt.x-BOLT_WIDTH/2, bolt.bottom)) or
                                   self.contains((bolt.x+BOLT_WIDTH/2, bolt.bottom)) or
                                   self.contains((bolt.x-BOLT_WIDTH/2, bolt.bottom + BOLT_HEIGHT)) or
                                   self.contains((bolt.x+BOLT_WIDTH/2, bolt.bottom + BOLT_HEIGHT)) ):
            return True 
            
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY


class Alien(GImage):
    """
    A class to represent a single alien.
    
    At the very least, you want a __init__ method to initialize the alien dimensions.
    These dimensions are all specified in consts.py.
    
    You also MIGHT want to add code to detect a collision with a bolt. We do not require
    this.  You could put this method in Wave if you wanted to.  But the advantage of 
    putting it here is that Ships and Aliens collide with different bolts.  Ships 
    collide with Alien bolts, not Ship bolts.  And Aliens collide with Ship bolts, not 
    Alien bolts. An easy way to keep this straight is for this class to have its own 
    collision method.
    
    However, there is no need for any more attributes other than those inherited by
    GImage. You would only add attributes if you needed them for extra gameplay
    features (like giving each alien a score value). If you add attributes, list
    them below.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    
    # INITIALIZER TO CREATE AN ALIEN
    def __init__(self, x, y, width, height, source):
        """ Initializer for an alien.
        This method initializes an alien image in the game.
        Attributes:
        x: the x-coordinate of the middle of the alien image [int or float]
        y: the y coordinate of the middle of the alien image [int or float]
        width: the width of the alien image [int]
        height: the height of the alien image [int]
        source: the image file of the alien image [png]"""
        
        super().__init__(x=x, y=y, width=ALIEN_WIDTH, height=ALIEN_HEIGHT, source=source)
        self._score = 0 

    # METHOD TO CHECK FOR COLLISION (IF DESIRED)
    def alien_collides(self, bolt):
        """ Return: True is the bolt was fired by the player and collides with this alien.
        
        Parameter bolt: The laser bolt to check
        Precondition: bolt is of class Bolt"""
        
        if bolt.isPlayerBolt() and (self.contains((bolt.x-BOLT_WIDTH/2, bolt.bottom)) or
                                   self.contains((bolt.x+BOLT_WIDTH/2, bolt.bottom)) or
                                   self.contains((bolt.x-BOLT_WIDTH/2, bolt.bottom + BOLT_HEIGHT)) or
                                   self.contains((bolt.x+BOLT_WIDTH/2, bolt.bottom + BOLT_HEIGHT)) ):
            return True 
    
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY
    def move_aliens_right(self):
        """ Moves the aliens to the right.
        This helper method moves the alien images ALIEN_H_WALK to the right when called.
        """
        self.x += ALIEN_H_WALK
        
    def move_aliens_down(self):
        """ Moves the aliens down.
        
        This helper method moves the alien images ALIEN_V_WALK down when called.
        
        We extended this part of the game so that at high speeds, the aliens move down a
        uickly but only by a little, whereas at low speeds, the aliens move down slowly
        but by a lot.
        """
        self.y -= ALIEN_V_WALK/ALIEN_ROWS
        
    def move_aliens_left(self):
        """ Moves the aliens to the left.
        This helper method moves the alien images ALIEN_H_WALK to the left when called.
        """
        self.x -= ALIEN_H_WALK
        

class Bolt(GRectangle):
    """
    A class representing a laser bolt.
    
    Laser bolts are often just thin, white rectangles.  The size of the bolt is 
    determined by constants in consts.py. We MUST subclass GRectangle, because we
    need to add an extra attribute for the velocity of the bolt.
    
    The class Wave will need to look at these attributes, so you will need getters for 
    them.  However, it is possible to write this assignment with no setters for the 
    velocities.  That is because the velocity is fixed and cannot change once the bolt
    is fired.
    
    In addition to the getters, you need to write the __init__ method to set the starting
    velocity. This __init__ method will need to call the __init__ from GRectangle as a 
    helper.
    
    You also MIGHT want to create a method to move the bolt.  You move the bolt by adding
    the velocity to the y-position.  However, the getter allows Wave to do this on its
    own, so this method is not required.
    
    INSTANCE ATTRIBUTES:
        _velocity: The velocity in y direction [int or float]
        _bolttime: the time since a bolt was created [int or float]
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """
    def __init__(self, x, bottom, width, height, linecolor, fillcolor, velocity):
        """ Initializer for a bolt.
        This method initilizes a bolt image in the game.
        Attributes:
        x: the x-coordinate of the middle of the alien image [int or float]
        bottom: the y coordinate of the bottom edge of the bolt image [int or float]
        width: the width of the alien image [int]
        height: the height of the alien image [int]
        linecolor: the color of the outline of the bolt [an RBG]
        fillcolor: the color of the bolt [an RGB]
        velocity: the velocity of the bolt when fired [a number]"""
        
        super().__init__(x=x, bottom=bottom, width=width, height=height,
                         linecolor=linecolor, fillcolor=fillcolor)
        self._velocity = velocity
        
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def GetBoltY(self):
        """ Returns: the y attribute of a bolt
    
        This is a getter for the y attribute of a bolt object
        """
        return self.y
    
    def SetBoltY(self, velocity):
        """ Sets the y attribute of a bolt object by incrementing velocity
        
        This is a setter for the y attribute of a bolt object. It sets the y
        attribute by incrementing it by velocity
        
        Parameter velocity: the value to increcement the y attribute by
        Precondition :velocity is a number
        """
        self.y += velocity
    
    def GetBoltVelocity(self):
        """ Returns: the velocity of a bolt
    
        This is a getter for the velocity of a bolt object
        """
        return self._velocity
    
    # INITIALIZER TO SET THE VELOCITY
    
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY
    def isPlayerBolt(self):
        """ Returns: True if the velocity of a bolt object is positive.
        
        This method checks if the velocity of a bolt object is postive, which
        indidcates that the bolt comes from the player's ship""" 
        if self._velocity > 0:
            return True
    
    def isAlienBolt(self):
        """ Returns: True if the velocity of a bolt object is negative.
        
        This method checks if the velocity of a bolt object is negative, which
        indidcates that the bolt comes from the aliens"""
        if self._velocity < 0:
            return True
        
#IF YOU NEED ADDITIONAL MODEL CLASSES, THEY GO HERE
