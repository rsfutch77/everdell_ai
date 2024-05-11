from agent import ReinforcementLearningAgent
import numpy as np
import matplotlib.pyplot as plt
import time
from player import AIPlayer
import random

class Game:

    def __init__(self, deck, agents, turn_update_callback=None, ui_root=None, time_to_wait_entry=None):
        self.time_to_wait_entry = time_to_wait_entry
        self.turn_update_callback = turn_update_callback
        self.ui_root = ui_root
        self.initial_deck = list(deck)  # Store the initial state of the deck
        self.deck = deck
        self.agents = agents if all(isinstance(agent, AIPlayer) for agent in agents) else [AIPlayer() for _ in range(2)]
        self.turns = 5
        self.current_turn = 0
        self.ties = 0
        # Initialize resources for each agent
        for agent in self.agents:
            agent.resources = 10
            agent.played_cards = []  # Reset the played cards for each agent
            agent.wins = 0
    
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

        return tie_calculator, winner, winner_index
    
    def train(self, num_episodes):
        self.ties = 0
        for episode in range(num_episodes):
            self.reset_game()
            while not self.is_game_over():
                self.play_turn()
                # After each turn, update the AI's knowledge
                state = self.get_numerical_game_state()
                action = self.agents[0].select_card(self.deck, state)
                done = self.is_game_over()
                next_state = self.get_numerical_game_state()
                for agent_index, agent in enumerate(self.agents):
                    reward = agent.get_reward(self, action, done, agent_index, self.ties)
                    agent.learn(state, action, reward, next_state, done)

            tie_calculator, winner, winner_index = self.get_winner(self)

            #Apply record of wins and ties
            if tie_calculator > 1:
                self.ties += 1
            else:
                self.agents[winner].wins += 1
                

            print(f"Episode {episode + 1}:")
            for win_rate_index, agent in enumerate(self.agents):
                win_rate = agent.wins / (episode + 1)
                agent.win_rates.append(win_rate)
                print(f"AI {win_rate_index} score: {agent.score},")
                print(f"AI {win_rate_index} Win Rate: {agent.wins / (episode + 1):.2%}")
            print(f"Ties: {self.ties / (episode + 1):.2%}")
        

        # Save the AI model after training
        self.agents[0].save_model('ai_model.pkl')
        # Plot the win rates over episodes
        for agent in self.agents:
            plt.plot(agent.win_rates)
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
