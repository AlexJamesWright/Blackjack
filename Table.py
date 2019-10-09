#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 18:42:56 2019

@author: ajw1e16

Table class
"""

from DeckAndShoe import Shoe
from HandSeatAndDealer import Seat, Dealer
import utilityFunctions as ut

class Table(object):
    """
    Physical table. Has seats, a dealer, and a shoe.
    
    Parameters
    ----------
    maxNumberOfSeats : int
        Maximum number of seats at the table.
    minBet : int
        Minimum bet size
    maxBet : int
        Maximum bet size
    """
    
    maxNumberOfSeats = 6
    
    def __init__(self, numberOfSeats=6, minBet=1, maxBet=100):
        self.dealer = Dealer()
        self.seats = []
        self.numberOfSeats = numberOfSeats
        self.newShoe()
        
        for i in range(self.numberOfSeats):
            if i < self.maxNumberOfSeats:
                self.newSeat()
        
    def newShoe(self):
        self.shoe = Shoe()
        
    def newSeat(self):
        self.seats.append(Seat())
        
    def playerActions(self):
        for seat in self.seats:
            for hand in seat.hands:
                # Start of hand, deal with doubling and splitting firest
                if len(hand.cards) == 1:
                    # Player must have split so take another card
                    print("Dealing second card after split")
                    hand.cards.append(self.shoe.nextCard())
                if len(seat.hands) == 1 and ut.canSplit(hand) and seat.player.wantsToSplit(hand) and seat.player.bank >= hand.bet:
                    print("Splitting hand")
                    seat.newBet(hand.bet)
                    seat.hands[1].cards.append(hand.cards[1])
                    hand.cards.remove(hand.cards[1])
                    hand.cards.append(self.shoe.nextCard())
                if ut.canDoubleDown(hand) and seat.player.wantsToDoubleDown(hand):
                    print("Doubling down")
                    hand.doubleDown(self.shoe)
                while not hand.stuck:
                    print("Playing hand normally")
                    seat.player.playHand(hand)
        