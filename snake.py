import pygame
from random import randint
from sys import exit

color = {
    "apple" : (125,0,0),
    "black" : (0,0,0),
    "green" : (0,125,0)
}

WIDTH = 800
NTILES = 40
tileSize = WIDTH // NTILES
frameRate = NTILES // 3

pygame.init()
pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN])
window = pygame.display.set_mode((WIDTH,WIDTH))
clock = pygame.time.Clock()

def getRandomPosition():
    return [randint(0,NTILES-1), randint(0,NTILES-1)]

def draw(snakePositions, applePosition):
    window.fill(color["black"])
    pygame.draw.rect(window, color["apple"], (applePosition[0]*tileSize, applePosition[1]*tileSize, tileSize, tileSize))
    for snakePos in snakePositions:
        pygame.draw.rect(window, color["green"], (snakePos[0]*tileSize, snakePos[1]*tileSize, tileSize, tileSize))
    pygame.display.flip()

def handleMove(key, movement):
    if (key == pygame.K_UP or key == pygame.K_w) and movement != [0,1]:
        return [0,-1]
    elif (key == pygame.K_DOWN or key == pygame.K_s) and movement != [0,-1]:
        return [0,1]
    elif (key == pygame.K_RIGHT or key == pygame.K_d) and movement != [-1,0]:
        return [1,0]
    elif movement != [1,0]:
        return [-1,0]
    return movement

def move(snake, movementList):
    for idx in range(len(snake)):
        snake[idx][0] += movementList[idx][0]
        snake[idx][1] += movementList[idx][1]

def inbounds(snake):
    return 0 <= snake[0][0] < NTILES and 0 <= snake[0][1] < NTILES

def selfCollision(snake):
    return any(part == snake[0] for part in snake[1:])

def checkEat(snake, apple):
    return snake[0][0] == apple[0] and snake[0][1] == apple[1]

def growSnake(snake, movementDirection):
    snake.append([snake[-1][0]-movementDirection[0], snake[-1][1]-movementDirection[1]])

def propogateMovement(movementList, movement):
    return [movement] + movementList[:-1]

def close():
    pygame.quit()
    exit()

apple = getRandomPosition()
snake = [[0,0]]
movement = [1,0]
movementList = [movement]

while True:
    if checkEat(snake, apple):
        apple = getRandomPosition()
        growSnake(snake, movementList[-1])
        movementList.append(movementList[-1])

    move(snake, movementList)
    movementList = propogateMovement(movementList, movement)
    draw(snake, apple)

    if not inbounds(snake) or selfCollision(snake):
        close()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            close()
        elif event.type == pygame.KEYDOWN:
            movement = handleMove(event.key, movement)

    clock.tick(frameRate)
