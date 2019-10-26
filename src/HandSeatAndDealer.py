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

