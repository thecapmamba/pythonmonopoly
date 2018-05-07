"""
 *****************************************************************************
   FILE:  game.py

   AUTHOR: Josh Caplan

   ASSIGNMENT: CS110 Final Project (Game)

   DATE: 5/1/18

   DESCRIPTION: This is a fully functioning 2-player monopoly game with 
   simplified rules as outlined in the user manual.

 *****************************************************************************
"""

from cs110graphics import *
import random


class Container(EventHandler):
    ''' Defines the parameters of any container that handles events '''

    def __init__(self, win, center, space=True):
        ''' Initializes a container '''

        EventHandler.__init__(self)
        self._win = win
        self._center = center
        self._space = space

    def get_center(self):
        return self._center


class corner_space(Container):
    ''' Defines the parameters for a corner space'''

    def __init__(self, win, width, height, center, text='', jail=False):
        ''' initializes a corner space '''

        Container.__init__(self, win, center)
        self._space = True
        self._text = Text(win, text, 10, center)
        self._win.add(self._text)
        self._width = width
        self._height = height
        self._spot = Rectangle(win, width, height, center)
        self._win.add(self._spot)
        self._jail = jail


class chance(Container):
    ''' Defines the parameters for a chance space '''

    def __init__(self, win, width, height, center, game):
        ''' Initializes a chance space '''

        Container.__init__(self, win, center)
        self._ = True
        self._width = width
        self._game = game
        self._height = height
        self._spot = Rectangle(win, width, height, center)
        self._text = Text(win, 'Chance', 8, center)
        self._text.set_depth(3)
        self._win.add(self._spot)
        self._win.add(self._text)
        
        # List of numbers representing chance cards 
        self._chancelist = [0, 1, 2]

    def choose(self):
        ''' Chooses a chance card at random and performs action on player '''
        
        card = random.choice(self._chancelist)
        self._text = None
        
        if card == 0:
            self._text = Text(self._win, "LOTTERY WIN! GET $50",
                                         16, (250, 385))
            self._text.set_depth(2)
            self._win.add(self._text)
            player.receive(self._game._currentplayer, 50)
        if card == 1:
            self._text = Text(self._win, "PAY HOSPITAL $100",
                                         16, (250, 385))
            self._win.add(self._text)
            self._game._currentplayer.pay(100)
        if card == 2:
            self._text = Text(self._win, "PAY DOCTOR $50",
                                         16, (250, 385))
            self._win.add(self._text)
            self._game._currentplayer.pay(50)

    def remove_all(self):
        ''' Removes the chance text '''
        self._win.remove(self._text)


class incometax(Container):
    ''' Defines the parameters of an income tax space '''

    def __init__(self, win, width, height, center):
        ''' Initializes an income tax space '''
        Container.__init__(self, win, center)
        self._space = True
        self._width = width
        self._height = height
        self._spot = Rectangle(win, width, height, center)
        self._win.add(self._spot)
        self._text1 = Text(win, 'Income', 8, (center[0], center[1] - 5))
        self._text2 = Text(win, 'Tax', 8, (center[0], center[1] + 10))
        self._text1.set_depth(3)
        self._text2.set_depth(3)
        self._win.add(self._text1)
        self._win.add(self._text2)


class communitychest(Container):
    ''' Defines the parameters of a community chest space '''

    def __init__(self, win, width, height, center, game):
        ''' Initializes a community chest space '''

        Container.__init__(self, win, center)
        self._space = True
        self._width = width
        self._height = height
        self._game = game
        self._win = win
        
        self._spot = Rectangle(win, width, height, center)
        self._win.add(self._spot)
        
        self._text1 = Text(win, 'Com', 8, (center[0], center[1] - 5))
        self._text2 = Text(win, 'Chest', 8, (center[0], center[1] + 10))
        self._text1.set_depth(3)
        self._text2.set_depth(3)

        self._win.add(self._text1)
        self._win.add(self._text2)
        
        # List of numbers representing community chest cards
        self._cclist = [0, 1, 2]

    def choose(self):
        ''' Chooses a community chest card and performs action on player '''

        card = random.choice(self._cclist)
        self._text = None
        
        if card == 0:
            self._text = Text(self._win, "LOTTERY WIN! GET $50",
                                         14, (250, 385))
            self._text.set_depth(2)
            self._win.add(self._text)
            player.receive(self._game._currentplayer, 50)
        
        if card == 1:
            self._text = Text(self._win, "PAY HOSPITAL $100",
                                         14, (250, 385))
            self._win.add(self._text)
            self._game._currentplayer.pay(100)
        
        if card == 2:
            self._text = Text(self._win, "PAY DOCTOR $50",
                                         14, (250, 385))
            self._win.add(self._text)
            self._game._currentplayer.pay(50)

    def remove_all(self):
        ''' Removes the community chest card text from window '''
        self._win.remove(self._text)

