#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 18:43:23 2019

@author: ajw1e16
"""

class Hand(object):
    
    cards = []
    bust = False
    
    def __init__(self, bet, ):
        self.bet = bet
        
    def split(self):
        pass
    
    def doubleDown(self):
        pass
    
    def newHit(self):
        pass
    
        
class Seat(object):
    
    hands = []
    bet = []
    bust = []
    
    def newBet(self, size):
        self.hand = None 
        self.bet = size
    
class Dealer(object):
    
    hand = []
