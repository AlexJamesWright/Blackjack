#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 18:43:23 2019

@author: ajw1e16
"""
import utilityFunctions as ut

class Hand(object):
    """
    A single hand, i.e. intially only two cards. Players may have multiple
    hands in a single game.
    
    Parameters
    ----------
    
    bet : int
        The size of the bet for this hand
        
    """
    
    def __init__(self, bet=None):
        self.stuck = False
        self.cards = []
        self.bet = bet
        
    def addCard(self, card):
        self.cards.append(card)
        
    def doubleDown(self, shoe):
        # Ahhhh, how to change the bet size....
        if ut.canDoubleDown(self):
            self.bet *= 2
            self.hit(shoe)
            self.stick()
    
    def hit(self, shoe):
        self.addCard(shoe.nextCard())
    
    def stick(self):
        self.stuck = True
            
        
class Seat(object):
    """
    A physical seat. A seat can have multiple hands/bets, e.g. through 
    splitting, and a player may play on multiple seats.
    """
    
    def __init__(self):
        self.player = None
        self.hands = []
        
    def resetSeat(self):
        self.hands = []
    
    def newBet(self, bet):
        if bet <= self.player.bank:
            self.hands.append(Hand(bet))
            self.player.bank -= bet
        
    def addPlayer(self, player):
        self.player = player
        
        
class Dealer(object):
    
    # Convention, first card is shown
    def __init__(self):
        self.hand = Hand()
    
    def upCard(self):
        return self.hand.cards[0]
    
    def shouldHit(self, hand):
        if ut.getTotal(hand) <= 16:
            return True
        elif ut.getTotal(hand) == 17 and ut.isSoft(hand):
            return True
        else:
            return False
    
    def playHand(self, hand, shoe):
        while self.shouldHit(hand):
            hand.hit(shoe)
        hand.stick()


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
        self.bank = bank
        
    def playHand(self, hand, shoe=None):
        raise NotImplementedError('Need to implement rules for this player')
        
        
class Hitter(Player):
    """
    Always hit. ALways. 'Till bust.
    """
    def playHand(self, hand, shoe=None):
        while ut.isNotStuckOrBust(hand):
            # Always hit
            hand.hit(shoe)
        
    def wantsToSplit(self, hand):
        return True
    
    def wantsToDoubleDown(self, hand):
        return True
        
class Sticker(Player):
    """
    Always stick.
    """
    def playHand(self, hand, shoe=None):
        hand.stick()
