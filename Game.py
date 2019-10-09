"""
Script contains the API for blackjack 21.

This class contains the main methods for playing a game of blackjack. We will
try to replicate how it is played in casinos.
"""

from Table import Table
from HandSeatAndDealer import Hitter, Sticker, Seat
import utilityFunctions as ut

class Game(object):
    """
    Overarching class describing the game. Contains the table (with its seats, 
    shoe etc), and contains methods for the game to be played.
    
    numberOfSeats : int
        Number of seats
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
        if seatNo < self.table.numberOfSeats:
            self.table.seats[seatNo].addPlayer(player)
            
    def removePlayerFromSeat(self, player, seatNo):
        if seatNo < self.seats:
            self.table.seats[seatNo] = Seat()
        
    def play(self):
        # Play the game until the end of the shoe
#        print("Forcing the shoe for the player")
#        self.table.shoe.cards[0] = 'Ah'
#        self.table.shoe.cards[2] = 'Ac'
        while None in self.table.shoe.cards:
            self.nextRound()
            
            # Force only one round for now
            break
    
    def cleanSeats(self):
        # Clear all seats of their hands
        for seat in self.table.seats:
            seat.resetSeat()
    
    def getBets(self):
        # Get the bets from the seats
        for i, seat in enumerate(self.table.seats):
            if seat.player:
                # For now just hard code a few hands
                seat.newBet(i*10) 
        
    def deal(self):
        # Hand out two cards to each player and the dealer
        # First card
        for seat in self.table.seats:
            if seat.player:
                for hand in seat.hands:
                    hand.addCard(self.table.shoe.nextCard())
        # Dealers first
        self.table.dealer.hand.addCard(self.table.shoe.nextCard())
        # Second card
        for seat in self.table.seats:
            if seat.player:
                for hand in seat.hands:
                    hand.addCard(self.table.shoe.nextCard())
        # Dealers second
        self.table.dealer.hand.addCard(self.table.shoe.nextCard())

    def seatAction(self):
        """
        All seats have their go until they either stick or bust.
        """
        
        #### I think that the seat action should be determined in the 
        # Table class, as this can pass the output of shoe.nextCard to any
        # hit/double functions returned by a players rules
    
        self.table.playerActions()
    
    def dealerAction(self):
        """
        Dealer plays until theys stick or bust.
        """
        
        self.table.dealer.playHand(self.table.dealer.hand, self.table.shoe)
    
    def settleUp(self):
        """
        Casino pays out winning hands.
        """
        pass
    
    def nextRound(self):
        # Need to initialise some new bets/hands
        self.cleanSeats()
        self.getBets()
        self.deal()
        self.seatAction()
        self.dealerAction()
        self.settleUp()
        
        
    ###########################################################################
    #### Useful functions that dont add to setting up the game or gameplay       
    ###########################################################################
    
    def showHands(self):
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
                
                
    
        
        
if __name__ == '__main__':
    
    # Lets create two players and start a game
    player1 = Hitter(1000)
    player2 = Sticker(8000)
    
    game = Game()
    game.addPlayerToSeat(player1, 0)
    game.play()
    game.showHands()