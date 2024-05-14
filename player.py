import sys
import os
# Add the parent directory to sys.path to allow for everdell_ai imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from everdell_ai.agent import ReinforcementLearningAgent

class AIPlayer(ReinforcementLearningAgent):      

    def __init__(self, alpha=0.1, gamma=0.9, epsilon=0.1, resources=10, wins=0):
        super().__init__(alpha, gamma, epsilon, resources)
        self.wins = wins  # Initialize the number of wins for the AIPlayer
        self.workers = 2  # Initialize the number of workers for the AIPlayer
        self.hand = []  # Initialize the hand of cards for the AIPlayer
        self.hand_starting_amount = 5  # Initialize the hand limit for the AIPlayer
        self.card_to_play = None  # Initialize the card to play attribute

    def receive_resources(self, amount):
        # Method to increase the agent's resources
        self.resources += amount
        self.workers -= 1  # Spend a worker to receive resources

    def can_play_card(self, card):
        # Check if the card can be played based on available resources and return the action
        if card in self.hand and card.cost <= self.resources:
            return ('play_card', card)
        else:
            # Only return the 'receive_resources' action if there are workers available
            if self.workers > 0:
                return ('receive_resources', None)
            return None

    def select_action(self, hand, meadow, numerical_game_state):
        # The game_state parameter should be a numerical representation
        # Meadow is a list of cards available to all players
        state = numerical_game_state
        # Include an additional action for receiving resources
        available_actions = [('play_card', card) for card in hand + meadow if card.cost <= self.resources]
        # Add the 'receive_resources' action only if there are workers available
        if self.workers > 0:
            available_actions.append(('receive_resources', None))
        action = self.choose_action(available_actions)
        self.card_to_play = action[1] if action and action[0] == 'play_card' else None
        return action
    
    def get_reward(self, game, action, done, agent_index):
        # Reward function that gives a small reward for playing a high point value card,
        # a penalty for not playing a card, and a larger reward for winning the game.
        # and a larger reward for winning the game.
        agents = game.agents  # Access the agents from the game object
        reward = 0  

        if done:
            tie_calculator, winner = game.get_winner(game)
            if tie_calculator > 1 and agents[agent_index].score == agents[winner].score:
                reward += 0.5  # Smaller reward for a tie
            elif agent_index == winner:
                reward += 1.0  # Large reward for winning
            else:
                reward = 0 # No additional reward or penalty if the AI loses
        elif action == 'receive_resources':
            reward = 0  # No reward for not playing a card
        elif action == 'play_card':
            card = game.agents[agent_index].card_to_play  # Assuming card_to_play is now an instance of Card
            if card:
                reward = card.points * 0.01  # Small reward for the card's point value


            
        return reward
