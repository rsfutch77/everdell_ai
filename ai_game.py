class Card:
    def __init__(self, name, points, cost):
        self.name = name
        self.points = points
        self.cost = cost  # Assign the fixed cost

import numpy as np
import random
from collections import defaultdict
import pickle

def default_q_value():
    return defaultdict(float)


class ReinforcementLearningAgent:
    def __init__(self, alpha=0.1, gamma=0.9, epsilon=0.1, resources=10):
        self.alpha = alpha  # learning rate
        self.gamma = gamma  # discount factor
        self.epsilon = epsilon  # exploration rate
        self.played_cards = []  # Initialize the list of played cards for the agent
        self.q_table = defaultdict(default_q_value)
        self.resources = resources  # Initialize resources for the agent    
    
    def can_play_card(self, card, game_state=None):
        # Check if the card can be played based on available resources
        return card.cost <= self.resources

    def select_card(self, hand, numerical_game_state):
        # The game_state parameter should be a numerical representation
        state = numerical_game_state
        available_actions = [i for i, card in enumerate(hand) if card.cost <= self.resources]  # Filter for affordable cards
        action_index = self.choose_action(available_actions)
        action = hand[action_index] if available_actions else None
        return action

    def choose_action(self, state):
        state = tuple(state)  # Convert list to tuple to use as a key
        if random.uniform(0, 1) < self.epsilon:
            # Explore: choose a random action
            return random.choice(list(state))
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

    def learn(self, state, action, reward, next_state, done):
        state = tuple(state)  # Convert list to tuple to use as a key
        next_state = tuple(next_state)  # Convert list to tuple to use as a key
        # Update Q-value using the Bellman equation
        old_value = self.q_table[state][action]
        next_max = max(self.q_table[next_state].values()) if not done else 0
        new_value = (1 - self.alpha) * old_value + self.alpha * (reward + self.gamma * next_max)
        self.q_table[state][action] = new_value

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

    def choose_action(self, state):
        state = tuple(state)  # Convert list to tuple to use as a key
        if random.uniform(0, 1) < self.epsilon:
            # Explore: choose a random action
            return random.choice(list(state))
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

    def learn(self, state, action, reward, next_state, done):
        state = tuple(state)  # Convert list to tuple to use as a key
        next_state = tuple(next_state)  # Convert list to tuple to use as a key
        # Update Q-value using the Bellman equation
        old_value = self.q_table[state][action]
        next_max = max(self.q_table[next_state].values()) if not done else 0
        new_value = (1 - self.alpha) * old_value + self.alpha * (reward + self.gamma * next_max)
        self.q_table[state][action] = new_value

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

    def get_reward(self, game, action, done):
        # Reward function that gives a small reward for playing a high point value card,
        # a penalty for not playing a card, and a larger reward for winning the game.
        if action is not None:
            reward = action.points * 0.1  # Small reward for the card's point value
        else:
            reward = -0.1  # Penalty for not playing a card
        if done:
            ai_score, adversarial_ai_score = game.calculate_score()
            if ai_score > adversarial_ai_score:
                reward += 1.0  # Large reward for winning
            elif ai_score == adversarial_ai_score:
                reward += 0.5  # Smaller reward for a tie
            # No additional reward or penalty if the AI loses
        return reward



class AIPlayer(ReinforcementLearningAgent):    
    
    def can_play_card(self, card, game_state=None):
        # Check if the card can be played based on available resources
        return card.cost <= self.resources

    def select_card(self, hand, numerical_game_state):
        # The game_state parameter should be a numerical representation
        state = numerical_game_state
        available_actions = [i for i, card in enumerate(hand) if card.cost <= self.resources]  # Filter for affordable cards
        action_index = self.choose_action(available_actions)
        action = hand[action_index] if available_actions else None
        return action



import matplotlib.pyplot as plt
import time

