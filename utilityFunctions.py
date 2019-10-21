#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 20 17:45:36 2019

@author: ajw1e16

Useful functions for interacting with the game.
"""

def getSuit(card):
    return card[-1]

def getNumber(card):
    num = card[:-1]
    try:
        return int(num)
    except ValueError:
        if num == 'A':
            return 11
        else:
            return 10

def getTotal(hand):
    tot = 0
    for card in hand.cards:
        tot += getNumber(card)
    if tot > 21 and isSoft(hand):
        tot -= 10
    return tot

def isNotBust(hand):
    return getTotal(hand) <= 21

def isBust(hand):
    return getTotal(hand) > 21

def canBePlayed(hand):
    """
    Can this hand be played? Checks that hand is not bust, and less than 21.
    If hand is 21, the hand is automatically stuck.
    """
    if hand.stuck:
        return False
    elif getTotal(hand) <= 20:
        return True
    # Either the player has 21 or bust, so auto-stick
    hand.stick()
    return False

def isSoft(hand):
    for card in hand.cards:
        if getNumber(card) is 11:
            return True
    return False

def canSplit(hand):
    if len(hand.cards) == 2 and \
                    (getNumber(hand.cards[0]) == getNumber(hand.cards[1])):
        return True
    return False

def canDoubleDown(hand):
    if len(hand.cards) == 2:
        return True
    return False

def isFlush(hand):
    if getSuit(hand.cards[0]) == getSuit(hand.cards[1]):
        return True
    return False

def isBlackjack(hand):
    if len(hand.cards) > 2:
        return False
    elif getTotal(hand) == 21: 
        return True
    return False


