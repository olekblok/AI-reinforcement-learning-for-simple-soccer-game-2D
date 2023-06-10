import torch
import random
from collections import namedtuple, deque
import numpy as np
from Model import DNN_QNet
from Model import QTrainer
import math
import os
import Constants

# Define named tuple for storing experiences
Experience = namedtuple('Experience', ['state', 'action', 'reward', 'next_state', 'done'])


class ReplayBuffer:
    def __init__(self, buffer_size):
        self.buffer = deque(maxlen=buffer_size)

    def add(self, experience):
        self.buffer.append(experience)

    def sample(self, batch_size):
        batch = random.sample(self.buffer, batch_size)
        states = []
        actions = []
        rewards = []
        next_states = []
        dones = []
        for experience in batch:
            states.append(experience.state)
            actions.append(experience.action)
            rewards.append(experience.reward)
            next_states.append(experience.next_state)
            dones.append(experience.done)
        return states, actions, rewards, next_states, dones

    def __len__(self):
        return len(self.buffer)


class Agent:
    def __init__(self, replay_buffer_size=10000):
        self.n_games = 0
        self.epsilon = 1  # Exploration rate
        self.gamma = 0.9  # discount rate
        self.replay_buffer = ReplayBuffer(replay_buffer_size)
        self.batch_size = Constants.BATCH_SIZE
        self.model = DNN_QNet(15, 256, 4)
        self.trainer = QTrainer(self.model, lr=Constants.LR, gamma=self.gamma)

    @staticmethod
    def get_state(p, b, o):
        state = [
            # Ball location
            b.x,
            b.y,
            b.v_x,
            b.v_y,

            # Player location
            p.x,
            p.y,

            # Opponent location
            o.x,
            o.y,

            # Distance and angle to the ball
            b.x - p.x,
            b.y - p.y,
            math.atan2(b.y - p.y, b.x - p.x),

            # Boundaries location
            p.bx1,
            p.bx2,
            p.by1,
            p.by2
        ]
        return np.array(state, dtype=float)

    def remember(self, state, action, reward, next_state, done):
        experience = Experience(state, action, reward, next_state, done)
        self.replay_buffer.add(experience)

    def train_long_memory(self):
        if len(self.replay_buffer) > self.batch_size:
            states, actions, rewards, next_states, dones = self.replay_buffer.sample(self.batch_size)
            self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        # random moves: tradeoff exploration / exploitation
        self.epsilon = 80 - self.n_games
        final_move = [0, 0, 0, 0]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 3)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move

    def load_model(self, file_path):
        if os.path.exists(file_path):
            self.model.load_state_dict(torch.load(file_path))
            print("Model loaded successfully!")
        else:
            print("No saved model found.")