class Game:

    def __init__(self, deck, agents, turn_update_callback=None, ui_root=None, time_to_wait_entry=None):
        self.time_to_wait_entry = time_to_wait_entry
        self.turn_update_callback = turn_update_callback
        self.ui_root = ui_root
        self.initial_deck = list(deck)  # Store the initial state of the deck
        self.deck = deck
        self.agents = agents if all(isinstance(agent, ReinforcementLearningAgent) for agent in agents) else [ReinforcementLearningAgent() for _ in range(2)]
        self.turns = 5
        self.current_turn = 0
        # Initialize resources for each agent
        for agent in self.agents:
            agent.resources = 10
            agent.played_cards = []  # Reset the played cards for each agent
            agent.wins = 0


    def train(self, num_episodes):
        ties = 0
        for episode in range(num_episodes):
            self.reset_game()
            while not self.is_game_over():
                self.play_turn()
                # After each turn, update the AI's knowledge
                state = self.get_numerical_game_state()
                action = self.agents[0].select_card(self.deck, state)
                done = self.is_game_over()
                next_state = self.get_numerical_game_state()
                for agent in self.agents:
                    reward = agent.get_reward(self, action, done)
                    agent.learn(state, action, reward, next_state, done)
                    agent.win_rates = []  # Store win rates after each episode
                    agent.wins
            # Log the results of the episode if necessary
            ai_score, adversarial_ai_score = self.calculate_score()
            if ai_score > adversarial_ai_score:
                ai_wins += 1
            elif ai_score < adversarial_ai_score:
                adversarial_ai_wins += 1
            else:
                ties += 1
            win_rate = ai_wins / (episode + 1)
            win_rates.append(win_rate)
            print(f"Episode {episode + 1}: AI score: {ai_score}, Adversarial AI score: {adversarial_ai_score}")
        # Save the AI model after training
        self.agents[0].save_model('ai_model.pkl')
        print(f"AI Win Rate: {ai_wins / num_episodes:.2%}")
        print(f"Adversarial AI Win Rate: {adversarial_ai_wins / num_episodes:.2%}")
        print(f"Ties: {ties / num_episodes:.2%}")
        # Plot the win rates over episodes
        plt.plot(win_rates)
        plt.title('AI Win Rate Over Time')
        plt.xlabel('Episode')
        plt.ylabel('Win Rate')
        plt.show()
    def reset_game(self):
        self.current_turn = 0
        self.deck = list(self.initial_deck)  # Reset the deck to its initial state
        self.played_cards = []
        for agent in self.agents:
            agent.resources = 10
            agent.played_cards = []  # Reset the played cards for each agent
        # Shuffle the deck or reset it to its initial state
        random.shuffle(self.deck)

    def is_game_over(self):
        return self.current_turn >= self.turns
        for _ in range(self.turns):
            self.play_turn()

    def get_numerical_game_state(self):
        # Convert the game state into a numerical representation for the AI
        state_representation = []
        # Include the current turn as a feature
        state_representation.append(self.current_turn)
        # Include the points and costs of cards in hand as features
        hand_features = [(card.points, card.cost) for card in self.deck]
        for points, cost in hand_features:
            state_representation.extend([points, cost])
        # Include the points of played cards as features
        played_points = [card.points for card in self.played_cards]
        state_representation.extend(played_points)
        # Normalize or scale the features if necessary
        # ...
        return state_representation

    def play_turn(self):
        if self.turn_update_callback:
            self.turn_update_callback(self.current_turn)
        if self.ui_root:
            self.ui_root.update_idletasks()
            self.ui_root.update()
            try:
                # Read the value from the time_to_wait_entry and convert it to a float
                time_to_wait = float(self.time_to_wait_entry.get())
            except ValueError:
                # If the value is not a valid float, default to 1 second
                time_to_wait = 1.0
            time.sleep(time_to_wait)  # Sleep for the specified number of seconds
        print(f"Turn {self.current_turn + 1}:")
        if not self.deck:
            print("The deck is empty. The game is over.")
            return
        for index, agent in enumerate(self.agents):
            print(f"Starting turn with AI {index} resources: {agent.resources}")
        print(f"Deck size before turn: {len(self.deck)}")
        if all(not any(card.cost <= agent.resources for card in self.deck) for agent in self.agents):
            print("No cards in the deck are affordable for any player.")
            print("No player has enough resources to play a card. The game is over.")
            self.current_turn = self.turns  # Set current turn to the total number of turns to end the game
            return
        else:
            # AI attempts to select and play a card
            numerical_game_state = self.get_numerical_game_state()
            print(f"Numerical game state: {numerical_game_state}")
            for agent in self.agents:
                agent.card_to_play = agent.select_card(self.deck, numerical_game_state)
                print(f"AI attempting to play: {agent.card_to_play.name if agent.card_to_play else 'None'}")
                if agent.card_to_play and agent.can_play_card(agent.card_to_play):
                        agent.resources -= agent.card_to_play.cost  # Deduct the cost from the AI player's resources
                        print(f"AI plays {agent.card_to_play.name} costing {agent.card_to_play.cost}. Remaining resources: {agent.resources}.")
                        if agent.card_to_play in self.deck:
                            self.deck.remove(agent.card_to_play)
                            agent.played_cards.append(agent.card_to_play)
                else:
                    print("AI cannot play a card this turn.")
                    agent.card_to_play = None
        print(f"Deck size after turn: {len(self.deck)}")
        self.current_turn += 1

    def get_game_state(self):
        # Placeholder for more complex game state
        return {'turn': self.current_turn, 'played_cards': self.played_cards}

    def calculate_score(self):
        scores = [sum(card.points for card in agent.played_cards) for agent in self.agents]
        return scores
