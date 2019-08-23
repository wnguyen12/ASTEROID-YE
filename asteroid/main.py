import sys, pygame, random, pandas as pd
from ship import Ship
from asteroid import Asteroid
import matplotlib.pyplot as plt
import numpy as np
from pygame.locals import *

pygame.init()
screen_info = pygame.display.Info()

# set the width and height to the size of the screen
size = (width, height) = (int(screen_info.current_w * 0.5), int(screen_info.current_h * 0.5))

screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
color = (30, 0, 30)
screen.fill(color)

# read and store game data
df = pd.read_csv('game_info.csv')

# Setup Game Variables
Asteroids = pygame.sprite.Group()
NumLevels = df['LevelNum'].max()
Level = df['LevelNum'].min()
LevelData = df.iloc[Level]
AsteroidCount = LevelData['AsteroidCount']
Player = Ship((LevelData['PlayerX'], LevelData['PlayerY']))
Tries = 0
TotalTries = []


def init():
    global AsteroidCount, Asteroids, LevelData, Tries
    LevelData = df.iloc[Level]
    Player.reset((LevelData['PlayerX'], LevelData['PlayerY']))
    Asteroids.empty()
    AsteroidCount = LevelData['AsteroidCount']
    for i in range(AsteroidCount):
        Asteroids.add(Asteroid((random.randint(50, width - 50), random.randint(50, height - 50)), random.randint(15, 60)))
    Tries = 1


def win():

    font = pygame.font.SysFont(None, 70)
    text = font.render("You Escaped!", True, (255, 0, 0))
    text_rect = text.get_rect()
    text_rect.center = (width/2, height/2)

    index = np.arange(len(TotalTries))
    plt.bar(index, TotalTries)
    plt.xlabel('Level Number', fontsize=20)
    plt.ylabel('No of Tries', fontsize=20)
    plt.xticks(index, TotalTries, fontsize=20, rotation=5)
    plt.title('Tries per level')
    plt.show()

    while True:
        screen.fill(color)
        screen.blit(text, text_rect)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()


def main():
    global Level, Tries, TotalTries
    init()
    while Level <= NumLevels:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    Player.speed[0] = 10
                if event.key == pygame.K_LEFT:
                    Player.speed[0] = -10
                if event.key == pygame.K_UP:
                    Player.speed[1] = -10
                if event.key == pygame.K_DOWN:
                    Player.speed[1] = 10
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    Player.speed[0] = 0
                if event.key == pygame.K_LEFT:
                    Player.speed[0] = 0
                if event.key == pygame.K_UP:
                    Player.speed[1] = 0
                if event.key == pygame.K_DOWN:
                    Player.speed[1] = 0

        screen.fill(color)
        Player.update()
        Asteroids.update()
        gets_hit = pygame.sprite.spritecollide(Player, Asteroids, False)
        Asteroids.draw(screen)
        screen.blit(Player.image, Player.rect)
        pygame.display.flip()

        if Player.checkReset(width):
            TotalTries.append(Tries)
            if Level == NumLevels:
                break
            else:
                Level += 1
                init()
        elif gets_hit:
            Player.reset((LevelData['PlayerX'], LevelData['PlayerY']))
            Tries += 1

    win()


if __name__ == '__main__':
    main()