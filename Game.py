import pygame
from Camera import Camera
from Player import Player
from Platform import Platform
from PlatformController import PlatformController

# pygame.init()

from Constants import *
from Utils import *

# game_display = pygame.display.set_mode(res)
# pygame.display.set_caption(GAME_CAPTION)

black = (0, 0, 0)
blue = (0, 0, 255)
white = (255, 255, 255)


def reinit():
    global player
    global platform_controller
    global floor
    global camera
    player = Player()
    platform_controller = PlatformController()
    floor = Platform(0, SCREEN_HEIGHT - 36, SCREEN_WIDTH, 36)
    camera = Camera(player)


player = Player()
platform_controller = PlatformController()
floor = Platform(0, SCREEN_HEIGHT - 36, SCREEN_WIDTH, 36)

arrow_image = load_image("arrow.png")
selected_option = 0.30

background = load_image("background.jpg")

camera = Camera(player)

game_state = "Playing"

game_loop = True
clock = pygame.time.Clock()
fps = 60

while game_loop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_loop = False
    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[pygame.K_LEFT]:
        player.vel_x -= player.acceleration
        if player.vel_x < -player.max_vel_x:
            player.vel_x = -player.max_vel_x
        player.sprite_index_y = 2
    elif keys_pressed[pygame.K_RIGHT]:
        player.vel_x += player.acceleration
        if player.vel_x > player.max_vel_x:
            player.vel_x = player.max_vel_x
        player.sprite_index_y = 1
    else:
        if player.vel_x < 0:
            player.vel_x += player.acceleration
            player.vel_x -= ICE_RESISTANCE
            if player.vel_x > 0:
                player.vel_x = 0
        else:
            player.vel_x -= player.acceleration
            player.vel_x += ICE_RESISTANCE
            if player.vel_x < 0:
                player.vel_x = 0

        if player.vel_y >= JUMP_VELOCITY / 2:
            player.sprite_index_y = 0
    # -------------------------PLAYING---------------------------

    if keys_pressed[pygame.K_SPACE]:
        if player.on_any_platform(platform_controller, floor):
            player.sprite_index_y = 3
            if player.vel_y >= JUMP_VELOCITY / 2:
                player.vel_y = -JUMP_VELOCITY

    player.update()
    player.combo()
    player.collide_platform(floor, 0)
    platform_controller.collide_set(player)

    platform_controller.score = player.score
    camera.update(player.score)
    platform_controller.generate_new_platforms(camera)

    if player.fallen_off_screen(camera):
        game_state = "Game Over"

    game_display.blit(background, (0, 0))

    floor.draw(game_display, camera)
    platform_controller.draw(game_display, camera)
    player.draw(game_display, camera)

    message_display(game_display, str(player.score), 25, 30, 36, white)

    # # ------------------------GAME OVER--------------------------
    # elif game_state == "Game Over":

    #     game_display.blit(background, (0, 0))
    #     if pygame.font:
    #         message_display(game_display, "GAME OVER", 0, 200, 70, white, True)
    #         message_display(
    #             game_display, "Score: %d" % player.score, 0, 300, 50, white, True
    #         )
    #         message_display(
    #             game_display, "Press SPACE to play again!", 0, 400, 50, white, True
    #         )
    #         message_display(
    #             game_display, "Press ESC to return to menu!", 0, 500, 40, white, True
    #         )

    # --------------------------ABOUT----------------------------
    # elif game_state == "About":
    #     game_display.blit(background, (0, 0))
    #     if pygame.font:
    #         for line in ABOUT_MESSAGE:
    #             message_display(
    #                 game_display,
    #                 line,
    #                 0,
    #                 MENU_START_Y + ABOUT_MESSAGE.index(line) * 35,
    #                 30,
    #                 white,
    #                 True,
    #             )
    #         message_display(
    #             game_display, "Press ESC to return to menu!", 0, 500, 40, white, True
    #         )

    # -----------------------------------------------------------

    # pygame.display.update()
    # clock.tick(fps)

# pygame.quit()
# quit()
