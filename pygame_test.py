import numpy as np
import pygame
import math

pygame.init()

# Tenho aqui vários pontos sobre uma circunferência

objeto = np.array([[1, 1, -1, -1, 1, 1, -1, -1],[1, -1, -1, 1, 1, -1, -1, 1],[-1, -1, -1, -1, 1, 1, 1, 1],[1, 1, 1, 1, 1, 1, 1, 1]])
d = 1
ang_x = 0
ang_y = 0
ang_z = 0


P = np.array([[1 ,0, 0, 0], [0, 1, 0, 0], [0, 0, 0, -d], [0, 0, -1/d, 0]])

# Velocidade angular (rotacoes por segundo)
v = 0.2

# Tamanho da tela e definição do FPS
screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()
FPS = 60  # Frames per Second

BLACK = (0, 0, 0)
COR_PERSONAGEM = (30, 200, 20)
COR_PONTOS = (200, 30, 20)


rodando = True
while rodando:

    rx = np.array([[1, 0, 0, 0],
    [0, math.cos(math.radians(ang_x)), -math.sin(math.radians(ang_x)), 0],
    [0, math.sin(math.radians(ang_x)), math.cos(math.radians(ang_x)), 0],
    [0, 0, 0, 1]])

    ry = np.array([[math.cos(math.radians(ang_y)), 0, math.sin(math.radians(ang_y)), 0],
                    [0, 1, 0, 0],
                    [-math.sin(math.radians(ang_y)), 0, math.cos(math.radians(ang_y)), 0],
                    [0, 0, 0, 1]])

    rz = np.array([[math.cos(math.radians(ang_z)), -math.sin(math.radians(ang_z)), 0, 0],
                [math.sin(math.radians(ang_z)), math.cos(math.radians(ang_z)), 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1]])
    
    proj = rz @ ry @ rz @ objeto
    proj[2] = proj[2] + 4
    proj = P @ proj
    proj = proj/proj[3]
    proj = proj * 200
    proj[0] = proj[0] + 800/2
    proj[1] = proj[1] + 800/2
    
    # Capturar eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:
                ang_x += 10
            elif event.key == pygame.K_y:
                ang_y += 10
            elif event.key == pygame.K_z:
                ang_z += 10


    # Controlar frame rate
    clock.tick(FPS)

    screen.fill(BLACK)

    for i in range(8):
        pygame.draw.circle(screen, COR_PERSONAGEM, (proj[0][i], proj[1][i]), 10)

    for start,end in [[0, 1], [1, 2], [2, 3], [3, 0], [4, 5], [5, 6], [6, 7], [7, 4], [0, 4], [1, 5], [2, 6], [3, 7]]:
        pygame.draw.line(screen, (0,255,0), (proj[0][start], proj[1][start]), (proj[0][end], proj[1][end]),10)


    # Update!
    pygame.display.update()

# Terminar tela
pygame.quit()