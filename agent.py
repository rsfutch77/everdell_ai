import random
import math
from collections import defaultdict
import pickle

def default_q_value():
    return defaultdict(float)

class ReinforcementLearningAgent:
    def __init__(self, alpha=0.1, gamma=0.9, epsilon=0.1, resources=10):
        self.alpha = alpha  # learning rate
        self.td_errors = []  # Initialize the list to track temporal difference errors
        self.gamma = gamma  # discount factor
        self.epsilon = epsilon  # exploration rate
        self.initial_epsilon = epsilon  # Store the initial exploration rate
        self.played_cards = []  # Initialize the list of played cards for the agent
        self.q_table = defaultdict(default_q_value)
        self.resources = resources  # Initialize resources for the agent    
        self.win_rates = []  # Initialize the list to track win rates over episodes

    def learn(self, state, action, reward, next_state, done):
        state = tuple(state)  # Convert list to tuple to use as a key
        next_state = tuple(next_state)  # Convert list to tuple to use as a key
        # Update Q-value using the Bellman equation
        old_value = self.q_table[state][action]
        next_max = max(self.q_table[next_state].values()) if not done else 0
        new_value = (1 - self.alpha) * old_value + self.alpha * (reward + self.gamma * next_max)
        self.q_table[state][action] = new_value
        self.td_errors.append(abs(old_value - new_value))  # Store the TD error

    def update_epsilon(self, episode, total_episodes):
        # Decaying epsilon over episodes
        self.epsilon = self.initial_epsilon * math.exp(-10 * episode / total_episodes)

    def save_model(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump({
                'q_table': self.q_table,
                'alpha': self.alpha,
                'gamma': self.gamma,
                'epsilon': self.epsilon
            }, file)

    def load_model(self, filename):
        with open(filename, 'rb') as file:
            data = pickle.load(file)
            self.q_table = data['q_table']
            self.alpha = data['alpha']
            self.gamma = data['gamma']
            self.epsilon = data['epsilon']

    def choose_action(self, available_actions):
        if not available_actions:
            # If there are no available actions, return None
            return None
        if random.uniform(0, 1) < self.epsilon:
            # Explore: choose a random action from the available actions
            return random.choice(available_actions)
        # Exploit: choose the best action based on past experience
        q_values = {action: self.q_table[tuple(available_actions)][action] for action in available_actions if action in self.q_table[tuple(available_actions)]}
        if q_values:
            max_q_value = max(q_values.values())
            best_actions = [action for action, q in q_values.items() if q == max_q_value]
            return random.choice(best_actions)
        # If there are no known Q-values, choose randomly among the available actions
        return random.choice(available_actions)
