#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 20:32:06 2019

@author: ajw1e16

This class will contain all history about a game, easy for every player to see.
"""

import utilityFunctions as ut

class Broadcast(object):
    """
    A public class that contains all information available to all players.
    Within this class, players can see the up card of the dealer, and any 
    counts that they want to use. 
    """
    
    def __init__(self):
        self.shoeHistory = []
        self.hiLoCount = 0
        self.dealersTotal = 0
        
    def reset(self):
        self.shoeHistory = []
        self.hiLoCount = 0
        self.dealersTotal = 0
    
    @property
    def dealersTotal(self):
        return self.__dealersTotal
    
    @dealersTotal.setter
    def dealersTotal(self, tot):
        self.__dealersTotal = tot
    
    def updateHiLo(self, card):
        val = ut.getNumber(card)
        if val > 9:
            self.hiLoCount -= 1
        elif val < 7:
            self.hiLoCount += 1
        print(self.hiLoCount)
    
    def append(self, card):
        """
        Append a card to the shoe history. All count update functions are 
        called within this method.
        
        Parameters
        ----------
        card : str
            Card to add to the history
        """
        self.shoeHistory.append(card)
        
        # Here we change the count according to the system we want to lose
        self.updateHiLo(card)
