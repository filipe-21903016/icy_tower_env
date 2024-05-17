from IcyTowerEnv import IcyTowerEnv


def main():
    env = IcyTowerEnv()

    for i in range(30):
        env.step(1)

    input("Press to reset")
    env.reset()


if __name__ == "__main__":
    main()