class property(Container):
    ''' Defines the parameters of a property space '''

    def __init__(self, win, width, height, center, idnum, category,
                 monopoly=False, color='white', price=0, rent=0, name=None,
                 owned=False, owner=None):
        ''' Initializes a property space '''

        Container.__init__(self, win, center)
        self._space = False
        self._width = width
        self._name = name
        self._rent = rent
        self._center = center
        self._height = height
        self._color = color
        self._owned = owned
        self._price = price
        self._idnum = idnum
        self._monopoly = monopoly
        self._category = category
        self._spot = Rectangle(win, width, height, center)
        self._spot.set_depth(10)
        self._owner = owner
        radius = width // 2

        # Based on where each horizontal or vertical array of spaces should be,
        # change the dimensions of the property accordingly so it faces
        # the proper direction
        if self._height > self._width and center[1] > 105:
            self._colorbox = Rectangle(win, width, height // 4, (center[0],
                                       center[1] - radius - 7))
        elif self._height < self._width and center[0] < 105:
            self._colorbox = Rectangle(win, width // 4, height,
                                       (center[0] + radius - 8, center[1]))
        elif self._height > self._width and center[1] < 105:
            self._colorbox = Rectangle(win, width, height // 4,
                                       (center[0], center[1] + radius + 7))
        elif self._height < self._width and center[0] > 105:
            self._colorbox = Rectangle(win, width // 4, height,
                                       (center[0] - radius + 8, center[1]))

        # Based on the direction the space faces, change the location of the
        # of the price on the space
        if self._height > self._width and center[1] > 105:
            self._text = Text(win, '$' + str(self._price), 8, (center[0],
                              center[1] + 20))
        elif self._height < self._width and center[0] < 105:
            self._text = Text(win, '$' + str(self._price), 8,
                              (center[0] - 20, center[1]))
        elif self._height > self._width and center[1] < 105:
            self._text = Text(win, '$' + str(self._price), 8,
                              (center[0], center[1] - 20))
        elif self._height < self._width and center[0] > 105:
            self._text = Text(win, '$' + str(self._price), 8,
                              (center[0] + 20, center[1]))

        self._colorbox.set_fill_color(color)
        self._colorbox.set_depth(5)

        self._text.set_depth(3)
        self._win.add(self._text)

        self._win.add(self._spot)
        self._win.add(self._colorbox)
    
    def name(prop):
        ''' Returns the name of the property '''
        
        return prop._name
    
    def check_owned(self, prop):
        ''' Returns if the propety is owned '''
        
        return prop._owned 
   
    def return_price(prop):
        ''' Returns the price of the property '''

        return prop._price
    
    def make_owned(self, prop):
        ''' Mark the property as owned '''

        prop._owned = True

    def check_owner(prop):
        ''' Return the player that owns the property '''
        return prop._owner
    
    def make_owner_player(self, prop, player):
        ''' Make the current player the property's owner '''

        prop._owner = player
    
    def check_idnum(prop):
        ''' Returns the id number of the property '''

        return prop._idnum
    
    def return_rent(prop):
        ''' Returns the rent of the property '''

        return prop._rent

    def return_center(prop):
        ''' Returns the center of the property '''

        return prop._center

    def return_category(prop):
        ''' Returns the categorty of properties the property is in '''
        
        return prop._category
    
    def check_monopoly(prop):
        ''' Checks if the owner has a monopoly on the property's category '''
        
        return prop._monopoly


class Game(object):
    ''' Defines the initial setup of the game '''

    def __init__(self, win):
        ''' Initializes the setup of the game '''
        self._win = win
        self._win.set_background("burlywood")
        
        # Builds the gameboard
        self._go = corner_space(win, 70, 70, (465, 500), "GO")
        self._medave = property(win, 40, 70, (410, 500), 1, 1, False,
                                'purple', 60, 2, "Med Ave")
        self._communitychest1 = communitychest(win, 40, 70, (370, 500), self)
        self._balticave = property(win, 40, 70, (330, 500), 2, 1, False,
                                   'purple', 60, 4, "Baltic Ave")
        self._incometax = incometax(win, 40, 70, (290, 500))
        self._readingrail = property(win, 40, 70, (250, 500), 23, 10, False,
                                     'black', 200, 50, "Reading Railroad")
        self._orientalave = property(win, 40, 70, (210, 500), 3, 2, False,
                                     'light blue', 100, 6, "Oriental Ave")
        self._chance1 = chance(win, 40, 70, (170, 500), self)
        self._vermontave = property(win, 40, 70, (130, 500), 4, 2, False,
                                    'light blue', 100, 6, "Vermont Ave")
        self._connave = property(win, 40, 70, (90, 500), 5, 2, False,
                                 'light blue', 120, 8, "Connecticut Ave")
        self._jail = corner_space(win, 70, 70, (35, 500), "Jail", True)

        self._stcharplace = property(win, 70, 40, (35, 445), 6, 3, False,
                                     'pink', 140, 10, "St. Charles Place")
        self._electriccompany = property(win, 70, 40, (35, 405), 27, 11, False,
                                         'white', 150, 10, "Electric Company")
        self._statesave = property(win, 70, 40, (35, 365), 7, 3, False,
                                   'pink', 140, 10, "States Ave")
        self._virginiaave = property(win, 70, 40, (35, 325), 8, 3, False,
                                     'pink', 160, 12, "Virginia Ave")
        self._pennrail = property(win, 70, 40, (35, 285), 24, 10, False,
                                  'black', 200, 50, "Pennsylvania Railroad")
        self._stjamesplace = property(win, 70, 40, (35, 245), 9, 5, False,
                                      'orange', 180, 14, "St. James Place")
        self._communitychest2 = communitychest(win, 70, 40, (35, 205), self)
        self._tennave = property(win, 70, 40, (35, 165), 10, 5, False,
                                 'orange', 180, 14, "Tennessee Ave")
        self._nyave = property(win, 70, 40, (35, 125), 11, 5, False, 'orange',
                               200, 16, "New York Avenue")
        self._freeparking = corner_space(win, 70, 70, (35, 70), "Parking")
        # Row 2
        self._kentuckyave = property(win, 40, 70, (90, 70), 12, 6, False,
                                     'red', 220, 18, "Kentucky Ave")
        self._chance2 = chance(win, 40, 70, (130, 70), self)
        self._indianaave = property(win, 40, 70, (170, 70), 13, 6, False,
                                    'red', 220, 18, "Indiana Ave")
        self._illinoisave = property(win, 40, 70, (210, 70), 14, 6, False,
                                     'red', 240, 20, "Illinois Ave")
        self._borailroad = property(win, 40, 70, (250, 70), 25, 10, False,
                                    'black', 200, 50, "B&O Railroad")
        self._atlanticave = property(win, 40, 70, (290, 70), 15, 7, False,
                                     'yellow', 260, 22, "Atlantic Ave")
        self._ventnorave = property(win, 40, 70, (330, 70), 16, 7, False,
                                    'yellow', 260, 22, "Ventnor Ave")
        self._waterworks = property(win, 40, 70, (370, 70), 28, 11, False,
                                    'white', 150, 10, "Water Works")
        self._marvgardens = property(win, 40, 70, (410, 70), 17, 7, False,
                                     'yellow', 280, 24, "Marvin Gardens")
        self._gotojail = corner_space(win, 70, 70, (465, 70), "GOTO Jail")
        # Column right
        self._pacificave = property(win, 70, 40, (465, 125), 18, 8, False,
                                    'green', 300, 26, "Pacific Avenue")
        self._ncave = property(win, 70, 40, (465, 165), 19, 8, False,
                               'green', 300, 26, "North Carolina Ave")
        self._communitychest3 = communitychest(win, 70, 40, (465, 205), self)
        self._pennave = property(win, 70, 40, (465, 245), 20, 8, False,
                                 'green', 320, 28, "Pennsylvania Ave")
        self._shortlinerail = property(win, 70, 40, (465, 285), 26, 10, False,
                                       'black', 200, 50, "Shortline Railroad")
        self._chance3 = chance(win, 70, 40, (465, 325), self)
        self._parkplace = property(win, 70, 40, (465, 365), 21, 9, False,
                                   'blue', 350, 35, "Park Place")
        self._incometax2 = incometax(win, 70, 40, (465, 405))
        self._boardwalk = property(win, 70, 40, (465, 445), 22, 9, False,
                                   'blue', 400, 50, "Boardwalk")

        # List used to index the gameboard
        self._spots = [self._go, self._medave, self._balticave,
                       self._incometax, self._readingrail, self._orientalave,
                       self._chance1, self._vermontave, self._connave,
                       self._jail, self._stcharplace, self._electriccompany,
                       self._statesave, self._virginiaave, self._pennrail,
                       self._stjamesplace, self._communitychest2,
                       self._tennave, self._nyave, self._freeparking,
                       self._kentuckyave, self._chance2, self._indianaave,
                       self._illinoisave, self._borailroad, self._atlanticave,
                       self._ventnorave, self._waterworks, self._marvgardens,
                       self._gotojail, self._pacificave, self._ncave,
                       self._communitychest3, self._pennave,
                       self._shortlinerail, self._chance3, self._parkplace,
                       self._incometax2, self._boardwalk]

        # Creates the players in the game
        self._player1 = player(win, 8, self, (465, 500), 1, 'blue', 'Player 1')
        self._player2 = player(win, 8, self, (465, 500), 2, 'red', "Player 2")
        self._playerlist = [self._player1, self._player2]

        # Creates the die in the game
        die1 = Die(win, width=40, center=(170, 200), diecolor='red')
        die2 = Die(win, width=40, center=(320, 200), diecolor='red')
        die1.addTo(win)
        die2.addTo(win)

        # Sets the current player
        self._currentplayer = self._playerlist[0]

        # Changes the current player
        if self._currentplayer == self._playerlist[0]:
            self._otherplayer = self._playerlist[1]
        
        elif self._currentplayer == self._playerlist[1]:
            self._otherplayer = self._playerlist[0]

        # Creates a roll button that controls the die
        self._roll = roll(self._currentplayer, self, win, die1, die2)

        # Creates the end turn button
        self._end_turn = end_turn(win, self, self._roll)

        # Creates the info section for each player
        self._player1_info = info(win, self._currentplayer, (750, 50), 350,
                                  150, 'Player 1 (Blue)')
        self._player2_info = info(win, self._otherplayer, (750, 300), 350, 150,
                                  'Player 2 (Red)')
        self._currentplayer.set_info(self._player1_info)
        self._otherplayer.set_info(self._player2_info)

        # Defines a notebox that can be used to display messages
        self._note = Text(self._win, '', 16, (250, 350))
        self._notebox = Rectangle(self._win, 300, 60, (250, 350))
        self._notebox.set_fill_color("burlywood")

        # Defines a note that is prompted when rolling in jail
        self._jailnote = Text(self._win, "Visited Jail! Charged $100", 16,
                              (250, 385))
        self._jailbox = Rectangle(self._win, 300, 60, (250, 385))
        self._notebox.set_fill_color("burlywood")
        
        # Defines a note that reports what the player has rolled
        self._rollbox = Text(self._win, '', 16, (250, 150))
        self._win.add(self._rollbox)

    def report_move(self, rolltotal):
        ''' Reports to the player how much to move from current position '''

        currentposition = self._currentplayer.position()
        newpos = (currentposition + rolltotal) % 39
        # If the player passes go, give them $200
        if (currentposition + rolltotal - 1) >= 40:
            player.receive(self._currentplayer, 200)
        '''
        self._currentplayer.move_to(self._spots[newposition-1].get_center(),
                                   newposition-1)
        '''                           
        if currentposition == 0:
            self._currentplayer.move_to(self._spots[newpos - 1].get_center(),
                                        newpos - 1)
        else:
            self._currentplayer.move_to(self._spots[newpos].get_center(),
                                        newpos)
        
    def get_currrentplayer(self):
        ''' Returns who is the current player '''
        
        return self._currentplayer
    
    def text_box(self):
        ''' Builds a text box that text can be placed over '''
        textbox = Rectangle(self._win, 275, 125, (250, 375))
        textbox.set_fill_color('burlywood')
        self._win.add(textbox)
        textbox.set_depth(5)

