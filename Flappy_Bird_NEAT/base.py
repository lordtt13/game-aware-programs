import pygame
import os

base_image = pygame.transform.scale2x(pygame.image.load(os.path.join("gallery","base.png")))

class Base:
    img = base_image
    def __init__(self,y):
        self.w = base_image.get_width()
        self.y = y
        self.x1 = 0
        self.x2 = self.w

    def move(self):
        self.x1 -= 5
        self.x2 -= 5
        if self.x1+self.w <= 0:
            self.x1 = self.x2 + self.w
        if self.x2+self.w <= 0:
            self.x2 = self.x1 + self.w
    
    def draw(self,win):
        win.blit(self.img,(self.x1,self.y))
        win.blit(self.img,(self.x2,self.y))