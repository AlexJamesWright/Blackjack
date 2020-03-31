#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 20 17:45:36 2019

@author: ajw1e16

Useful functions for interacting with the game.
"""

def getSuit(card):
    """
    Get the suit of a card. 
    'h' = hearts
    'c' = clubs
    'd' = diamons 
    's' = spades
    
    Parameters 
    ----------
    card : str
        The card we are looking at
    Returns 
    -------
    suit : str
        The suit of the card 
    """
    return card[-1]

def getNumber(card):
    """
    Get the value of a card.
    
    Parameters 
    ----------
    card : str
        The card we are looking at
        
    Returns 
    -------
    val : int
        The value of the card
    """
    num = card[:-1]
    try:
        return int(num)
    except ValueError:
        if num == 'A':
            return 11
        else:
            return 10

def getTotal(hand):
    """
    Get the total value of a hand
    
    Parameters 
    ----------
    hand : Hand object
        The hand we are looking at
        
    Returns 
    -------
    tot : int
        The total value of the hand
    """
    tot = 0
    for card in hand.cards:
        tot += getNumber(card)
    if tot > 21 and isSoft(hand):
        tot -= 10
    return tot

def isNotBust(hand):
    """
    Is this hand not bust?
    
    Parameters 
    ----------
    hand : Hand object
        The hand we are looking at
        
    Returns
    -------
    nb : bool
        not bust
    """
    return getTotal(hand) <= 21

def isBust(hand):
    """
    Is this hand bust?
    
    Parameters 
    ----------
    hand : Hand object
        The hand we are looking at
        
    Returns
    -------
    b : bool
        bust
    """
    return getTotal(hand) > 21

def canBePlayed(hand):
    """
    Can this hand be played? Checks that hand is not bust, and less than 21.
    If hand is 21, the hand is automatically stuck.
    
    Parameters 
    ----------
    hand : Hand object
        The hand we are looking at
        
    Returns
    -------
    playable : bool
        Is this hand playable?
    """
    if hand.stuck:
        return False
    elif getTotal(hand) <= 20:
        return True
    # Either the player has 21 or bust, so auto-stick
    hand.stick()
    return False

def isSoft(hand):
    """
    Is this hand soft?
    
    Parameters 
    ----------
    hand : Hand object
        The hand we are looking at
        
    Returns
    -------
    soft : bool
        Is this hand soft?
    """
    for card in hand.cards:
        if getNumber(card) == 11:
            return True
    return False

def canSplit(hand):
    """
    Is this hand splittable (in terms of cards, not bank)?
    
    Parameters 
    ----------
    hand : Hand object
        The hand we are looking at
        
    Returns
    -------
    soft : bool
        Is this hand splittable?
    """
    if len(hand.cards) == 2 and \
                    (getNumber(hand.cards[0]) == getNumber(hand.cards[1])):
        return True
    return False

def canDoubleDown(hand):
    """
    Is this hand doubleable (in terms of cards, not bank)?
    
    Parameters 
    ----------
    hand : Hand object
        The hand we are looking at
        
    Returns
    -------
    soft : bool
        Is this hand doubleable?
    """
    if len(hand.cards) == 2:
        return True
    return False

def isFlush(hand):
    """
    Is this hand a flush?
    
    Parameters 
    ----------
    hand : Hand object
        The hand we are looking at
        
    Returns
    -------
    soft : bool
        Is this hand a flush?
    """
    if getSuit(hand.cards[0]) == getSuit(hand.cards[1]):
        return True
    return False

def isBlackjack(hand):
    """
    Is this hand blackjack?
    
    Parameters 
    ----------
    hand : Hand object
        The hand we are looking at
        
    Returns
    -------
    soft : bool
        Is this hand blackjack?
    """
    if len(hand.cards) > 2:
        return False
    elif getTotal(hand) == 21: 
        return True
    return False

def handHas(hand, val):
    """
    Does this hand contain a card with the value val?
    
    Parameters
    ----------
    hand : Hand object
        The hand we are looking at
    val : int
        The value card to check for
        
    Returns
    -------
    has : bool
        Does this hand have val?
    """
    if (getNumber(hand.cards[0]) == val or
        getNumber(hand.cards[1]) == val):
        return True
    return False
    
    
    
    

