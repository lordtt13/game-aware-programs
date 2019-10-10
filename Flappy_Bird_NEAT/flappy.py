from bird import Bird
from pipe import Pipe
from base import Base
import neat
import random
import pygame
import os

def run(config_path):
    config = neat.config.Config(neat.DefaultGenome,neat.DefaultReproduction,neat.DefaultSpeciesSet,neat.DefaultStagnation,config_path)
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    winner = p.run(main,50)

def screen(win,birds,pipe,base,score):
    win.blit(pygame.transform.scale2x(pygame.image.load(os.path.join("gallery","back.png"))),(0,0))
    for i in pipe:
        i.draw(win)
    base.draw(win)
    #win.blit(base_image,(0,730))
    for bird in birds:
        bird.draw(win)
    pygame.font.init()
    score_font = pygame.font.SysFont("Forte",50)
    score_text = score_font.render("Score: "+str(score),1,(0,0,0))
    win.blit(score_text,(10,10))
    pygame.display.update()

def main(genomes,config):
    pygame.init()
    win = pygame.display.set_mode((500,800))
    pygame.display.set_caption('Flappy Birds!')

    nets = []
    ge = []
    birds = []
    pipes = [Pipe(600)]
    base = Base(730)
    
    for _,g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g,config)
        nets.append(net)
        birds.append(Bird(230,350))
        g.fitness = 0
        ge.append(g)

    done = True
    clk = pygame.time.Clock()
    speed = 60
    score = 0

    while done:
        clk.tick(speed)
        curr_pipe = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = False
                pygame.quit()
                break
        
        if len(birds) > 0:
            if len(pipes) >1 and birds[0].x > pipes[0].x + pipes[0].pipe_top.get_width():
                curr_pipe = 1
        else:
            done = False
            break

        for x,bird in enumerate(birds):
            bird.move()
            ge[x].fitness += 0.1
            
            output = nets[x].activate((bird.y,abs(bird.y-pipes[curr_pipe].height),abs(bird.y-pipes[curr_pipe].bottom)))

            if output[0]>0.5:
                bird.jump()

        pipe_added = False
        del_pipe = []
        for i in pipes:
            for x,bird in enumerate(birds):
                if i.collide(bird):
                    ge[x].fitness -= 1
                    birds.pop(x)
                    nets.pop(x)
                    ge.pop(x)
                if not i.passed and i.x<bird.x:
                    i.passed = True
                    pipe_added = True
            
            if i.x+i.pipe_top.get_width()<0:
                del_pipe.append(i)
            
            i.move()
        if pipe_added:
            score += 1
            for g in ge:
                g.fitness += 5
            pipes.append(Pipe(700))
        for j in del_pipe:
            pipes.remove(j)
        
        for x,bird in enumerate(birds):    
            if bird.y+bird.img.get_height()>=730 or bird.y<0:
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)
        base.move()
        screen(win,birds,pipes,base,score)

if __name__=="__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir,"config-feedforward.txt")
    run(config_path)