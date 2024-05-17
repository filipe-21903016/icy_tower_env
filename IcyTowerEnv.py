from enum import Enum
from typing import List
from pygame import Surface
import pygame

from Camera import Camera
from Constants import *
from Platform import Platform
from PlatformController import PlatformController
from Player import Player
from Utils import load_image


class IcyTowerEnv:
    # UI
    render: bool
    game_display: Surface
    clock: pygame.time.Clock = None
    background = None
    camera: Camera
    fps: int
    # Game
    agent: Player
    platform_controller: PlatformController
    floor: Platform
    game_loop: bool
    done: bool
    action_space: List[int] = [0, 1, 2, 3]
    action_space_size = len(action_space)

    def __init__(self, render=True):
        if render:
            pygame.init()
            self.game_display = pygame.display.set_mode(res)
            self.clock = pygame.time.Clock()
            self.background = load_image("background.jpg")

        self.agent = Player()
        self.camera = Camera(self.agent)
        self.platform_controller = PlatformController()
        self.floor = Platform(0, SCREEN_HEIGHT - 36, SCREEN_WIDTH, 36)
        self.done = False
        self.fps = 60
        self.render = render

    def step(self, action: int):
        assert action in self.action_space, "Invalid action"
        prev_score = self.agent.score

        if action == 0:
            self._move_left()
        elif action == 1:
            self._move_right()
        elif action == 2:
            self._move_up()
        elif action == 3:
            self._iddle_move()

        self._update()

        reward = self.agent.score - prev_score
        info = {}
        state = self.get_state()

        return state, reward, self.done, info

    def get_state(self):
        pass

    def reset(self):
        self.agent = Player()
        self.platform_controller = PlatformController()
        self.floor = Platform(
            0, SCREEN_HEIGHT - FLOOR_HEIGHT, FLOOR_WIDTH, FLOOR_HEIGHT
        )
        self.camera = Camera(self.agent)
        self.done = False

    def _move_left(self):
        self.agent.vel_x -= self.agent.acceleration
        if self.agent.vel_x < -self.agent.max_vel_x:
            self.agent.vel_x = -self.agent.max_vel_x
        self.agent.sprite_index_y = 2

    def _move_right(self):
        self.agent.vel_x += self.agent.acceleration
        if self.agent.vel_x > self.agent.max_vel_x:
            self.agent.vel_x = self.agent.max_vel_x
        self.agent.sprite_index_y = 1

    def _move_up(self):
        if self.agent.on_any_platform(self.platform_controller, self.floor):
            self.agent.sprite_index_y = 3
            if self.agent.vel_y >= JUMP_VELOCITY / 2:
                self.agent.vel_y = -JUMP_VELOCITY

    def _iddle_move(self):
        if self.agent.vel_x < 0:
            self.agent.vel_x += self.agent.acceleration
            self.agent.vel_x -= ICE_RESISTANCE
            if self.agent.vel_x > 0:
                self.agent.vel_x = 0
        else:
            self.agent.vel_x -= self.agent.acceleration
            self.agent.vel_x += ICE_RESISTANCE
            if self.agent.vel_x < 0:
                self.agent.vel_x = 0

        if self.agent.vel_y >= JUMP_VELOCITY / 2:
            self.agent.sprite_index_y = 0

    def _update(self):
        self.agent.update()
        self.agent.combo()
        self.agent.collide_platform(self.floor, 0)
        self.platform_controller.collide_set(self.agent)
        self.platform_controller.score = self.agent.score
        self.camera.update(self.agent.score)
        self.platform_controller.generate_new_platforms(self.camera)

        if self.agent.fallen_off_screen(self.camera):
            self.done = True

        if self.render:
            self.game_display.blit(self.background, (0, 0))
            self.floor.draw(self.game_display, self.camera)
            self.platform_controller.draw(self.game_display, self.camera)
            self.agent.draw(self.game_display, self.camera)
            pygame.display.update()

    def close():
        pygame.quit()
        quit()
