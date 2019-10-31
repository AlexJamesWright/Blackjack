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
from time import time

if __name__ == '__main__':

    plt.figure()

    # Colours for plotting
    colours = ['blue', 'green', 'red', 'orange', 'brown', 'pink']

    # How many times to run the experiment
    Nrealisations = 10

    # How many shoes to play in each experiment
    Nshoes = 3000

    # How much should the players start with
    startingBank = 80000

    # Each of the players we are going to use
    playerClasses = [BasicStrategist, Counter]

    # A list (later a numpy array) of the histories of each player
    # shape = (Nplayers, Nrealisations, Nrounds)
    playerHistory = np.zeros((len(playerClasses), Nrealisations, Nshoes*52*6//2))

    # The mean of each players bank at this round
    playersMeans = np.zeros((len(playerClasses), Nshoes*52*6//2))


    # All players will have the same number of rounds played by the end of each
    # experiment/realisation, however the different realisations may have a
    # different number of rounds between them,. which causes problems when
    # averaging over the realisations. Only average as far as is possible using
    # all realisations
    minRounds = np.inf
    maxRounds = 0

    for realisation in range(Nrealisations):
        # Lets create the players
        players = [player(startingBank) for player in playerClasses]

        # Create the game and add the players
        game = Game()
        for i, player in enumerate(players):
            game.addPlayerToSeat(player, i+1)

        # Play the game
        startTime = time()
        game.play(numberOfShoes=Nshoes, showHands=False, showBanks=False)
        print(f"One game took {time() - startTime}")
        # Set the minimum/maximum number of rounds played so far
        thisRounds = len(players[0].bankHistory)
        minRounds = min(minRounds, thisRounds)
        maxRounds = max(maxRounds, thisRounds)

        # Store the history of each player's bank for this round
        for i, player in enumerate(players):
            playerHistory[i, realisation, :thisRounds] = np.asarray(player.bankHistory)

            plt.plot(player.bankHistory, color=colours[i], alpha=0.1)

    for i, history in enumerate(playerHistory):
        playersMeans[i, :minRounds] = history[:, :minRounds].mean(axis=0)

    for i, mean in enumerate(playersMeans):
        plt.plot(mean[:minRounds], color=colours[i], linestyle='--', label=players[i].__name__)

    plt.ylabel('Bank')
    plt.xlabel('Round')
    plt.ylim(0, 1.5*startingBank)
    plt.legend(loc='lower left')
    plt.show()

    for i, player in enumerate(playerClasses):
        print(f"{player.__name__}: mean bank = {playersMeans[i][minRounds-1]}")