class check_winner():
    ''' Checks to see if the game is over, if so, it decides a winner '''
    
    def __init__(self, win, game):
        ''' Initializes the checking for the game being over, if so,
        this function also decides the winner '''
        
        self._win = win
        self._game = game

        # Total value of each players assets (money + property)
        currentplayer_total_value = 0
        otherplayer_total_value = 0

        # If either player has a balance of 0, add up their total value
        if player.balance(self._game._currentplayer) == 0 or \
           player.balance(self._game._otherplayer) == 0:

            for prop_cat in self._game._currentplayer._propsowned:

                for prop in prop_cat:
                    prop_value = property.return_price(prop)
                    currentplayer_total_value += prop_value
                    currentplayer_total_value += \
                        player.balance(self._game._currentplayer)

            for prop_cat in self._game._otherplayer._propsowned:
                
                for prop in prop_cat:
                    prop_value = property.return_price(prop)
                    otherplayer_total_value += prop_value
                    otherplayer_total_value += \
                        player.balance(self._game._otherplayer)

            # If current player has higher total value, returns them as winner
            # and provides their value and the losers lesser value
            if currentplayer_total_value > otherplayer_total_value:
                winner_box = Rectangle(self._win, 1000, 550, (500, 275))
                winner_box.set_depth(2)
                winner_box.set_fill_color("Pink")
                win_text = Text(self._win,
                                str(player.name(self._game._currentplayer)) +
                                " is your winner!", 16, (500, 275))
                win_text.set_depth(1)
                win_amount = Text(self._win,
                                  str(player.name(self._game._currentplayer)) +
                                  " had a total value of $" +
                                  str(currentplayer_total_value), 16,
                                  (500, 300))
                loser_amount = Text(self._win,
                                    str(player.name(self._game._otherplayer)) +
                                    " only had $" +
                                    str(otherplayer_total_value), 16,
                                    (500, 325))

                winner_amount.set_depth(1)
                loser_amount.set_depth(1)
                self._win.add(winner_box)
                self._win.add(win_text)
                self._win.add(win_amount)
                self._win.add(loser_amount)
                self._win.remove(self._game._currentplayer._pawn)
                self._win.remove(self._game._otherplayer._pawn)

            # If the other player has higher total value, returns them as
            # winner and provides their value and the losers lesser value
            elif otherplayer_total_value > currentplayer_total_value:
                winner_box = Rectangle(self._win, 1000, 550, (500, 275))
                winner_box.set_depth(2)
                winner_box.set_fill_color("Pink")
                win_text = Text(self._win,
                                str(player.name(self._game._otherplayer)) +
                                " is your winner!", 16, (500, 275))
                win_amount = Text(self._win,
                                  str(player.name(self._game._otherplayer)) +
                                  " had a total value of $" +
                                  str(otherplayer_total_value), 16,
                                  (500, 300))
                loser_amount = Text(self._win,
                                    player.name(self._game._currentplayer) +
                                    "only had a total value of $" +
                                    str(currentplayer_total_value), 16,
                                    (500, 325))
                win_text.set_depth(1)
                win_amount.set_depth(1)
                loser_amount.set_depth(1)
                self._win.add(winner_box)
                self._win.add(win_text)
                self._win.add(win_amount)
                self._win.add(loser_amount)
                self._win.remove(self._game._currentplayer._pawn)
                self._win.remove(self._game._otherplayer._pawn)


