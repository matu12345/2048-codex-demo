# 2048 Codex Demo

This project contains a simple implementation of the 2048 puzzle and a Q-Learning
agent that learns to play the game.

## Features

- 2048 game logic in pure Python
- Q-Learning agent using an ε-greedy policy
- Normalisation of board states to avoid rotational duplicates
- Batch training script printing the score and largest tile for each episode

## Running

Run `python3 qlearning.py --episodes 1000` to train the agent for a number of episodes. Progress for each episode will be printed to the console.

