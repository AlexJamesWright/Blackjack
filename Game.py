"""
Script contains the API for blackjack 21.

This class contains the main methods for playing a game of blackjack. We will
try to replicate how it is played in casinos.
"""

from Table import Table
from HandSeatAndDealer import Mug, Sticker, Seat
import utilityFunctions as ut

class Game(object):
    """
    Overarching class describing the game. Contains the table (with its seats, 
    shoe etc), and contains methods for the game to be played.
    
    Parameters
    ----------
    numberOfSeats : int
        Number of seats at table
        
    randomPen : bool
        Do we want to randomly penetrate the deck?
        
    penPosition : int
        Position to penetrate the deck
    """
    
    def __init__(self, numberOfSeats=6, randomPen=False, penPosition=250):
        
        self.table = Table(numberOfSeats=numberOfSeats)
        self.penPosition = penPosition
        
        
        # Penetrate the deck
        if not randomPen:
            self.table.shoe.penetrate(penPosition)
        else:
            raise NotImplementedError
        
        
    def addPlayerToSeat(self, player, seatNo):
        """
        Add a given player to a specified seat.
        
        Parameters
        ----------
        player : Player object
            Player to add to the seat
        
        seatNo : int
            Seat number player wants to sit at (index from 0)
        """
        if seatNo < self.table.numberOfSeats:
            self.table.seats[seatNo].addPlayer(player)
            
    def removePlayerFromSeat(self, seatNo):
        """
        Removes a player from a seat.
        
        Parameters
        ----------
        seatNo : int
            Seat number to remove player from (index from 0)
        """
        if seatNo < self.seats:
            self.table.seats[seatNo] = Seat()
        
    def play(self):
        """
        Play blackjack until the end of the shoe.
        """
#        print("Forcing the shoe for the player")
#        self.table.shoe.cards = 'Ah'
#        self.table.shoe.cards = 'Ac'
        while None in self.table.shoe.cards:
            self.nextRound()
            
            # Force only one round for now
#            break
    
    
    def nextRound(self):
        """
        Play the next round of blakjack
        """
        # Need to initialise some new bets/hands
        self.table.cleanSeats()
        self.table.getBets()
        self.table.deal()
        self.table.playerActions()
        self.table.dealerAction()
        self.table.settleUp()
        self.showHands()
        
        
    ###########################################################################
    #### Useful functions that dont add to setting up the game or gameplay       
    ###########################################################################
    
    def showHands(self):
        """
        Print the current hand at the table.
        """
        dstr = ''
        for n, card in enumerate(self.table.dealer.hand.cards):
            dstr += '{:3}'.format(card)
            if n < len(self.table.dealer.hand.cards)-1:
                dstr += ' '
        print("Dealer   :   {:2d} [{}]".format(ut.getTotal(self.table.dealer.hand), dstr))        
        for s, seat in enumerate(self.table.seats):
            for h, hand in enumerate(seat.hands):
                hstr = ''
                for n, card in enumerate(hand.cards):
                    hstr += '{:3}'.format(card)
                    if n < len(hand.cards)-1:
                        hstr += ' '
                print("Seat {}.{} :   {:2d} [{}]".format(s, h, ut.getTotal(hand), hstr))
        
        for player in self.getPlayers():
            print("{}: bank = {}".format(player.__name__, player.bank))
                
                
    def getPlayers(self):
        """
        Get all the players current at the table.
        
        Returns
        -------
        player : list
            A list of all Player objects at the table
        
        """
        players = []
        for seat in self.table.seats:
            if seat.player not in players and seat.player is not None:
                players.append(seat.player)
        return players
    
        
        
if __name__ == '__main__':
    
    # Lets create two players and start a game
    player1 = Mug(1000)
    player2 = Sticker(8000)
    
    game = Game()
#    game.addPlayerToSeat(player1, 0)
    game.addPlayerToSeat(player2, 3)
    game.play()
    game.showHands()