class end_turn(EventHandler):
    ''' Defines the parameters and functions of the end turn button '''

    def __init__(self, win, game, roll):
        ''' Initializes the end turn button '''

        EventHandler.__init__(self)
        self._win = win
        self._game = game
        self._roll = roll
        self._endturn = Rectangle(win, 70, 50, (245, 250))
        self._endturn.set_depth(10)
        self._endturn.set_fill_color("White")
        self._text = Text(win, 'End Turn', 10, (245, 250))
        self._text.set_depth(5)
        self._win.add(self._endturn)
        self._win.add(self._text)
        self._endturn.add_handler(self)
        self._text.add_handler(self)

    def handle_mouse_release(self, win):
        ''' Triggers actions in the event handler when the mouse clicks the
            end turn button and is released. '''

        # If the player has rolled and any property decisions have
        # been made change the turn and check if there is a winner
        curpos = self._game._spots[self._game._currentplayer._position]
        if type(curpos) == chance:
            chance.remove_all(curpos)
        elif type(curpos) == communitychest:
            communitychest.remove_all(curpos)

        if self._roll.return_enabled() is False:
            
            if self._game._currentplayer.return_decisionmade() is True:
                if self._game._currentplayer == self._game._playerlist[0]:
                    self._game._currentplayer = self._game._playerlist[1]
                    self._roll.enable()
                    end_turn.inactive_color(self)
                    player.remove_win(self._game)
                    roll.remove_jailnote(self._game)
                    self._roll._dubcounter = 0
                    check_winner(self._win, self._game)
                
                elif self._game._currentplayer == self._game._playerlist[1]:
                    self._game._currentplayer = self._game._playerlist[0]
                    self._roll.enable()
                    roll.remove_jailnote(self._game)
                    self._roll._dubcounter = 0
                    player.remove_win(self._game)
                    end_turn.inactive_color(self)
                    check_winner(self._win, self._game)
        
            # If a decision hasn't been made, check winner but nothing else
            elif self._game._currentplayer.return_decisionmade() is False:
                check_winner(self._win, self._game)
            
    def active_color(self):
        ''' Sets the end turn button to its active color '''

        self._endturn.set_fill_color("Green")

    def inactive_color(self): 
        ''' Sets the end turn button to its inactive color '''
        self._endturn.set_fill_color("White")


class Die:
    ''' Defines the properties of a die. This class was taken from Professor
        Cambell's classnotes. I have not commented on it because it was
        taken from the classnotes (TA approved idea)  '''

    # class variables
    SIDES = 6
    POSITIONS = [None,
                 [(0, 0), None, None, None, None, None],
                 [(-.25, -.25), (.25, .25), None, None, None, None],
                 [(-.25, -.25), (.25, .25), (0, 0), None, None, None],
                 [(-.25, -.25), (.25, .25), (.25, -.25), (-.25, .25),
                  None, None],
                 [(-.25, -.25), (.25, .25), (.25, -.25), (-.25, .25), (0, 0),
                  None],
                 [(-.25, -.25), (.25, .25), (.25, -.25), (-.25, .25),
                  (-.25, 0), (.25, 0)]]

    def __init__(self, win, width=30, center=(200, 200), diecolor='white',
                 pipcolor='blue'):
        self._value = 1
        self._win = win
        self._square = Rectangle(win, width, width, center)
        self._square.set_depth(20)
        self._square.set_fill_color(diecolor)
        self._width = width
        self._center = center
        self._pips = []
        for _ in range(Die.SIDES):
            pip = Circle(win, round(width / 12), center)
            pip.set_border_color(pipcolor)
            pip.set_fill_color(pipcolor)
            pip.set_depth(19)
            self._pips.append(pip)

    def addTo(self, win):
        win.add(self._square)
        for pip in self._pips:
            win.add(pip)
    
    def roll(self):
        self._value = random.randrange(Die.SIDES) + 1
        self._update()
        return self._value

    def _update(self):
        positions = Die.POSITIONS[self._value]
        cx, cy = self._center
        for i in range(len(positions)):
            if positions[i] is None:
                self._pips[i].set_depth(25)  # behind the die body.
            else:
                self._pips[i].set_depth(15)
                fx, fy = positions[i]
                self._pips[i].move_to((round(cx + fx * self._width),
                                       round(cy + fy * self._width)))


