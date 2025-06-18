import pygame
import random
import pickle
import numpy as np
from flappy_game import FlappyGame, SCREEN_WIDTH, SCREEN_HEIGHT, PIPE_GAP, GRAVITY, BIRD_JUMP, PIPE_SPEED

# Q-learning parameters
ALPHA = 0.1  # Learning rate
GAMMA = 0.99  # Discount factor
EPSILON_START = 1.0  # Exploration rate
EPSILON_END = 0.01
EPSILON_DECAY = 0.9995

# Discretization for state space
# vertical_distance: -SCREEN_HEIGHT to SCREEN_HEIGHT
# horizontal_distance: 0 to SCREEN_WIDTH
# velocity: BIRD_JUMP to some max positive velocity

# Define bins for state discretization
VERTICAL_DISTANCE_BINS = np.linspace(-SCREEN_HEIGHT, SCREEN_HEIGHT, 20)
HORIZONTAL_DISTANCE_BINS = np.linspace(0, SCREEN_WIDTH, 10)
VELOCITY_BINS = np.linspace(-10, 10, 10) # Adjust based on actual bird velocity range

def discretize_state(state):
    vertical_distance, horizontal_distance, velocity = state
    v_bin = np.digitize(vertical_distance, VERTICAL_DISTANCE_BINS)
    h_bin = np.digitize(horizontal_distance, HORIZONTAL_DISTANCE_BINS)
    vel_bin = np.digitize(velocity, VELOCITY_BINS)
    return (v_bin, h_bin, vel_bin)

class QLearningAgent:
    def __init__(self, actions=[0, 1]):
        self.q_table = {}
        self.actions = actions
        self.epsilon = EPSILON_START

    def get_q_value(self, state, action):
        return self.q_table.get((state, action), 0.0)

    def choose_action(self, state):
        if random.uniform(0, 1) < self.epsilon:
            return random.choice(self.actions)  # Explore
        else:
            # Exploit
            q_values = [self.get_q_value(state, action) for action in self.actions]
            max_q = max(q_values)
            # Handle cases where all Q-values are the same (e.g., all 0.0 initially)
            if q_values.count(max_q) > 1:
                best_actions = [i for i, q in enumerate(q_values) if q == max_q]
                return self.actions[random.choice(best_actions)]
            else:
                return self.actions[np.argmax(q_values)]

    def learn(self, state, action, reward, next_state):
        current_q = self.get_q_value(state, action)
        max_future_q = max([self.get_q_value(next_state, a) for a in self.actions])
        new_q = current_q + ALPHA * (reward + GAMMA * max_future_q - current_q)
        self.q_table[(state, action)] = new_q

    def decay_epsilon(self):
        self.epsilon = max(EPSILON_END, self.epsilon * EPSILON_DECAY)

def train_agent(episodes=10000):
    agent = QLearningAgent()
    env = FlappyGame(headless=True)
    scores = []
    average_scores = []

    for episode in range(episodes):
        env.reset_game()
        state = discretize_state(env.get_state())
        done = False
        episode_score = 0

        while not done:
            action = agent.choose_action(state)
            next_state_raw, reward, done, current_score = env.run_frame(action)
            next_state = discretize_state(next_state_raw)

            # Adjust reward for passing pipes
            if current_score > episode_score:
                reward = 5 # Reward for passing a pipe
            episode_score = current_score

            agent.learn(state, action, reward, next_state)
            state = next_state

        scores.append(episode_score)
        agent.decay_epsilon()

        if (episode + 1) % 100 == 0:
            avg_score = np.mean(scores[-100:])
            average_scores.append(avg_score)
            print(f"Episode {episode + 1}/{episodes}, Average Score (last 100): {avg_score:.2f}, Epsilon: {agent.epsilon:.4f}")

    # Save Q-table
    with open('q_table.pkl', 'wb') as f:
        pickle.dump(agent.q_table, f)
    print("Q-table saved to q_table.pkl")

    return agent.q_table, average_scores

if __name__ == '__main__':
    train_agent(episodes=10000)


