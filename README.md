## Multi Agent Reinforcement Learning

A custom environment of Multi Agent Reinforcement Learning using PettingZoo Lib.

it simulates a multi agent reinforcement learning environment in which we have 2 agents, one Prisoner and one Guard.
There is also a gate which can be used to escape from prison.
The Prisoner always spawns at the top left and prisoner always spawns at the bottom right.

The goal of the Prisoner is to escape from the prison by opening the gate.
The goal of the Guard is to catch the Prisoner before he escapes.

# Rewards

The prisoner gets a reward of 1 if he escapes from the prison ,else he gets a reward of -1.
The guard gets a reward of 1 if he catches the prisoner ,else he gets a reward of -1 as a punishment.

# Actions

Both of the guard and prisoner can move on the grid in 4 directions, up, down, left and right.
