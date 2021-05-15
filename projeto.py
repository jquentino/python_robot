from classes import Ambiente, Robo, ObstaculoMovel
from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt
import numpy as np
import random
import copy
import time


obstaculos = [[2,4], [3,1], [3,8], [5,2], [6,4], [7,1], [8,7]]  
target = [5,5]
pos_inicial = [0,9]

# Dimensões do Ambiente
dimx, dimy = 10, 10 # Dimensões da grid do ambiente em x e y
amb = Ambiente(dimx, dimy) # Objeto da classe Ambiente

for par in obstaculos:
    amb.add(par[0], par[1])
    
# Parâmetros do Robô
posx, posy  = pos_inicial[0], pos_inicial[1] # Posição inicial do robô em x e y
sensor = 1 # Nl (alcance do sensor do robô)
robo = Robo(sensor, posx, posy, amb.grid) # Objeto da classe Robô
robo.define_target(target[0], target[1])

# Obstáculos Móveis
moving_obs = ObstaculoMovel(amb)
moving_obs.include_obs()

print('This is initial environment:')
fig = plt.figure()
ax = fig.add_subplot(111)
cmap = ListedColormap(['w', 'k', 'r', 'lightgreen'])
positions = amb.grid.copy()
positions[robo.posx, robo.posy] = 510 
positions[target[0], target[1]] = 1020 
cax = ax.matshow(positions.tolist(),cmap=cmap)

# Planejar caminho inicial
robo.initial_direction()
robo.detect_att()
robo.potential_field() # Calcular campo potencial inicial
collision = False

while robo.posx != target[0] or robo.posy != target[1]:
    
    robot_will_move = robo.choose_next_step()
    
    if robot_will_move == None:
        robo.potential_field()
        robot_will_move = chose_next_step(robo) 
    if robot_will_move == 'Left':
        robo.move_robot(robo.posx, robo.posy - 1)
    elif robot_will_move == 'Right':
        robo.move_robot(robo.posx, robo.posy + 1)
    elif robot_will_move == 'Front':
        if robo.x_positive == True:
            robo.move_robot(robo.posx + 1, robo.posy)
        else:
            robo.move_robot(robo.posx - 1, robo.posy)

    print('\nRobot position:', robo.posx, robo.posy)  
    
    #Uncomment the lines below to make the obstacles moves. 
    # moving_obs.move_obs()
    # collision = robo.detect_collision(moving_obs)
    
    if collision == True:
         break
    
    # Plotando posições
    fig = plt.figure()
    ax = fig.add_subplot(111)
    cmap = ListedColormap(['w', 'k', 'r', 'lightgreen'])
    positions = amb.grid.copy()
    positions[robo.posx, robo.posy] = 510 
    positions[target[0], target[1]] = 1020 
    cax = ax.imshow(positions.tolist(), cmap = cmap)
      
    #  Início do próximo movimento
    robo.detect_att()
        