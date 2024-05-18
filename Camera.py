import pygame
import math

from Constants import SCREEN_HEIGHT


class Camera:
    def __init__(self, player, easy = False):
        self.y = 0
        self.player = player
        self.easy = easy

    def update(self, score):
        if self.player.y - self.y <= SCREEN_HEIGHT / 2:
            self.y = self.player.y - SCREEN_HEIGHT / 2
        if self.player.y < SCREEN_HEIGHT / 2:
            change = int(math.sqrt(score)) / 10
            if not change or self.easy:
                self.y -= 1
            elif change < 4:
                self.y -= change
            else:
                self.y -= 4
