from agent import ReinforcementLearningAgent
import numpy as np
import matplotlib.pyplot as plt
import time
from player import AIPlayer
import random

class Game:

    def __init__(self, deck, agents, randomize_agents, turn_update_callback=None, ui_root=None, time_to_wait_entry=None):
        self.time_to_wait_entry = time_to_wait_entry
        self.turn_update_callback = turn_update_callback
        self.ui_root = ui_root
        self.initial_deck = list(deck)  # Store the initial state of the deck
        self.deck = deck
        self.agents = agents if all(isinstance(agent, AIPlayer) for agent in agents) else [AIPlayer(wins=0) for _ in range(2)]
        self.current_turn = 0
        self.ties = 0
        self.randomize_agents = randomize_agents  # Store the randomize_agents variable
        # Initialize resources for each agent
        for agent in self.agents:
            agent.resources = 10
            agent.played_cards = []  # Reset the played cards for each agent

    def get_winner(self, game):

        agents = game.agents  # Access the agents from the game object
        for agent in agents:
            scores = game.calculate_score()
            agent.score = scores[agents.index(agent)]  # Assign the individual score

        # Find the highest Score
        winner = -1 #Initialize
        winning_score = 0 #Initialize
        for winner_index, agent in enumerate(agents):
            if agent.score and agent.score > winning_score:
                winning_score = agent.score
                winner = winner_index

        #Check for ties
        tie_calculator = 0 #Initialize
        for agent in agents:
            if agent.score == winning_score:
                tie_calculator += 1

        return tie_calculator, winner

    def train(self, num_episodes):
        self.ties = 0
        # Initialize a list to store the average TD errors for all episodes
        all_episodes_td_errors = []
        for episode in range(num_episodes):
            # Randomize the number of agents for each episode if enabled
            if self.randomize_agents.get():
                number_of_agents = random.randint(2, 4)  # Randomly choose between 2, 3, or 4 agents
                self.agents = [AIPlayer(alpha=0.1, gamma=0.9, epsilon=0.1) for _ in range(number_of_agents)]
            for agent in self.agents:
                agent.update_epsilon(episode, num_episodes)
            else:
                number_of_agents = len(self.agents)  # Use the predefined number of agents
            self.reset_game()
            while not self.is_game_over():
                state = self.get_numerical_game_state()  # Capture the state before the turn
                self.play_turn()
                next_state = self.get_numerical_game_state()  # Capture the state after the turn
                done = self.is_game_over()
                # After each turn, update the AI's knowledge
                for agent_index, agent in enumerate(self.agents):
                    action = 'play_card' if agent.card_to_play else 'receive_resources'
                    reward = agent.get_reward(self, action, done, agent_index, self.ties)
                    agent.learn(state, action, reward, next_state, done)

            # Collect and average TD errors for the episode
            if self.randomize_agents.get():
                episode_td_errors = [agent.td_errors[-1] for agent in self.agents if agent.td_errors]
                average_td_error = sum(episode_td_errors) / len(episode_td_errors) if episode_td_errors else 0
                all_episodes_td_errors.append(average_td_error)  # Store the average TD error for the episode

            tie_calculator, winner, winner_index = self.get_winner(self)

            #Apply record of wins and ties
            if tie_calculator > 1:
                self.ties += 1
            else:
                self.agents[winner].wins += 1


            print(f"Episode {episode + 1}:")
            for agent in self.agents:
                win_rate = agent.wins / (episode + 1)
                agent.win_rates.append(win_rate)
                print(f"AI {self.agents.index(agent)} score: {agent.score},")
                if not self.randomize_agents.get():
                    print(f"AI {self.agents.index(agent)} Win Rate: {agent.wins / (episode + 1):.2%}")
            print(f"Ties: {self.ties / (episode + 1):.2%}")


        # Save the AI model after training
        if not self.randomize_agents.get():
            plt.figure()  # Create a new figure
            for agent in self.agents:
                plt.plot(agent.td_errors)
        else:
            plt.figure()  # Create a new figure for agent[0] only
            x_values = range(1, num_episodes + 1)
            plt.plot(x_values, all_episodes_td_errors, marker='o')  # Plot TD errors with markers for clarity
            # Calculate and plot the trendline
            z = np.polyfit(x_values, all_episodes_td_errors, 1)
            p = np.poly1d(z)
            plt.plot(x_values, p(x_values), "r--")  # Plot the trendline
        plt.title('TD Error Over Time')
        plt.xlabel('Learning Step')
        plt.ylabel('TD Error')

        if not self.randomize_agents.get():
            # Plot the win rates over episodes
            plt.figure()  # Create a new figure
            for agent in self.agents:
                plt.plot(agent.win_rates)
            plt.title('AI Win Rate Over Time')
            plt.xlabel('Episode')
            plt.ylabel('Win Rate')

        plt.show()

        self.agents[0].save_model('ai_model.pkl')

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
        # The game is over when the deck is empty or when all players have no workers left and cannot play any cards
        if len(self.deck) == 0:
            return True
        for agent in self.agents:
            # Check if the agent can play a card or has workers left
            if agent.workers > 0 or any(agent.can_play_card(card) for card in self.deck):
                return False
        return True

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
        for agent in self.agents:
            print(f"Starting turn with AI {self.agents.index(agent)} resources: {agent.resources}")
            print(f"AI {self.agents.index(agent)} has {agent.workers} workers remaining.")
        print(f"Deck size before turn: {len(self.deck)}")

        # AI attempts to select an action
        numerical_game_state = self.get_numerical_game_state()
        print(f"Numerical game state: {numerical_game_state}")
        for agent in self.agents:
            selected_action = agent.select_action(self.deck, numerical_game_state) or (None, None)
            action, card = selected_action
            if action == 'play_card' and card:
                agent.resources -= card.cost  # Deduct the cost from the AI player's resources
                print(f"AI {self.agents.index(agent)} plays {card.name} costing {card.cost}. Remaining resources: {agent.resources}.")
                if card in self.deck:
                    self.deck.remove(card)
                    agent.played_cards.append(card)
            elif action == 'receive_resources':
                if agent.workers > 0:  # Check if the agent has workers available
                    resources_received = 3  # Define the amount of resources received when choosing to receive resources
                    agent.receive_resources(resources_received)
                    print(f"AI {self.agents.index(agent)} receives {resources_received} resources. Total resources: {agent.resources}")
                else:
                    print(f"AI {self.agents.index(agent)} has no workers left to receive resources.")
            else:
                print(f"AI {self.agents.index(agent)} cannot play a card this turn.")
                agent.card_to_play = None

        print(f"Deck size after turn: {len(self.deck)}")
        self.current_turn += 1
        if self.is_game_over():
            print("No player has any moves left. The game is over.")

    def get_game_state(self):
        # Placeholder for more complex game state
        return {'turn': self.current_turn, 'played_cards': self.played_cards}

    def calculate_score(self):
        scores = [sum(card.points for card in agent.played_cards) for agent in self.agents]
        return scores
