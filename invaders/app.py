"""
Primary module for Alien Invaders

This module contains the main controller class for the Alien Invaders application. There 
is no need for any additional classes in this module.  If you need more classes, 99% of 
the time they belong in either the wave module or the models module. If you are unsure 
about where a new class should go, post a question on Piazza.

Debasmita Bhattacharya (db758) and Amelia Myers (arm293)
2 December 2017
"""
import cornell
from consts import *
from game2d import *
from wave import *


# PRIMARY RULE: Invaders can only access attributes in wave.py via getters/setters
# Invaders is NOT allowed to access anything in models.py

class Invaders(GameApp):
    """
    The primary controller class for the Alien Invaders application
    
    This class extends GameApp and implements the various methods necessary for processing 
    the player inputs and starting/running a game.
    
        Method start begins the application.
        
        Method update either changes the state or updates the Play object
        
        Method draw displays the Play object and any other elements on screen
    
    Because of some of the weird ways that Kivy works, you SHOULD NOT create an
    initializer __init__ for this class.  Any initialization should be done in
    the start method instead.  This is only for this class.  All other classes
    behave normally.
    
    Most of the work handling the game is actually provided in the class Wave.
    Wave should be modeled after subcontrollers.py from lecture, and will have
    its own update and draw method.
    
    The primary purpose of this class is to manage the game state: which is when the 
    game started, paused, completed, etc. It keeps track of that in an attribute
    called _state.
    
    INSTANCE ATTRIBUTES:
        view:   the game view, used in drawing (see examples from class)
                [instance of GView; it is inherited from GameApp]
        input:  the user input, used to control the ship and change state
                [instance of GInput; it is inherited from GameApp]
        _state: the current state of the game represented as a value from consts.py
                [one of STATE_INACTIVE, STATE_NEWWAVE, STATE_ACTIVE, STATE_PAUSED, STATE_CONTINUE, STATE_COMPLETE]
        _wave:  the subcontroller for a single wave, which manages the ships and aliens
                [Wave, or None if there is no wave currently active]
        _text:  the currently active message
                [GLabel, or None if there is no message to display]
        lastkeys: the number of keys pressed last frame [int >= 0]
    
    STATE SPECIFIC INVARIANTS: 
        Attribute _wave is only None if _state is STATE_INACTIVE.
        Attribute _text is only None if _state is STATE_ACTIVE.
    
    For a complete description of how the states work, see the specification for the
    method update.
    
    You may have more attributes if you wish (you might want an attribute to store
    any score across multiple waves). If you add new attributes, they need to be 
    documented here.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    _bg : the background of the start screen
    _livestext : the text displaying how many lives are left
    _wintext: the text displaying the win message
    _losetext: the text displaying the lose message
    _pausedtext: the text displayed the paused message when a ship life is lost
    """
    
    # DO NOT MAKE A NEW INITIALIZER!
    
    # THREE MAIN GAMEAPP METHODS
    def start(self):
        """
        Initializes the application.
        
        This method is distinct from the built-in initializer __init__ (which you 
        should not override or change). This method is called once the game is running. 
        You should use it to initialize any game specific attributes.
        
        This method should make sure that all of the attributes satisfy the given 
        invariants. When done, it sets the _state to STATE_INACTIVE and create a message 
        (in attribute _text) saying that the user should press to play a game.
        """
        
        self._wave = None
        self._state = STATE_INACTIVE
        self.lastkeys = 0
        self._text = GLabel(text="Press Any Key To Play", x=400, y=350, linecolor=cornell.WHITE,
                            font_size= 50, font_name = "RetroGame")
        self._bg = GImage(x= 400, y= 350, width = 800, height = 800, source = 'Space.png') 
        self._pausedtext = GLabel(text="You Lost A Life, Press Any Key To Play", x=400, y=350, linecolor=cornell.BLUE,
                            font_size= 25, font_name = "RetroGame")
        self._wintext = GLabel(text="Yay, You Won!", x=400, y=350, linecolor=cornell.BLUE,
                            font_size= 50, font_name = "RetroGame")
        self._losetext = GLabel(text="Oops, You Lost, Try Again", x=400, y=350, linecolor=cornell.BLUE,
                            font_size= 25, font_name = "RetroGame")
        
    
    def update(self,dt):
        """
        We discussed how to implement STATE_PAUSED with Peter Oh.
        
        Animates a single frame in the game.
        
        It is the method that does most of the work. It is NOT in charge of playing the
        game.  That is the purpose of the class Wave. The primary purpose of this
        game is to determine the current state, and -- if the game is active -- pass
        the input to the Wave object _wave to play the game.
        
        As part of the assignment, you are allowed to add your own states. However, at
        a minimum you must support the following states: STATE_INACTIVE, STATE_NEWWAVE,
        STATE_ACTIVE, STATE_PAUSED, STATE_CONTINUE, and STATE_COMPLETE.  Each one of these 
        does its own thing and might even needs its own helper.  We describe these below.
        
        STATE_INACTIVE: This is the state when the application first opens.  It is a 
        paused state, waiting for the player to start the game.  It displays a simple
        message on the screen. The application remains in this state so long as the 
        player never presses a key.  In addition, this is the state the application
        returns to when the game is over (all lives are lost or all aliens are dead).
        
        STATE_NEWWAVE: This is the state creates a new wave and shows it on the screen. 
        The application switches to this state if the state was STATE_INACTIVE in the 
        previous frame, and the player pressed a key. This state only lasts one animation 
        frame before switching to STATE_ACTIVE.
        
        STATE_ACTIVE: This is a session of normal gameplay.  The player can move the
        ship and fire laser bolts.  All of this should be handled inside of class Wave
        (NOT in this class).  Hence the Wave class should have an update() method, just
        like the subcontroller example in lecture.
        
        STATE_PAUSED: Like STATE_INACTIVE, this is a paused state. However, the game is
        still visible on the screen.
        
        STATE_CONTINUE: This state restores the ship after it was destroyed. The 
        application switches to this state if the state was STATE_PAUSED in the 
        previous frame, and the player pressed a key. This state only lasts one animation 
        frame before switching to STATE_ACTIVE.
        
        STATE_COMPLETE: The wave is over, and is either won or lost.
        
        You are allowed to add more states if you wish. Should you do so, you should 
        describe them here.
        
        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        if self._state == STATE_INACTIVE:
            self._determineState()
            
        if self._state == STATE_ACTIVE:
            self._wave.update(self.input, dt)
            
        if self._state == STATE_ACTIVE:
            if self._wave._ship is None and self._wave._lives > 0:
                self._state = STATE_PAUSED
        if self._state == STATE_NEWWAVE:
            self._wave = Wave()
            self._state = STATE_ACTIVE
        
        if self._state == STATE_PAUSED:
            self.playAgain()
            
        if self._state == STATE_CONTINUE:
            self._state = STATE_ACTIVE
            
        if self._state == STATE_ACTIVE:
            if self._wave.checkPaused():
                self._state = STATE_PAUSED
            if self._wave.checkGameOver():
                self._state = STATE_COMPLETE
            
            if self._wave.aliens_dead() == True or self._wave.aliens_win() == True:
                self._state = STATE_COMPLETE
        
        
            
    def draw(self):
        """
        We discussed how to handle drawing in STATE_PAUSED with Peter Oh. 
        Draws the game objects to the view.
        
        Every single thing you want to draw in this game is a GObject.  To draw a GObject 
        g, simply use the method g.draw(self.view).  It is that easy!
        
        Many of the GObjects (such as the ships, aliens, and bolts) are attributes in 
        Wave. In order to draw them, you either need to add getters for these attributes 
        or you need to add a draw method to class Wave.  We suggest the latter.  See 
        the example subcontroller.py from class.
        
        We extended this section by adding a background image for the start screen and STATE_ACTIVE,
        by displaying the number of lives left, and by displaying the current game score.
        """
        # IMPLEMENT ME
        if self._state == STATE_INACTIVE:
            self._bg.draw(self.view)
            self._text.draw(self.view)
        elif self._state != STATE_INACTIVE:
            self._text = None   
        if self._state == STATE_NEWWAVE or self._state == STATE_ACTIVE:
            self._bg.draw(self.view)
            self._wave.draw_aliens(self.view)
            self._livestext = GLabel(text="Lives: " + str(self._wave._lives), x=120, y=650, linecolor=cornell.WHITE,
                            font_size= 25, font_name = "RetroGame")
            self._livestext.draw(self.view)
            self._scoretext = GLabel(text="Score: " + str(self._wave._score), x=620, y=650, linecolor=cornell.WHITE,
                            font_size= 25, font_name = "RetroGame")
            self._scoretext.draw(self.view) 
        if self._state == STATE_NEWWAVE or self._state == STATE_ACTIVE:
            self._wave.draw_ship(self.view)   
        if self._state == STATE_NEWWAVE or self._state == STATE_ACTIVE:
            self._wave.draw_dline(self.view)   
        if (self._state == STATE_NEWWAVE or self._state == STATE_ACTIVE):
            #if(input.is_key_down('spacebar')):
                self._wave.draw_bolt(self.view)       
        if self._state == STATE_PAUSED and self._pausedtext != None:
            self._pausedtext.draw(self.view)    
        if self._state == STATE_COMPLETE:
            if self._wave._ship is None and self._wave._lives == 0:
                self._losetext.draw(self.view)
            elif  self._wave.aliens_win():
                self._losetext.draw(self.view)
            else:
                self._wintext.draw(self.view)
        
        
    # HELPER METHODS FOR THE STATES GO HERE
    
    def _determineState(self):
        """
        We used the implementation provided by Walker White during lecture.
        
        Determines the current state and assigns it to self.state
        
        This method checks for a key press, and if there is one, changes the state 
        to the next value.  A key press is when a key is pressed for the FIRST TIME.
        We do not want the state to continue to change as we hold down the key.  The
        user must release the key and press it again to change the state.
        """
        # Determine the current number of keys pressed
        curr_keys = self.input.key_count
        
        # Only change if we have just pressed the keys this animation frame
        change = curr_keys > 0 and self.lastkeys == 0
        
        if change:
            # Click happened.  Change the state
            self._state = STATE_NEWWAVE
            self._text = None
        
        # Update last_keys
        self.lastkeys= curr_keys
    
    def playAgain(self):
        """
        We used the implementation provided by Walker White during lecture.
        
        Determines the current state and assigns it to self.state
        
        This method checks for a key press, and if there is one, changes the state 
        to the next value.  A key press is when a key is pressed for the FIRST TIME.
        We do not want the state to continue to change as we hold down the key.  The
        user must release the key and press it again to change the state.
        """
        # Determine the current number of keys pressed
        curr_keys = self.input.key_count
        
        # Only change if we have just pressed the keys this animation frame
        change = curr_keys > 0 and self.lastkeys == 0
        
        if change:
            # Click happened.  Change the state
            self._state = STATE_CONTINUE
            self._wave.restartShip()
           
        # Update last_keys
        self.lastkeys = curr_keys
    
    
    