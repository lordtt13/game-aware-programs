import pygame
import os

class Bird:
    def __init__(self,x,y):
        self.x = x;
        self.y = y;
        self.t = 0
        self.vel = 0
        self.height = self.y
        self.img = pygame.transform.scale2x(pygame.image.load(os.path.join("gallery","bird.png")))

    def jump(self):
        self.vel = -10.5
        self.t = 0
        self.height = self.y

    def move(self):
        self.t += 1
        d = self.vel*self.t+1.5*self.t**2
        if d>=16:
            d = 16
        if d<0:
            d -= 2
        self.y = self.y+d
    
    def draw(self,win):
        win.blit(self.img,(self.x,self.y))
    
    def get_mask(self):
        return pygame.mask.from_surface(self.img)