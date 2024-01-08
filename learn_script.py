import gym
from game import GymGame
from game import MergeBricks
import numpy as np



env = MergeBricks()

done=False
while not done:
    action = env.action_list[np.random.randint(len(env.action_list))]
    env.step(action)
    done= env.end
    
    print(env.world)
    print('Reward:', env.score)
    print('Done:', done)

# # Register the environment
# gym.register(
#     id='GymGame-v0',
#     entry_point='game:GymGame', 
#     kwargs={'width': 5,
#             'height':5} 
# )



# env = gym.make('GymGame-v0')

# obs = env.reset()

# done = False
# while not done:
#     action = env.action_space.sample()  # Random action selection
#     obs, reward, done, _ = env.step(action)
#     env.render()
#     print('Reward:', reward)
#     print('Done:', done)
    
    