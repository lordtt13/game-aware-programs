import random
import pygame
import os

from bird import Bird
from pipe import Pipe
from base import Base

def draw_win(win,bird,pipe,base,score):
    win.blit(pygame.transform.scale2x(pygame.image.load(os.path.join("gallery","back.png"))),(0,0))
    for i in pipe:
        i.draw(win)
    base.draw(win)
    #win.blit(base_image,(0,575))
    bird.draw(win)
    pygame.font.init()
    score_font = pygame.font.SysFont("Forte",50)
    score_text = score_font.render("Score: "+str(score),1,(0,0,0))
    win.blit(score_text,(10,10))
    pygame.display.update()

def main():
    bird = Bird(230,350)
    base = Base(730)
    pipes = [Pipe(600)]
    pygame.init()
    win = pygame.display.set_mode((500,800))
    pygame.display.set_caption('Flappy Birds!')
    done = True
    clk = pygame.time.Clock()
    score = 0
    while done:
        clk.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = False
            if event.type ==pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump()
        bird.move()
        add_pipe = False
        del_pipe = []
        for i in pipes:
            if i.collide(bird):
                pygame.quit()
                break
            if i.x+i.pipe_top.get_width()<0:
                del_pipe.append(i)
            if not i.passed and i.x<bird.x:
                i.passed = True
                add_pipe = True
            i.move()
        if add_pipe:
            score += 1
            pipes.append(Pipe(700))
        for j in del_pipe:
            pipes.remove(j)
        if bird.y+bird.img.get_height()>=730 or bird.y<0:
            done = False
            break
        base.move()
        draw_win(win,bird,pipes,base,score)
    pygame.quit()
    quit()
main()