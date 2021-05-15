# Importando os pacotes
import matplotlib.pyplot as plt
import numpy as np
import random

class Ambiente:

    def __init__(self, dimx, dimy):
    
        # Atributos
        self.dimx = dimx # int
        self.dimy = dimy # int
        self.grid = np.zeros((dimx, dimy), dtype = int) # np.ndarray
        
    def add(self,x,y):
        # Adicionar obstáculo
        self.grid[x,y] = 255
    
    def rmv(self,x,y):
        # Remover obstaculo    
        self.grid[x,y] = 0

class Robo:

    def __init__(self, n_l, posx, posy, environment):
        
        # Atributos
        self.posx = posx # Posição em x
        self.posy = posy # Posição em y
        self.n_l = n_l # Campo do sensor
        self.real_grid = environment # Grid do ambiente
        self.dimx = self.real_grid.shape[0]
        self.dimy = self.real_grid.shape[1]
        self.grid_robot = np.zeros((self.dimx, self.dimy), dtype = int) # Grid do Robô
        self.potential = np.zeros((self.dimx, self.dimy), dtype = int)
        
    def define_target(self, x, y):
        # posx: posição em x do target
        # posy: posição em y do target
        self.target =  np.array([x, y])
        
        
    def detect_att(self):
        
        try:
            self.grid_robot[self.posx, self.posy - 1] = self.real_grid[self.posx, self.posy - 1] # Left vision
        except IndexError:
            pass
        
        try:
            self.grid_robot[self.posx, self.posy + 1] = self.real_grid[self.posx, self.posy + 1] # Right vision
        except IndexError:
            pass
        
        try:
            if self.x_positive == True:
                self.grid_robot[self.posx + 1, self.posy] = self.real_grid[self.posx + 1, self.posy] # Front vision
            else:
                self.grid_robot[self.posx + 1, self.posy]  = self.real_grid[self.posx -1, self.posy] # Front vision
        except IndexError:
            pass
        
    def potential_field(self):

        for i in range(self.dimx):
            xdif = abs(i-self.target[0])
            for j in range(self.dimy):
                ydif = abs(j-self.target[1])
                
                if self.grid_robot[i,j] == 0:
                    self.potential[i,j] = xdif + ydif
                else:
                    self.potential[i,j] = None
        
    def move_robot(self, x, y):
        self.posx = x
        self.posy = y
        
    def detect_collision(self, obs_obj):
        
        x_obstacles = obs_obj.xobs
        y_obstacles = obs_obj.yobs
        collision = False
        
        if any(x == self.posx for x in x_obstacles) and any(y == self.posy for y in y_obstacles):
            collision = True
            print('A collision happened!')
            
            
        return collision
        
    def choose_next_step(self):
    
        options = []
        try:            
            left = self.potential[self.posx, self.posy - 1] # Consult value of potential field in left
            grid_value = self.grid_robot[self.posx, self.posy - 1] # Check if way is free
            if left < self.potential[self.posx, self.posy] and grid_value == 0 and self.posy - 1 >= 0: 
                options.append('Left') # If value is smaller than the value from the current position, go left is an option for robot
        except IndexError or TypeError:
            pass

        try:
            right = self.potential[self.posx, self.posy + 1] # Consult value of potential field in right
            grid_value = self.grid_robot[self.posx, self.posy + 1] # Check if way is free
            if right < self.potential[self.posx, self.posy] and grid_value == 0 and self.posy + 1 >= 0:
                options.append('Right') # If value is smaller than the value from the current position, go right is an option for robot
        except IndexError or TypeError:
            pass

        try:
            if self.x_positive == True:
                front = self.potential[self.posx + 1, self.posy] # Consult value of potential field in the front
                grid_value = self.grid_robot[self.posx + 1, self.posy] # Check if way is free
                if front < self.potential[self.posx, self.posy] and grid_value == 0 and self.posx + 1 >= 0: 
                    options.append('Front') # If value is smaller than the value from the current position, go right is an option for robot
            else:
                front = self.potential[self.posx - 1, self.posy] # Consult value of potential field in the front
                grid_value = self.grid_robot[self.posx - 1, self.posy] # Check if way is free
                if front < self.potential[self.posx, self.posy] and grid_value == 0 and self.posx - 1 >= 0: 
                    options.append('Front') # If value is smaller than the value from the current position, go right is an option for robot
        except IndexError or TypeError:
            pass

        try:    
            robot_will_move = random.choice(options)
        
        except IndexError:
            robot_will_move = None
            print('\nThere is no possible movement right now')

        return robot_will_move
    
    def initial_direction(self):
        x_dir = self.target[0] - self.posx

        if x_dir > 0:
            print('\nThe robot is looking in the positive direction of x')
            self.x_positive = True
        else:
            print('\nThe robot is looking in the negative direction of x')
            self.x_positive = False


class ObstaculoMovel():
    
    def __init__(self, environment):
        self.env_obj = environment        
            
    def include_obs(self):
        env = self.env_obj.grid
        
        maxdimx = env.shape[0] - 1
        maxdimy = env.shape[1] - 1
        
        self.xobs = np.random.randint(0, maxdimx, size = 2)
        self.yobs = np.random.randint(0, maxdimy, size = 2)
        
        self.env_obj.add(self.xobs[0], self.yobs[0])
        self.env_obj.add(self.xobs[1], self.yobs[1])
        
    def move_obs(self):
        
        self.env_obj.rmv(self.xobs[0], self.yobs[0])
        self.env_obj.rmv(self.xobs[1], self.yobs[1])
        
        self.include_obs()       
        
