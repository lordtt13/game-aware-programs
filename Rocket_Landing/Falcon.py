from SpaceX import Elon_Musk
import gym
import numpy as np
import random
import time

seed = np.random.seed(666)

episodes = 10000
render = True

env = gym.make('LunarLander-v2')
env = env.unwrapped

lr = 0.001
gamma = 0.98
nx = env.observation_space.shape[0]
ny = env.action_space.n
agent = Elon_Musk(nx,ny,lr,gamma)
win=0
rewards_over_time = []

for i in range(episodes):
    observation = env.reset()
    observation = observation.reshape(1,-1)
    start = time.time()
    while True:
        if render==True:
            env.render()
        
        action = agent.get_action(observation)
        new_observation,reward,flag,inf = env.step(action)
        new_observation = new_observation.reshape(1,-1)
        agent.memory_recall(observation,action,reward,new_observation,flag)
        observation = new_observation

        end = time.time()
        t = end-start
        if t>15:
            flag=True
        
        total_episode_rewards = sum(agent.episode_rewards)
        if total_episode_rewards<-300:
            flag = True
        
        if flag == True:
            rewards_over_time.append(total_episode_rewards)
            max_reward = np.max(rewards_over_time)
            if int(total_episode_rewards)>150:
                render=True
            episode_max = np.argmax(rewards_over_time)
            if total_episode_rewards>=200:
                win=win+1
            print('##################################################################')
            print('Launch# : ',i)
            print('Reward : ',int(total_episode_rewards))
            print('Time : ',np.round(t,2),'sec')
            print('Maximum Reward : '+str(int(max_reward))+'       (in launch#:'+str(episode_max)+')')
            print('Wins : '+str(win))

            hist,mm = agent.training(16)
            break