class roll(EventHandler):
    ''' Defines the roll button and its functions '''

    def __init__(self, player, game, win, die1, die2):
        ''' Initializes the roll button '''

        EventHandler.__init__(self)
        self._game = game
        self._player = player
        self._win = win
        self._die1 = die1
        self._die2 = die2
        self._roll_button = Rectangle(win, 70, 50, (245, 200))
        self._roll_button.set_depth(10)
        self._roll_text = Text(win, 'Roll', 16, (245, 200))
        self._roll_text.set_depth(5)
        self._win.add(self._roll_button)
        self._win.add(self._roll_text)
        self._roll_button.add_handler(self)
        self._roll_text.add_handler(self)
        self._enabled = True
        self._roll_button.set_fill_color("Green")
        self._dubcounter = 0

    def handle_mouse_release(self, win):
        ''' When clicked, roll the die and report the values '''

        if self._enabled:
            self._value1 = self._die1.roll()
            self._value2 = self._die2.roll()
            self._movetotal = self._value1 + self._value2
            self._game._rollbox.set_text('You rolled ' +
                                         str(self._movetotal) + '!')
            
            # If not doubles, disable roll and move the piece
            if self._value1 != self._value2:
                roll.disable(self)
                self._game.report_move(self._movetotal)
            
            # If doubles, keep track of how many in a row
            else:
                self._dubcounter += 1
                # If three doubles in a row, send to jail
                if self._dubcounter == 3:
                    gojail = self._game._spots[9]
                    self._player.move_to(property.return_center(gojail), 10)
                    self._player._position = 10
                    self._win.add(self._game._jailnote)
                    self._win.add(self._game._jailbox)
                    player.pay(self._player, 100)
                    roll.disable(self)
                    self._game._end_turn.active_color()
                    
                # Else, report the players move
                else:
                  
                    self._game.report_move(self._movetotal)

        else:
            pass

    def enable(self):
        ''' Enables the roll button '''
        self._enabled = True
        self._roll_button.set_fill_color("Green")
        return self._enabled
   
    def disable(self):
        ''' Disables the roll button '''
        self._roll_button.set_fill_color("White")
        self._enabled = False
        return self._enabled
    
    def return_enabled(self):
        ''' Returns if the roll button is enabled '''
        return self._enabled
    
    def return_roll(self):
        ''' Returns the total value of the rolled die '''
        return self._movetotal
    
    def remove_jailnote(self):
        ''' Removes the note telling the player they have gone to jail '''
        self._win.remove(self._jailnote)
        self._win.remove(self._jailbox)

class player(EventHandler):
    ''' Defines a player attributes and functions '''

    def __init__(self, win, radius, game, center, idnum, color='red', name=''):
        ''' Initializes a player '''

        EventHandler.__init__(self)
        self._win = win
        self._radius = radius
        self._center = center
        self._color = color
        self._game = game
        self._name = name
        self._position = 0
        self._info = None
        self._pawn = Circle(win, radius, center)
        self._pawn.set_fill_color(color)
        self._pawn.set_depth(1)
        self._win.add(self._pawn)
        self._pawn.add_handler(self)
        self._balance = 1500
        self._decisionmade = True
        self._propsowned = [[], [], [], [], [], [], [], [], [], [], [], []]
        self._idnum = idnum

    def move_to(self, cords, position):
        ''' Moves a player to a given position '''

        self._position = position
        self._pawn.move_to(cords)

        # If the positon is gotojail, move the piece to jail and charge them
        # the jail fee
        currentspace = self._game._spots[self._position]
        if self._position == 29:
            self._position = 10
            self._pawn.move_to(property.return_center(self._game._spots[9]))
            self._win.add(self._game._jailnote)
            self._win.add(self._game._jailbox)
            self.pay(100)
            roll.disable(self._game._roll)
            self._game._end_turn.active_color()
            
        # If the position is a property, check if its owned
        elif player.return_space_type(currentspace) == property:
            
            # If the property is unknowed, ask if the player would like to buy
            if property.check_owned(self, currentspace) is False:
                player.ask_buy(self, currentspace)
                self._game._end_turn.active_color()
           
            # If owned, check who owns it
            else:
                # If current player owns it, do nothing
                if property.check_owner(currentspace) == self:
                    self._game._end_turn.active_color()
                
                # If the other player owns it, charge rent
                else:
                    player.charge_rent(self, currentspace)
                    self._game._end_turn.active_color()

        # If the space is income tax, charge them income tax            
        elif player.return_space_type(currentspace) == incometax:
            player.pay(self, 75)
            self._game._end_turn.active_color()
        # If the space is a corner space, do nothing specific
        elif player.return_space_type(currentspace) == corner_space:
            self._game._end_turn.active_color()
        # If the space is community chest, choose a card
        elif player.return_space_type(currentspace) == communitychest:
            communitychest.choose(self._game._spots[self._position])
           
            self._game._end_turn.active_color()
        # If the space is chace, choose a card
        elif player.return_space_type(currentspace) == chance:
            chance.choose(self._game._spots[self._position])
           
            self._game._end_turn.active_color()
   
    def set_info(self, information):
        ''' Sets the player info to the information provided '''
        
        self._info = information
    
    def return_space_type(self):
        ''' Returns the type of space landed on '''
        
        return type(self)
    
    def balance(self):
        ''' Returns the balance of the player '''
        
        return self._balance
    
    def position(self):
        ''' Returns the player's position '''
        
        return self._position
    
    def pay(self, amount):
        ''' Player pays amount given and updates balance '''
        
        self._balance = player.balance(self) - amount
        if self._balance < 0:
            self._balance = 0
        self._info.update_balance()
    
    def receive(self, amount):
        ''' Player receives amount given and updates balance '''
        
        self._balance += amount
        self._info.update_balance()
    def ask_buy(self, prop):
        ''' Runs a window that asks the player if they want to buy property '''
        
        self._prop = prop
        player.disable(self)
        buy_window(self, self._win, 275, 125, (250, 385), prop)

    def decision_made(self):
        ''' Handles a decision on purchasing a property'''
        
        # If the player purchases the property, have them pay for it and
        # make them the owner
        
        if self._decisionmade == True:
            player.pay(self, property.return_price(self._prop))
            player.make_owned(self, self._prop)
            self._info.update_balance()
            self._prop.make_owner_player(self._prop, self)
            cat_prop = property.return_category(self._prop)
            self._propsowned[cat_prop].append(self._prop)
            
            # Check if the player now has a monopoly 
            player.check_monopoly(self, self._prop)
            
            # Update the player info section with the purchase
            info.info_properties(self, property.check_idnum(self._prop), 
                                 self._idnum)

            player.enable(self)

            # Marks the property with a marker of the owner's color
            player_marker(self._win, 5, property.return_center(self._prop), 
                          player.return_color(self))

        elif self._decisionmade == False:
            player.enable(self)

    def enable(self):
        ''' Returns that the property waas purchased '''
        
        self._decisionmade = True
        return self._decisionmade

    def disable(self):
        ''' Returns that the property was not purchased '''
        
        self._decisionmade = False
        return self._decisionmade

    def return_decisionmade(self):
        ''' Returns what the decision was '''
        
        return self._decisionmade

    def make_owned(self, prop):
        ''' Makes the player the property's owner '''
        
        property.make_owned(self, prop)

    def decision(self, decision):
        ''' Returns what the decision is if a decision is made '''
        
        if decision:
            self._decisionmade = True
        else:
            self._decisionmade = False
        self.decision_made()

    def charge_rent(self, prop):
        ''' Charges the player rent '''
        
        # If the property is in a monopoly, charge 10x rent
        if property.check_monopoly(prop) == True:
            player.pay(self, property.return_rent(prop) * 10)
            player.receive(property.check_owner(prop), 
                           property.return_rent(prop) * 10)
        
        # Otherwise, charge the player normal rent
        else:
            player.pay(self, property.return_rent(prop))
            player.receive(property.check_owner(prop), 
                           property.return_rent(prop))

        # Report what the player paid in rent
        self._game._note = Text(self._win, "You paid " +
                                str(player.name(self._game._otherplayer)) +
                                " $" + str(player.new_rent(prop)) +
                                " in rent!", 16, (250, 350))
        self._game._note.set_depth(3)
        self._game._notebox.set_depth(5)
        self._win.add(self._game._note)
        self._win.add(self._game._notebox)
   
    def return_color(self):
        ''' Returns the player's color '''
        return self._color
    
    def remove_win(self):
        ''' Removes the rent note from the window '''
        self._win.remove(self._note)
        self._win.remove(self._notebox)
    
    def check_monopoly(self, prop):
        ''' Checks if the player has a monopoly '''

        if property.return_category(self._prop) == 0 or 8 or 10:
            if len(self._propsowned[property.return_category(prop)]) == 2:
                for props in self._propsowned[property.return_category(prop)]:
                    props._monopoly = True

        if property.return_category(self._prop) == 1 or 2 or 3 or 4 or 5 or 6 \
                or 7:

            if len(self._propsowned[property.return_category(prop)]) == 3:
                for props in self._propsowned[property.return_category(prop)]:
                    props._monopoly = True

        if property.return_category(self._prop) == 9:
            if len(self._propsowned[10]) == 4:
                for props in self._propsowned[property.return_category(prop)]:
                    props._monopoly = True

    def new_rent(prop):
        ''' If theres a monopoly, returns the rent with a monopoly '''
        if property.check_monopoly(prop) is True:
            return property.return_rent(prop) * 10
        else:
            return property.return_rent(prop)

    def name(self):
        ''' Returns the name of the player '''

        return str(self._name)

