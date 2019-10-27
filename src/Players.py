#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 26 13:53:59 2019

@author: ajw1e16

Various blackjack players.
"""

import utilityFunctions as ut

class Player(object):
    """
    Base player. All other players will inherit from this with their own
    playing style.
    
    Parameters
    ----------
    
    bank : int
        Total money player is bringing to the table.
    """
    def __init__(self, bank=1000):
        
        # History of this players bank
        self.bankHistory = []
        
        # Current bank
        self.bank = bank
        
        # How much have we bet in this round
        self.roundBetting = 0
        
        # What is the payout in this round
        self.payout = 0
        
        # A view of the broadcast
        self.broadcast = None
        
    @property
    def bank(self):
        return self.__bank
    
    @bank.setter
    def bank(self, bank):
        """
        Update the player's bank. When setting the player's bank at the end of 
        a round, update the players bank history also.
        
        Parameters
        ----------
        bank : float
            The new bank
        """
        self.__bank = bank

        # Save to the history
        self.bankHistory.append(self.bank)
        
    @property
    def roundBetting(self):
        return self.__roundBetting
    
    @roundBetting.setter
    def roundBetting(self, amount):
        self.__roundBetting = amount
        
    @property
    def payout(self):
        return self.__payout
    
    @payout.setter
    def payout(self, amount):
        self.__payout = amount
        
    def settleRound(self):
        """
        After a round has ended, settle up outstanding bets.
        """
        self.bank += self.payout - self.roundBetting
        self.payout = 0
        self.roundBetting = 0
        
    def wantsToSplit(self, hand):
        """
        Does this player want to split? If this method has been called, Table 
        has already checked that 'hand' can be split.
        """
        raise NotImplementedError('Need to implement rules for this player: ', self.__class__)
        
    def wantsToDoubleDown(self, hand):
        """
        Does this player want to double down?
        """
        raise NotImplementedError('Need to implement rules for this player: ', self.__class__)
        
    def wantsToHit(self, hand, shoe):
        """
        Does this player want to hit?
        """
        raise NotImplementedError('Need to implement rules for this player: ', self.__class__)
        
    def getBet(self):
        """
        What size bet does this player want to make?
        """
        raise NotImplementedError('Need to implement getBet for this player: ', self.__class__)
        
        
class Mug(Player):
    """
    Always split, double or hit.
    """
    
    __name__ = 'Mug'
    
    def wantsToHit(self, hand):
        return True
        
    def wantsToSplit(self, hand):
        return True
    
    def wantsToDoubleDown(self, hand):
        return True
        
    def getBet(self):
        return 80
    
    
class Sticker(Player):
    """
    Always stick.
    """
    
    __name__ = 'Pussy'
    
    def wantsToSplit(self, hand):
        return False
    
    def wantsToDoubleDown(self, hand):
        return False
        
    def wantsToHit(self, hand):
        return False
    
    def getBet(self):
        return 80
    
    
class Risker(Player):
    """
    Always split, double, and hit under 19.
    """
    
    __name__ = 'Risker'
    
    def wantsToHit(self, hand):
        if ut.getTotal(hand) < 19:
            return True
        return False
        
    def wantsToSplit(self, hand):
        return True
    
    def wantsToDoubleDown(self, hand):
        if ut.getTotal(hand) < 12:
            return True
        return False
        
    def getBet(self):
        return 80


class BasicStrategist(Player):
    """
    Play basic strategy.
    """
    
    __name__ = "BasicStrategist"
    
    def wantsToSplit(self, hand):
        
        dealersTot = self.broadcast.dealersTotal
        
        # AA, 88
        if ut.handHas(hand, 11) or ut.handHas(hand, 8):
            return True
        # 99
        elif ut.handHas(hand, 9):
            if dealersTot == 7 or dealersTot > 9:
                return False
            else:
                return True
        # 77
        elif ut.handHas(hand, 7):
            if dealersTot < 8:
                return True
        # 66
        elif ut.handHas(hand, 6):
            if dealersTot < 7:
                return True
        # 44
        elif ut.handHas(hand, 4):
            if dealersTot == 5 or dealersTot == 6:
                return True
        # 33, 22
        elif ut.handHas(hand, 3) or ut.handHas(hand, 2):
            if dealersTot < 8:
                return True
        return False
            
    def wantsToDoubleDown(self, hand):
        tot = ut.getTotal(hand)
        dealersTot = self.broadcast.dealersTotal
        
        # A
        if tot == 11:
            if dealersTot != 11: 
                return True
        # 10
        elif tot == 10:
            if dealersTot < 10: 
                return True
        elif tot == 9:
            if dealersTot > 2 or dealersTot < 7:
                return True
        # Soft hands
        elif ut.isSoft(hand):
            # A7, A6
            if tot == 18 or tot == 17:
                if dealersTot > 2 or dealersTot < 7:
                    return True
            # A5, A4
            elif tot == 16 or tot == 15:
                if dealersTot > 3 or dealersTot < 7:
                    return True
            # A3, A2
            elif tot == 14 or tot == 13:
                if dealersTot > 4 or dealersTot < 7:
                    return True
        return False
                
    def wantsToHit(self, hand):
        tot = ut.getTotal(hand)
        dealersTot = self.broadcast.dealersTotal
        
        # First deal with soft hands
        if ut.isSoft(hand):
            if tot == 18 and dealersTot > 8:
                return True
            elif tot > 12 and tot < 18:
                return True
        # Total < 17
        if tot < 17:
            # Dealer shows > 6
            if dealersTot > 6:
                return True
            # Dealer shows < 6
            else:
                if tot == 12 and dealersTot < 4:
                    return True
                elif tot < 12:
                    return True
        return False
    
    def getBet(self):
        return 80
        

class Counter(BasicStrategist):
    
    __name__ = "Counter"
    
    def __init__(self, bank=1000, mult=5):
        super().__init__(bank)
        self.mult = mult
    
    def getBet(self):
        return max(int(self.broadcast.trueHiLoCount() - 2) * self.mult * 80, 0)
                
                
            
            
            
            
            
            
            
            
            
            
            
            
            
            
               
            
            
    
    
    
    
    