import gym
import numpy as np
from agent import Agent
# from utils import plot_learning_curve
from gym import wrappers
import environment as e
from environment import _Embedding, MulticastEnvironment
import tensorflow as tf

if __name__ == '__main__':

    env = MulticastEnvironment('multi-cast')    
    objects_A = e.generate_prefixes('/uofm/',  'abcdefgh')
    objects_B = e.generate_prefixes('/mit/',  'ijklmnox')
    objects_B = e.generate_prefixes('/ucla/',  'pqrstuvw')
    doc_dict = e.doc_dict
    embed = _Embedding(len(doc_dict.values()))
    agent = Agent(alpha=1e-5, n_actions=2)
 
    # duplicates, delay_timer 
    observation = list(doc_dict.values())[0]
    observation = embed.get_embedding(observation)
    observation = tf.math.reduce_mean(observation, axis=0)
    observation = tf.concat ((observation, [2, 5]), axis=0)
    
    done = False
    while not done:
        action = agent.choose_action(observation)
        print(action)
        exit()



    # #env = gym.make('LunarLander-v2')
    # env = emb.('multi-cast')
    # n_games = 1800
    # # uncomment this line and do a mkdir tmp && mkdir video if you want to
    # # record video of the agent playing the game.
    # #env = wrappers.Monitor(env, 'tmp/video', video_callable=lambda episode_id: True, force=True)
    # # filename = 'cartpole_1e-5_1024x512_1800games.png'
    # # figure_file = 'plots/' + filename

    # best_score = env.reward_range[0]
    # score_history = []
    # load_checkpoint = False 

    # if load_checkpoint:
    #     agent.load_models()

    # for i in range(n_games):
    #     observation = env.reset()
    #     done = False
    #     score = 0
    #     while not done:
    #         action = agent.choose_action(observation)
    #         observation_, reward, done, info = env.step(action)
    #         if i == 2:
    #             exit()
    #             score+= reward
    #         if not load_checkpoint:
    #             agent.learn(observation, reward, observation_, done)
    #         observation = observation_
    #     score_history.append(score)
    #     avg_score = np.mean(score_history[-100:])

    #     if avg_score > best_score:
    #         best_score = avg_score
    #         if not load_checkpoint:
    #             agent.save_models()

    #     # print('episode ', i, 'score %.1f' % score, 'avg_score %.1f' % avg_score)

    # if not load_checkpoint:
    #     x = [i+1 for i in range(n_games)]
    #     print(x, score_history)