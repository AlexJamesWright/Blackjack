#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 21:13:17 2019

@author: ajw1e16
"""

from Game import Game
from HandSeatAndDealer import Sticker, Risker
from matplotlib import pyplot as plt
import numpy as np
        
if __name__ == '__main__':
    
    plt.figure()
    
    stickersHistory = []
    riskersHistory = []
    
    Nrealisations = 100
    for realisation in range(Nrealisations):
        # Lets create two players and start a game
    #    mug = Mug(8000)
        sticker = Sticker(8000)
        risker = Risker(8000)
        
        game = Game()
    #    game.addPlayerToSeat(mug, 0)
        game.addPlayerToSeat(sticker, 1)
        game.addPlayerToSeat(risker, 2)
        
        game.play(numberOfShoes=6, showHands=False, showBanks=False)
        
        stickersHistory.append(np.asarray(sticker.bankHistory[:170]))
        riskersHistory.append(np.asarray(risker.bankHistory[:170]))
        
    #    plt.plot(mug.bankHistory, label="Mug")
        plt.plot(sticker.bankHistory, color='blue', alpha=0.1)
        plt.plot(risker.bankHistory, color='orange', alpha=0.1)
        
    stickerMean = np.asarray(stickersHistory).mean(axis=0)
    riskerMean = np.asarray(riskersHistory).mean(axis=0)
        
    plt.plot(stickerMean, color='blue', linestyle='--', label='Sticker')
    plt.plot(riskerMean, color='orange', linestyle='--', label='Risker')
    plt.ylabel('Bank')
    plt.xlabel('Round')
    plt.ylim(0, 10000)
    plt.legend(loc='lower left')
    plt.show()
        