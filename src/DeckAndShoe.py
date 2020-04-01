#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 18:40:16 2019

@author: ajw1e16

Stuff involving cards
"""

import random

class Deck(object):
    """
    A single deck of cards.
    """
    
    def __init__(self):
        
        self.suits = ['h', 'd', 'c', 's']
        self.value = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        self.cards = [ value + suit for suit in self.suits for value in self.value]
        # Because maybe this will be usefull?
        self.originalCards = self.cards.copy()


class Shoe(object):
    """
    A single shoe, containing multiple decks.
    
    Parameters 
    ----------
    broadcast : object
        Broadcast object
    numberOfDecks : int 
        Number of decks to use in this shoe
    """
    def __init__(self, broadcast, numberOfDecks=6):
        
        self.decks = []
        self.cards = []
        self.penPosition = None
        self.broadcast = broadcast
        self.broadcast.numberOfDecks = numberOfDecks
        for i in range(numberOfDecks):
            self.decks.append(Deck())
            self.cards += self.decks[i].cards
            
        random.shuffle(self.cards)
        
    def penetrate(self, position):
        """
        Penetrate the deck with the None card.
        
        Parameters
        ----------
        position : int
            Card number at which to penetrate deck 
        """
        self.penPosition = position
        lastCard = self.cards[-1]
        self.cards[position+1:] = self.cards[position:-1]
        self.cards[position] = None
        self.cards.append(lastCard)
        
    def nextCard(self):
        """
        Used everytime a card is requested. This removes the card at index 0, 
        returns is, and shifts all cards forward by one.
        
        Returns
        -------
        card : str
            String defining the next card out the shoe
        """
        card = self.cards[0]
        self.cards = self.cards[1:]
        
        if card is not None:
            self.broadcast.append(card)
            return card
        else:
            return self.nextCard()
    
    