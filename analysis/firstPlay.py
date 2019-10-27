#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 21:13:17 2019

@author: ajw1e16
"""
import sys
sys.path.append('../src')

from Game import Game
from Players import Sticker, BasicStrategist, Counter
from matplotlib import pyplot as plt
import numpy as np
        
if __name__ == '__main__':
    
    plt.figure()
    
    playerClasses = [Sticker, BasicStrategist, Counter]
    playerHistory = [[] for player in playerClasses]
    playersMeans = []
    colours = ['blue', 'green', 'red', 'orange', 'brown', 'pink']
    
    Nrealisations = 100
    for realisation in range(Nrealisations):
        # Lets create the players 
        players = [player(8000) for player in playerClasses]
        
        # Create the game and add the players
        game = Game()
        for i, player in enumerate(players):
            game.addPlayerToSeat(player, i+1)
        
        # Play the game
        game.play(numberOfShoes=6, showHands=False, showBanks=False)
        
        # Store the history of each player's bank for this round
        for i, player in enumerate(players):
            playerHistory[i].append(np.asarray(player.bankHistory[:180]))
        
            plt.plot(player.bankHistory, color=colours[i], alpha=0.1)
        
    for history in playerHistory:
        playersMeans.append(np.asarray(history).mean(axis=0))
    
    for i, mean in enumerate(playersMeans):
        plt.plot(mean, color=colours[i], linestyle='--', label=players[i].__name__)
            
    plt.ylabel('Bank')
    plt.xlabel('Round')
    plt.ylim(0, 12000)
    plt.legend(loc='lower left')
    plt.show()
    
    for i, player in enumerate(playerClasses):
        print(f"{player.__name__}: mean bank = {playersMeans[i][-1]}")
        