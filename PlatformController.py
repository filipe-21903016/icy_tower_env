import math
from random import randrange, getrandbits
from Platform import Platform
from Constants import SCREEN_WIDTH, MAX_JUMP


class PlatformController:
    def __init__(self, easy=False):
        self.platform_set = []
        self.index = 10
        self.last_x = MAX_JUMP
        self.score = 0
        self.easy = easy
        for i in range(0, self.index):
            self.platform_set.append(self.generate_platform(i, self.score))

    def generate_platform(self, index, score):
        if self.easy:
            change = 0
        elif score < MAX_JUMP * MAX_JUMP:
            change = int(math.sqrt(score))
        else:
            change = MAX_JUMP - 1
        width = 200 - randrange(change, change + 60)
        height = 20
        y = 600 - index * 100
        while True:
            side = bool(getrandbits(1))
            if side:
                x = randrange(self.last_x - MAX_JUMP, self.last_x - change)
            else:
                x = randrange(
                    self.last_x + width + change, self.last_x + MAX_JUMP + width
                )
            if 0 <= x <= SCREEN_WIDTH - width:
                break
        self.last_x = x
        return Platform(x, y, width, height)

    def draw(self, game_display, camera):
        for p in self.platform_set:
            p.draw(game_display, camera)

    def collide_set(self, player):
        for i, p in enumerate(self.platform_set):
            player.collide_platform(p, i)

    def generate_new_platforms(self, camera):
        if self.platform_set[-1].y - camera.y > -50:
            for i in range(self.index, self.index + 10):
                self.platform_set.append(self.generate_platform(i, self.score))
            self.index += 10

    def get_nearest_platforms(self, player, num_platforms):
        n = min(num_platforms, len(self.platform_set))
        platforms = sorted(
            [p for p in self.platform_set if p.y < player.y],
            key=lambda p: p.y,
            reverse=True,
        )
        return platforms[:n]