class buy_window():
    ''' Defines the attributes and functions of the buy window '''

    def __init__(self, player, win, width, height, center, propert):
        ''' Initializes the buy window '''

        EventHandler.__init__(self)
        self._win = win
        self._player = player
        self._choicemade = None
        self._textbox = Rectangle(self._win, width, height, center)
        self._textbox.set_fill_color('burlywood')
        self._win.add(self._textbox)
        self._textbox.set_depth(5)

        # Asks if the player wants to buy the property
        self._ask = Text(self._win, "Buy " + str(property.name(propert)) +
                         " for $" + str(property.return_price(propert)) +
                         "?", 12, (250, 350))
        self._ask.set_depth(1)
        self._win.add(self._ask)

        # Initializes the buy button with the buy window
        self._buyButton = buy_button(self, win, width, height, center, player)

        # Initializes the pass button with the buy window
        self._passButton = pass_button(self, win, width, height, center,
                                       player)

    def remove_all(self):
        ''' Removes all items from the buy window '''
        self._buyButton.remove_button()
        self._passButton.remove_button()
        self._win.remove(self._textbox)
        self._win.remove(self._ask)


class buy_button(EventHandler):
    ''' Defines the attributes and functions of the buy button '''

    def __init__(self, parent, win, width, height, center, player):
        ''' Initializes the buy button '''

        self._win = win
        self._parent = parent
        self._player = player
        self._buy_button = Rectangle(self._win, width // 3, height // 3,
                                     (center[0] - 50, center[1]))
        self._buy_button.set_depth(2)
        self._buy_text = Text(win, "Buy", 16, (center[0] - 50, center[1]))
        self._buy_text.set_depth(1)
        self._win.add(self._buy_button)
        self._win.add(self._buy_text)
        EventHandler.__init__(self)
        self._buy_button.add_handler(self)
        self._buy_text.add_handler(self)

    def handle_mouse_release(self, win):
        ''' If clicked, return buy as decision '''
        self._player.decision(True)
        self._parent.remove_all()

    def remove_button(self):
        ''' Removes the button '''
        self._win.remove(self._buy_button)
        self._win.remove(self._buy_text)


class pass_button(EventHandler):
    ''' Defines the attributes and functions of the pass button '''

    def __init__(self, parent, win, width, height, center, player):
        ''' Intializes the pass button '''

        self._win = win
        self._parent = parent
        self._player = player
        self._pass_button = Rectangle(self._win, width // 3, height // 3,
                                      (center[0] + 50, center[1]))
        self._pass_button.set_depth(2)
        self._pass_text = Text(self._win, "Pass", 16, (center[0] + 50,
                               center[1]))
        self._pass_text.set_depth(1)
        self._win.add(self._pass_button)
        self._win.add(self._pass_text)
        EventHandler.__init__(self)
        self._pass_button.add_handler(self)
        self._pass_text.add_handler(self)

    def handle_mouse_release(self, win):
        ''' If clicked, return the decision was pass '''

        self._player.decision(False)
        self._parent.remove_all()

    def remove_button(self):
        ''' Removes the pass button '''

        self._win.remove(self._pass_button)
        self._win.remove(self._pass_text)


class player_marker(object):
    ''' Defines the attributes of a player marker '''

    def __init__(self, win, radius, center, color):
        ''' Intializes the player marker '''

        self._win = win
        self._radius = radius
        self._center = center
        marker = Circle(win, radius, center)
        marker.set_fill_color(color)
        marker.set_depth(4)
        self._win.add(marker)


