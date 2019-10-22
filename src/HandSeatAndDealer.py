#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 18:43:23 2019

@author: ajw1e16
"""
import utilityFunctions as ut
import numpy as np

class Hand(object):
    """
    A single hand, i.e. intially only two cards. Players may have multiple
    hands in a single game.
    
    Parameters
    ----------
    
    bet : float
        The size of the bet for this hand
        
    """
    
    def __init__(self, bet=None):
        self.stuck = False
        self.cards = []
        self.bet = bet
        
    def addCard(self, card):
        """
        Add a card to this hand.
        
        Parameters
        ----------
        card : str
            String defining the card to add
        """
        self.cards.append(card)
        
    def doubleDown(self, shoe):
        """
        Double down and only take one more card.
        
        Parameters
        ----------
        shoe : Shoe object
            The shoe
        """
        self.bet *= 2
        self.hit(shoe)
        self.stick()
    
    def hit(self, shoe):
        """
        Take another card.
        
        Parameters
        ----------
        shoe : Shoe object
            The shoe
        """
        self.addCard(shoe.nextCard())
    
    def stick(self):
        """
        Stick.
        """
        self.stuck = True
            
        
class Seat(object):
    """
    A physical seat. A seat can have multiple hands/bets, e.g. through 
    splitting, and a player may play on multiple seats. Only one player per 
    seat.
    """
    
    def __init__(self):
        self.player = None
        self.hands = []
        
    def resetSeat(self):
        """
        Delete the hand at this seat.
        """
        self.hands = []
    
    def newBet(self, bet):
        """
        Place a new bet at this seat.
        
        bet : float
            Bet size of the new bet
        """
        if bet <= self.player.bank and bet > 0:
            self.hands.append(Hand(bet))
            self.player.roundBetting += bet
        
    def addPlayer(self, player):
        """
        Add a player to this seat
        
        Parameters
        ----------
        player : player object
            The player to add
        """
        self.player = player
        
        
class Dealer(object):
    """
    This is the dealer object, which contains the dealers cards (hand) and the
    conventional playing strategy. It also contains some useful functions such 
    as Dealer.total() to get the value of the dealers up-card. By convention,
    the dealer shows their first card. The dealer hits soft 17.
    
    """
    
    def __init__(self):
        self.hand = Hand()
    
    def upCard(self):
        """
        Show the dealers up-card
        
        Returns
        -------
        card : str
            This string defining the dealers up-card
        """
        return self.hand.cards[0]
    
    def shouldHit(self, hand):
        """
        Should the dealer be hitting their current hand? Dealer hits soft 17.
        
        Returns
        -------
        hit : bool
            Should the dealer hit?
        """
        if ut.getTotal(hand) <= 16:
            return True
        elif ut.getTotal(hand) == 17 and ut.isSoft(hand):
            return True
        else:
            return False
    
    def total(self):
        """
        Get the dealer's total that players can see. I.e. the up-card
        
        Returns 
        -------
        tot : int
            The value of the dealers up card
        """
        return ut.getNumber(self.hand.cards[0])
    
    def fullTotal(self):
        """
        Get the dealer's full total. I.e. all cards
        
        Returns 
        -------
        tot : int
            The value of the dealers up card
        """
        return ut.getTotal(self.hand)
        
    def resetHand(self):
        """
        Delete the dealer's hand.
        """
        self.hand = Hand()
    
    def playHand(self, hand, shoe):
        """
        Play the hand.
        """
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
        
        self.bankHistory = [bank]
        self.bank = bank
        self.roundBetting = 0
        self.payout = 0
        
    @property
    def bank(self):
        return self.__bank
    
    @bank.setter
    def bank(self, bank):
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
        self.bank += self.payout - self.roundBetting
        self.payout = 0
        self.roundBetting = 0
        
    def wantsToSplit(self, hand):
        """
        Does this player want to split?
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
    Always split, double or hit
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
    Always split, double, and hit under 19
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
