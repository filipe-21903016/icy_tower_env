from enum import Enum
from typing import List
from pygame import Surface
import pygame
from Camera import Camera
from Constants import *
from Platform import Platform
from PlatformController import PlatformController
from Player import Player
from Utils import load_image, message_display
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())
logger.addHandler(logging.FileHandler("log.txt"))


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
    steps: List[int]
    action_space: List[int] = [0, 1, 2, 3]
    action_size = len(action_space)
    state_size = 9
    easy: bool

    def __init__(self, render=True, easy=False):
        if render:
            pygame.init()
            self.game_display = pygame.display.set_mode(res)
            self.clock = pygame.time.Clock()
            self.background = load_image("background.jpg")

        self.easy = easy
        self.render = render
        self.agent = Player(render)
        self.camera = Camera(self.agent, easy)
        self.platform_controller = PlatformController(easy=easy)
        self.floor = Platform(0, SCREEN_HEIGHT - 36, SCREEN_WIDTH, 36)
        self.done = False
        self.fps = 60
        self.steps = []

    def step(self, action: int):
        assert action in self.action_space, "Invalid action"
        prev_score = self.agent.score

        logger.debug(f"\n======= START OF STEP {len(self.steps)} =======")

        if action == 0:
            self._move_left()
            logger.debug(f"ACTION: Moved Left: [{self.agent.x}, {self.agent.y}]")
        elif action == 1:
            self._move_right()
            logger.debug(f"ACTION: Move Right: [{self.agent.x}, {self.agent.y}]")
        elif action == 2:
            self._move_up()
            logger.debug(f"ACTION: Moved Up: [{self.agent.x}, {self.agent.y}]")
        elif action == 3:
            self._iddle_move()
            logger.debug(f"ACTION: Iddle: [{self.agent.x}, {self.agent.y}]")

        self.steps.append(action)

        self._update()

        state = self.get_state()

        reward = self.agent.score - prev_score if not self.done else -100
        logger.debug(f"STATE: {', '.join(map(str, state))}")
        logger.debug(f"REWARD: {reward}")
        logger.debug(f"SCORE: {self.agent.score}")

        info = {}
        state = self.get_state()

        logger.debug(f"======= END OF STEP =======\n")
        return state, reward, self.done, info

    def get_state(self):
        agent_x, agent_y = self.agent.x, self.agent.y
        agent_vx, agent_vy = self.agent.vel_x, self.agent.vel_y
        nearest_platforms = self.platform_controller.get_nearest_platforms(
            self.agent, 2
        )
        on_platform = self.agent.on_any_platform(self.platform_controller, self.floor)

        state = [
            agent_x,
            agent_y,
            agent_vx,
            agent_vy,
            on_platform and 1 or 0,
            nearest_platforms[0].x,
            nearest_platforms[0].y,
            nearest_platforms[1].x,
            nearest_platforms[1].y,
        ]

        return state

    def reset(self):
        self.agent = Player(self.render)
        self.platform_controller = PlatformController(easy=self.easy)
        self.floor = Platform(
            0, SCREEN_HEIGHT - FLOOR_HEIGHT, FLOOR_WIDTH, FLOOR_HEIGHT
        )
        self.camera = Camera(self.agent, self.easy)
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
            message_display(
                self.game_display, str(self.agent.score), 25, 30, 36, (255, 255, 255)
            )
            pygame.display.update()
            self.clock.tick(self.fps)

    def close(self):
        pygame.quit()
        quit()