class info(EventHandler):
    ''' Defines the attributes and functions of the player info section '''

    def __init__(self, win, player, center, width, height, name):
        ''' Intializes the player info section '''
        EventHandler.__init__(self)
        self._center = center
        self._win = win
        self._width = width
        self._height = height
        self._player = player
        self._curbal = self._player.balance()
        self._playername = Text(win, name + ':', 16, center)
        self._balance_indicator = Text(win, 'Balance:', 12, (center[0] - 30,
                                       center[1] + 25))
        self._currentbalance = Text(win, '$' + str(self._curbal), 12,
                                    (center[0] + 30, center[1] + 25))
        self._property_indicator = Text(win, 'Properties:', 14,
                                        (center[0], center[1] + 50))
        self._property_space = Rectangle(win, width, height, (center[0],
                                         center[1] + 140))
        self._property_space.set_depth(10)
        self._currentbalance.add_handler(self)
        win.add(self._playername)
        win.add(self._balance_indicator)
        win.add(self._currentbalance)
        win.add(self._property_indicator)
        win.add(self._property_space)

    def update_balance(self):
        ''' Updates the player's balance '''

        self._curbal = self._player.balance()
        self._currentbalance.set_text('$' + str(self._curbal))

    def info_properties(self, idnum, playernum):
        ''' Adds the representation of a purchased property to
            the properties part of the player info section '''

        # If player 1, add to player 1's section
        if playernum == 1:
            if idnum == 1:
                medave = Rectangle(self._win, 10, 15, (590, 135))
                medave.set_fill_color('Purple')
                medave.set_depth(4)
                self._win.add(medave)
            if idnum == 2:
                baltic = Rectangle(self._win, 10, 15, (630, 135))
                baltic.set_fill_color('Purple')
                baltic.set_depth(3)
                self._win.add(baltic)
            if idnum == 3:
                oriave = Rectangle(self._win, 10, 15, (590, 160))
                oriave.set_fill_color('light blue')
                oriave.set_depth(4)
                self._win.add(oriave)
            if idnum == 4:
                verave = Rectangle(self._win, 10, 15, (630, 160))
                verave.set_fill_color('light blue')
                verave.set_depth(4)
                self._win.add(verave)
            if idnum == 5:
                connave = Rectangle(self._win, 10, 15, (670, 160))
                connave.set_fill_color('light blue')
                connave.set_depth(4)
                self._win.add(connave)
            if idnum == 6:
                stchar = Rectangle(self._win, 10, 15, (590, 185))
                stchar.set_fill_color('Pink')
                stchar.set_depth(4)
                self._win.add(stchar)
            if idnum == 7:
                statesave = Rectangle(self._win, 10, 15, (630, 185))
                statesave.set_fill_color('Pink')
                statesave.set_depth(4)
                self._win.add(statesave)
            if idnum == 8:
                virginiaave = Rectangle(self._win, 10, 15, (670, 185))
                virginiaave.set_fill_color('Pink')
                virginiaave.set_depth(4)
                self._win.add(virginiaave)
            if idnum == 9:
                stjames = Rectangle(self._win, 10, 15, (590, 210))
                stjames.set_fill_color('orange')
                stjames.set_depth(4)
                self._win.add(stjames)
            if idnum == 10:
                tennave = Rectangle(self._win, 10, 15, (630, 210))
                tennave.set_fill_color('orange')
                tennave.set_depth(4)
                self._win.add(tennave)
            if idnum == 11:
                nyave = Rectangle(self._win, 10, 15, (670, 210))
                nyave.set_fill_color('orange')
                nyave.set_depth(4)
                self._win.add(nyave)
            if idnum == 12:
                kentuckyave = Rectangle(self._win, 10, 15, (590, 235))
                kentuckyave.set_fill_color('red')
                kentuckyave.set_depth(4)
                self._win.add(kentuckyave)
            if idnum == 13:
                ventnorave = Rectangle(self._win, 10, 15, (630, 235))
                ventnorave.set_fill_color('red')
                ventnorave.set_depth(4)
                self._win.add(ventnorave)
            if idnum == 14:
                margarave = Rectangle(self._win, 10, 15, (670, 235))
                margarave.set_fill_color('red')
                margarave.set_depth(4)
                self._win.add(margarave)
            if idnum == 15:
                atlanticave = Rectangle(self._win, 10, 15, (720, 135))
                atlanticave.set_fill_color('yellow')
                atlanticave.set_depth(4)
                self._win.add(atlanticave)
            if idnum == 16:
                ventnorave = Rectangle(self._win, 10, 15, (760, 135))
                ventnorave.set_fill_color('yellow')
                ventnorave.set_depth(4)
                self._win.add(ventnorave)
            if idnum == 17:
                margar = Rectangle(self._win, 10, 15, (800, 135))
                margar.set_fill_color('yellow')
                margar.set_depth(4)
                self._win.add(margar)
            if idnum == 18:
                pacificave = Rectangle(self._win, 10, 15, (720, 160))
                pacificave.set_fill_color('green')
                pacificave.set_depth(4)
                self._win.add(pacificave)
            if idnum == 19:
                northcaroave = Rectangle(self._win, 10, 15, (760, 160))
                northcaroave.set_fill_color('green')
                northcaroave.set_depth(4)
                self._win.add(northcaroave)
            if idnum == 20:
                pennave = Rectangle(self._win, 10, 15, (800, 160))
                pennave.set_fill_color('green')
                pennave.set_depth(4)
                self._win.add(pennave)
            if idnum == 21:
                parkplace = Rectangle(self._win, 10, 15, (720, 185))
                parkplace.set_fill_color('blue')
                parkplace.set_depth(4)
                self._win.add(parkplace)
            if idnum == 22:
                boardwalk = Rectangle(self._win, 10, 15, (760, 185))
                boardwalk.set_fill_color('blue')
                boardwalk.set_depth(4)
                self._win.add(boardwalk)
            if idnum == 23:
                readingrail = Rectangle(self._win, 10, 15, (720, 210))
                readingrail.set_fill_color('black')
                readingrail.set_depth(4)
                self._win.add(readingrail)
            if idnum == 24:
                pennrail = Rectangle(self._win, 10, 15, (760, 210))
                pennrail.set_fill_color('black')
                pennrail.set_depth(4)
                self._win.add(pennrail)
            if idnum == 25:
                borail = Rectangle(self._win, 10, 15, (800, 210))
                borail.set_fill_color('black')
                borail.set_depth(4)
                self._win.add(borail)
            if idnum == 26:
                shortline = Rectangle(self._win, 10, 15, (840, 210))
                shortline.set_fill_color('black')
                shortline.set_depth(4)
                self._win.add(shortline)
            if idnum == 27:
                electriccomp = Rectangle(self._win, 10, 15, (720, 235))
                electriccomp.set_fill_color('black')
                electriccomp.set_depth(4)
                self._win.add(electriccomp)
            if idnum == 28:
                waterworks = Rectangle(self._win, 10, 15, (760, 235))
                waterworks.set_fill_color('black')
                waterworks.set_depth(4)
                self._win.add(waterworks)

        # If player 2, add to player 2's section
        elif playernum == 2:
            if idnum == 1:
                medave = Rectangle(self._win, 10, 15, (590, 385))
                medave.set_fill_color('Purple')
                medave.set_depth(4)
                self._win.add(medave)
            if idnum == 2:
                baltic = Rectangle(self._win, 10, 15, (630, 385))
                baltic.set_fill_color('Purple')
                baltic.set_depth(3)
                self._win.add(baltic)
            if idnum == 3:
                oriave = Rectangle(self._win, 10, 15, (590, 410))
                oriave.set_fill_color('light blue')
                oriave.set_depth(4)
                self._win.add(oriave)
            if idnum == 4:
                verave = Rectangle(self._win, 10, 15, (630, 410))
                verave.set_fill_color('light blue')
                verave.set_depth(4)
                self._win.add(verave)
            if idnum == 5:
                connave = Rectangle(self._win, 10, 15, (670, 410))
                connave.set_fill_color('light blue')
                connave.set_depth(4)
                self._win.add(connave)
            if idnum == 6:
                stchar = Rectangle(self._win, 10, 15, (590, 435))
                stchar.set_fill_color('Pink')
                stchar.set_depth(4)
                self._win.add(stchar)
            if idnum == 7:
                statesave = Rectangle(self._win, 10, 15, (630, 435))
                statesave.set_fill_color('Pink')
                statesave.set_depth(4)
                self._win.add(statesave)
            if idnum == 8:
                virginiaave = Rectangle(self._win, 10, 15, (670, 435))
                virginiaave.set_fill_color('Pink')
                virginiaave.set_depth(4)
                self._win.add(virginiaave)
            if idnum == 9:
                stjames = Rectangle(self._win, 10, 15, (590, 460))
                stjames.set_fill_color('orange')
                stjames.set_depth(4)
                self._win.add(stjames)
            if idnum == 10:
                tennave = Rectangle(self._win, 10, 15, (630, 460))
                tennave.set_fill_color('orange')
                tennave.set_depth(4)
                self._win.add(tennave)
            if idnum == 11:
                nyave = Rectangle(self._win, 10, 15, (670, 460))
                nyave.set_fill_color('orange')
                nyave.set_depth(4)
                self._win.add(nyave)
            if idnum == 12:
                kentuckyave = Rectangle(self._win, 10, 15, (590, 485))
                kentuckyave.set_fill_color('red')
                kentuckyave.set_depth(4)
                self._win.add(kentuckyave)
            if idnum == 13:
                ventnorave = Rectangle(self._win, 10, 15, (630, 485))
                ventnorave.set_fill_color('red')
                ventnorave.set_depth(4)
                self._win.add(ventnorave)
            if idnum == 14:
                margarave = Rectangle(self._win, 10, 15, (670, 485))
                margarave.set_fill_color('red')
                margarave.set_depth(4)
                self._win.add(margarave)
            if idnum == 15:
                atlanticave = Rectangle(self._win, 10, 15, (720, 385))
                atlanticave.set_fill_color('yellow')
                atlanticave.set_depth(4)
                self._win.add(atlanticave)
            if idnum == 16:
                ventnorave = Rectangle(self._win, 10, 15, (760, 385))
                ventnorave.set_fill_color('yellow')
                ventnorave.set_depth(4)
                self._win.add(ventnorave)
            if idnum == 17:
                margar = Rectangle(self._win, 10, 15, (800, 385))
                margar.set_fill_color('yellow')
                margar.set_depth(4)
                self._win.add(margar)
            if idnum == 18:
                pacificave = Rectangle(self._win, 10, 15, (720, 410))
                pacificave.set_fill_color('green')
                pacificave.set_depth(4)
                self._win.add(pacificave)
            if idnum == 19:
                northcaroave = Rectangle(self._win, 10, 15, (760, 410))
                northcaroave.set_fill_color('green')
                northcaroave.set_depth(4)
                self._win.add(northcaroave)
            if idnum == 20:
                pennave = Rectangle(self._win, 10, 15, (800, 410))
                pennave.set_fill_color('green')
                pennave.set_depth(4)
                self._win.add(pennave)
            if idnum == 21:
                parkplace = Rectangle(self._win, 10, 15, (720, 435))
                parkplace.set_fill_color('blue')
                parkplace.set_depth(4)
                self._win.add(parkplace)
            if idnum == 22:
                boardwalk = Rectangle(self._win, 10, 15, (760, 435))
                boardwalk.set_fill_color('blue')
                boardwalk.set_depth(4)
                self._win.add(boardwalk)
            if idnum == 23:
                readingrail = Rectangle(self._win, 10, 15, (720, 460))
                readingrail.set_fill_color('black')
                readingrail.set_depth(4)
                self._win.add(readingrail)
            if idnum == 24:
                pennrail = Rectangle(self._win, 10, 15, (760, 460))
                pennrail.set_fill_color('black')
                pennrail.set_depth(4)
                self._win.add(pennrail)
            if idnum == 25:
                borail = Rectangle(self._win, 10, 15, (800, 460))
                borail.set_fill_color('black')
                borail.set_depth(4)
                self._win.add(borail)
            if idnum == 26:
                shortline = Rectangle(self._win, 10, 15, (840, 460))
                shortline.set_fill_color('black')
                shortline.set_depth(4)
                self._win.add(shortline)
            if idnum == 27:
                electriccomp = Rectangle(self._win, 10, 15, (720, 485))
                electriccomp.set_fill_color('black')
                electriccomp.set_depth(4)
                self._win.add(electriccomp)
            if idnum == 28:
                waterworks = Rectangle(self._win, 10, 15, (760, 485))
                waterworks.set_fill_color('black')
                waterworks.set_depth(4)
                self._win.add(waterworks)


def program(win):
    ''' Starts the game and defines the window dimensions '''

    win.set_width(1000)
    win.set_height(550)
    Game(win)

    # for dice


def main():
    StartGraphicsSystem(program)


if __name__ == "__main__":
    main()
