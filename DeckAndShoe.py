#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 18:40:16 2019

@author: ajw1e16

Stuff involving cards
"""

import random

class Deck(object):
    
    def __init__(self):
        
        self.suits = ['h', 'd', 'c', 's']
        self.value = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        self.cards = [ value + suit for suit in self.suits for value in self.value]
        # Because maybe this will be usefull?
        self.originalCards = self.cards.copy()

class Shoe(object):
    
    def __init__(self, numberOfDecks=6):
        
        self.decks = []
        self.cards = []
        self.penPosition = None
        for i in range(numberOfDecks):
            self.decks.append(Deck())
            random.shuffle(self.decks[i].cards)
            self.cards += self.decks[i].cards
            random.shuffle(self.cards)
            
        random.shuffle(self.cards)
        
    def penetrate(self, position):
        self.penPosition = position
        lastCard = self.cards[-1]
        self.cards[position+1:] = self.cards[position:-1]
        self.cards[position] = None
        self.cards.append(lastCard)
        
    def nextCard(self):
        nextCard = self.cards[0]
        self.cards = self.cards[1:]
        return nextCard
    
    