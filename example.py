from IcyTowerEnv import IcyTowerEnv
import pygame


def main():
    pygame.init()
    env = IcyTowerEnv(True)
    while True:
        state = None
        reward = 0
        done = False
        info = {}

        # Listen for keyboard input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_ESCAPE]:
            pygame.quit()
            env.close()
            quit()
        elif keys_pressed[pygame.K_LEFT]:
            state, reward, done, info = env.step(0)
        elif keys_pressed[pygame.K_RIGHT]:
            state, reward, done, info = env.step(1)
        else:
            state, reward, done, info = env.step(3)

        if keys_pressed[pygame.K_SPACE]:
            state, reward, done, info = env.step(2)

        if done:
            env.reset()
            break


if __name__ == "__main__":
    main()
