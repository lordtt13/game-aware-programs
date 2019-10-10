import os
import neat
import gym, ppaquette_gym_super_mario
import pickle
import multiprocessing as mp
import warnings
import time

warnings.filterwarnings("ignore")

level = 'ppaquette/SuperMarioBros-1-1-Tiles-v0'
gym.logger.set_level(40)

class Mario:
    def __init__(self):
        self.actions = [[0, 0, 0, 1, 0, 1],[0, 0, 0, 1, 1, 1],[1, 0, 0, 1, 0, 1],[1, 0, 0, 1, 1, 1],]
        
    def calc_fitness(self, genome, config, o):
        env = gym.make(level)
        state = env.reset()
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        done = False
        c = 0
        old = 40
        while not done:
            time.sleep(0.01)
            state = state.flatten()
            output = net.activate(state)
            output = self.actions[output.index(max(output))]
            state,reward,done,info = env.step(output)
            c += 1
            if c%50==0:
                if old == info['distance']:
                    break
                else:
                    old = info['distance']
                    
        fitness = -1 if info['distance'] <= 40 else info['distance']
        if fitness >= 3252:
            pickle.dump(genome, open("finisher.pkl", "wb"))
            env.close()
            exit()
        o.put(fitness)
        print("Distance travelled: "+str(info['distance']))
        env.close()
        
    def eval_genomes(self, genomes, config):
        idx,genomes = zip(*genomes)
        for i in range(0,len(genomes),1):
            output = mp.Queue()
            operations = [mp.Process(target=self.calc_fitness, args=(genome,config,output)) for genome in genomes[i:i+1]]
            [j.start() for j in operations]
            [j.join() for j in operations]
            sol = [output.get() for j in operations]
            for x,y in enumerate(sol):
                genomes[i+x].fitness = y

    def play_mario(self, config_file, w):
        config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,neat.DefaultSpeciesSet, neat.DefaultStagnation,config_file)
        p = neat.Population(config)
        p.add_reporter(neat.StdOutReporter(True))
        p.add_reporter(neat.Checkpointer(5))
        stats_reporter = neat.StatisticsReporter()
        p.add_reporter(stats_reporter)
        winner = p.run(self.eval_genomes, w)
        real_winner = p.best_genome
        pickle.dump(winner, open('winner.pkl', 'wb'))
        pickle.dump(real_winner, open('real_winner.pkl', 'wb'))

    def main(self, config_file='config'):
        local_dir = os.path.dirname(__file__)
        config_path = os.path.join(local_dir, config_file)
        self.play_mario(config_path, 1000)

mario = Mario()
mario.main()