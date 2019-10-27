#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 18:42:56 2019

@author: ajw1e16

Table class
"""

from DeckAndShoe import Shoe
from HandSeatAndDealer import Seat, Dealer
import utilityFunctions as ut

class Table(object):
    """
    Physical table. Has seats, a dealer, and a shoe.
    
    Parameters
    ----------
    broadcast : object
        Broadcast object
    maxNumberOfSeats : int
        Maximum number of seats at the table.
    minBet : int
        Minimum bet size
    maxBet : int
        Maximum bet size
    """
    
    maxNumberOfSeats = 6
    
    
    def __init__(self, broadcast, numberOfSeats=6, minBet=1, maxBet=100):
        self.broadcast = broadcast
        self.dealer = Dealer()
        self.seats = []
        self.numberOfSeats = numberOfSeats
        self.newShoe()
        
        for i in range(self.numberOfSeats):
            if i < self.maxNumberOfSeats:
                self.newSeat()
        
        
    def newShoe(self, penPosition=250):
        """
        Generate a new shoe.
        """
        self.broadcast.reset()
        self.shoe = Shoe(self.broadcast)
        self.shoe.penetrate(penPosition)
        
        
    def newSeat(self):
        """
        Add a new seat to the table.
        """
        self.seats.append(Seat())
        
        
    def playerActions(self):
        """
        Go round the table and perform all player actions.
        """
        for seat in self.seats:
            for hand in seat.hands:
                # Start of hand, deal with doubling and splitting firest
                if len(hand.cards) == 1:
                    # Player must have split so take another card
                    hand.cards.append(self.shoe.nextCard())
                elif len(seat.hands) == 1 and ut.canSplit(hand) and seat.player.wantsToSplit(hand) and seat.player.bank >= hand.bet:
                    seat.newBet(hand.bet)
                    seat.hands[1].cards.append(hand.cards[1])
                    hand.cards.remove(hand.cards[1])
                    hand.cards.append(self.shoe.nextCard())
                elif ut.canDoubleDown(hand) and seat.player.wantsToDoubleDown(hand) and seat.player.bank >= hand.bet:
                    seat.player.roundBetting += hand.bet
                    hand.doubleDown(self.shoe)
                # Special actions have been delt with, now play normally
                while ut.canBePlayed(hand):
                    if seat.player.wantsToHit(hand):
                        hand.hit(self.shoe)
                    else:
                        hand.stick()
                    
                    
    def cleanSeats(self):
        """
        Delete all hands.
        """
        for seat in self.seats:
            seat.resetSeat()
        self.dealer.resetHand()
        
        
    def getBets(self):
        """
        Go around the table requesting bets from the players/
        """
        # Get the bets from the seats
        for seat in self.seats:
            if seat.player:
                # Get players bet size
                seat.newBet(seat.player.getBet()) 
        
        
    def deal(self):
        """
        Go round the table dealing cards to the players and dealer.
        """
        # Hand out two cards to each player and the dealer
        # First card
        for seat in self.seats:
            if seat.player:
                for hand in seat.hands:
                    hand.addCard(self.shoe.nextCard())
        # Dealer's first
        self.dealer.hand.addCard(self.shoe.nextCard())
        # Second card
        for seat in self.seats:
            if seat.player:
                for hand in seat.hands:
                    hand.addCard(self.shoe.nextCard())
        # Dealers second
        self.dealer.hand.addCard(self.shoe.nextCard())
        
        # Update the broadcast with dealers up card
        self.broadcast.dealersTotal = self.dealer.total()
        
        
    def dealerAction(self):
        """
        Dealer plays until theys stick or bust.
        """
        self.dealer.playHand(self.dealer.hand, self.shoe)
        
        
    def nextRound(self):
        """
        Play the next round of blakjack
        """
        # Need to initialise some new bets/hands
        self.cleanSeats()
        self.getBets()
        self.deal()
        self.playerActions()
        self.dealerAction()
        self.settleUp()
    
    def getPlayers(self):
        """
        Get all the players current at the table.
        
        Returns
        -------
        player : list
            A list of all Player objects at the table
        
        """
        players = []
        for seat in self.seats:
            if seat.player not in players and seat.player is not None:
                players.append(seat.player)
        return players
        
    def settleUp(self):
        """
        Casino pays out winning hands.
        """
        for seat in self.seats:
            for hand in seat.hands:
                # Only pay out if player isnt bust
                if ut.isNotBust(hand):
                    # Recall that bet has already been taken, so payouts must
                    # include this again. I.e. a push requires bank+=bet
                    
                    # Payout 1.5x if player got blackjack
                    if ut.isBlackjack(hand):
                        seat.player.payout += hand.bet*2.5
                    # Pay out if dealer busts
                    elif ut.isBust(self.dealer.hand):
                        seat.player.payout += hand.bet*2
                    # Pay out if higher score than dealer
                    elif ut.getTotal(hand) > self.dealer.fullTotal():
                        seat.player.payout += hand.bet*2
                    # Push, give bet back
                    elif ut.getTotal(hand) == self.dealer.fullTotal():
                        seat.player.payout += hand.bet
                        
        for player in self.getPlayers():
            player.settleRound()