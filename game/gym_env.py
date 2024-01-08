from .env import MergeBricks
import gym
from gym import spaces
import numpy as np
import pygame

class GymGame(gym.Env):
    def __init__(self, width:int = 5, height:int =5):
        super(GymGame, self).__init__()
        
        self.env = MergeBricks(width=width,height=height)
        
        self.action_space = spaces.Discrete(width*height)
        self.observation_space = spaces.Box(low=1, high=2048)
        self.action_list = []
        
        for y in range(height):
            for x in range(width):
                self.action_list.append((y,x))
                
        # Initialize Pygame
        # pygame.init()
        # self.cell_size = 100
        # # setting display size
        # self.screen = pygame.display.set_mode((width * self.cell_size, height * self.cell_size))
    
    def reset(self):
        self.env.reset
        return self.env.next
        
    def step(self, action):
        self.env.step(self.action_list[action])
        
        return self.env.next, self.env.score, self.env.end, {}
    
    def render(self):
        print(self.env.world)
        