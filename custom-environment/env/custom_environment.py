import functools
import random
from copy import copy 
import numpy as np

from gymnasium.spaces import Discrete, MultiDiscrete
from pettingzoo.utils.env import ParallelEnv
from time import sleep
class CustomEnv(ParallelEnv):
    def __init__(self):
        self.escape_y = None
        self.escape_x = None
        self.guard_x = None
        self.guard_y = None
        self.prisoner_x = None
        self.prisoner_y = None
        self.timestep = None
        self.possible_agents = ["prisoner", "guard"]
    def reset(self, seed=None, return_info=False, options=None):
        self.agents = copy(self.possible_agents)
        self.timestep = 0

        self.prisoner_x = 0
        self.prisoner_y = 0

        self.guard_x = 7
        self.guard_y = 7

        self.escape_x = random.randint(2, 5)
        self.escape_y = random.randint(2, 5)

        observation = (
            self.prisoner_x + 7 * self.prisoner_y,
            self.guard_x + 7 * self.guard_y,
            self.escape_x + 7 * self.escape_y,
        )
        observations = {
            "prisoner": {"observation": observation, "action_mask": [0, 1, 1, 0]},
            "guard": {"observation": observation, "action_mask": [1, 0, 0, 1]},
        }
        return observations
    
    def step(self, actions):
        # Execute actions
        prisoner_action = actions["prisoner"]
        guard_action = actions["guard"]

        if prisoner_action == 0 and self.prisoner_x > 0:
            self.prisoner_x -= 1
        elif prisoner_action == 1 and self.prisoner_x < 6:
            self.prisoner_x += 1
        elif prisoner_action == 2 and self.prisoner_y > 0:
            self.prisoner_y -= 1
        elif prisoner_action == 3 and self.prisoner_y < 6:
            self.prisoner_y += 1

        if guard_action == 0 and self.guard_x > 0:
            self.guard_x -= 1
        elif guard_action == 1 and self.guard_x < 6:
            self.guard_x += 1
        elif guard_action == 2 and self.guard_y > 0:
            self.guard_y -= 1
        elif guard_action == 3 and self.guard_y < 6:
            self.guard_y += 1

        # Generate action masks
        prisoner_action_mask = np.ones(4)
        if self.prisoner_x == 0:
            prisoner_action_mask[0] = 0  # Block left movement
        elif self.prisoner_x == 6:
            prisoner_action_mask[1] = 0  # Block right movement
        if self.prisoner_y == 0:
            prisoner_action_mask[2] = 0  # Block down movement
        elif self.prisoner_y == 6:
            prisoner_action_mask[3] = 0  # Block up movement

        guard_action_mask = np.ones(4)
        if self.guard_x == 0:
            guard_action_mask[0] = 0
        elif self.guard_x == 6:
            guard_action_mask[1] = 0
        if self.guard_y == 0:
            guard_action_mask[2] = 0
        elif self.guard_y == 6:
            guard_action_mask[3] = 0

        if self.guard_x - 1 == self.escape_x:
            guard_action_mask[0] = 0
        elif self.guard_x + 1 == self.escape_x:
            guard_action_mask[1] = 0
        if self.guard_y - 1 == self.escape_y:
            guard_action_mask[2] = 0
        elif self.guard_y + 1 == self.escape_y:
            guard_action_mask[3] = 0

        # Check termination conditions
        terminations = {a: False for a in self.agents}
        rewards = {a: 0 for a in self.agents}
        if self.prisoner_x == self.guard_x and self.prisoner_y == self.guard_y:
            rewards = {"prisoner": -1, "guard": 1}
            terminations = {a: True for a in self.agents}
            self.agents = []

        elif self.prisoner_x == self.escape_x and self.prisoner_y == self.escape_y:
            rewards = {"prisoner": 1, "guard": -1}
            terminations = {a: True for a in self.agents}
            self.agents = []

        # Check truncation conditions (overwrites termination conditions)
        truncations = {"prisoner": False, "guard": False}
        if self.timestep > 100:
            rewards = {"prisoner": 0, "guard": 0}
            truncations = {"prisoner": True, "guard": True}
            self.agents = []
        self.timestep += 1

        # Get observations
        observation = (
            self.prisoner_x + 7 * self.prisoner_y,
            self.guard_x + 7 * self.guard_y,
            self.escape_x + 7 * self.escape_y,
        )
        observations = {
            "prisoner": {
                "observation": observation,
                "action_mask": prisoner_action_mask,
            },
            "guard": {"observation": observation, "action_mask": guard_action_mask},
        }

        # Get dummy infos (not used in this example)
        infos = {"prisoner": {}, "guard": {}}

        return observations, rewards, terminations, truncations, infos



    def render(self):
        # grid = np.zeros((7, 7))
        # define grid of 7 x7 containing 0 using list comprehension
        grid = [["0" for x in range(7)] for y in range(7)]
        grid[self.prisoner_x][self.prisoner_y] = "P"
        grid[self.guard_x-1][ self.guard_y-1] = "G"
        grid[self.escape_x-1][ self.escape_y-1] = "E"
        # print the grid in grid form
        for i in range(7):
            for j in range(7):
                print(grid[i][j], end=" ")
            print("\n")
        print("end of episode ")
        
    @functools.lru_cache(maxsize=None)
    def observation_space(self, agent):
        return MultiDiscrete([7 * 7 - 1] * 3)

    @functools.lru_cache(maxsize=None)
    def action_space(self, agent):
        return Discrete(4)
    # def observation_space(self,agent):
    #     return self.observation_space[agent]
    # def action_space(self,agent):
    #     return self.action_spaces[agent]
    
# import register_env from pettingzoo

from pettingzoo.test import parallel_api_test

# parallel_api_test(CustomEnv() , num_cycles = 1_000_000)
parallel_api_test(CustomEnv() , num_cycles = 1_000_000)
env = CustomEnv()
env.reset()
env.render()
episode = 0

while episode <2 :
    actions = {
        "prisoner" : env.action_space("pisoner").sample(),
        "guard" : env.action_space("guard").sample()
    }
    observations, rewards, terminations, truncations, infos = env.step(actions)
    env.render()
    sleep(1)
    episode +=1
    # print(observations, rewards, terminations, truncations, infos)
        
    # render the environment
    
