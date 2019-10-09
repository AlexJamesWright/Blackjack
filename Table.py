#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 18:42:56 2019

@author: ajw1e16

Table class
"""

from DeckAndShoe import Shoe
from HandSeatAndDealer import Seat, Dealer

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
        