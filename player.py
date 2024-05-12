import sys
import os
# Add the parent directory to sys.path to allow for everdell_ai imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from everdell_ai.agent import ReinforcementLearningAgent

class AIPlayer(ReinforcementLearningAgent):      

    def __init__(self, alpha=0.1, gamma=0.9, epsilon=0.1, resources=10, wins=0):
        super().__init__(alpha, gamma, epsilon, resources)
        self.wins = wins  # Initialize the number of wins for the AIPlayer
        self.card_to_play = None  # Initialize the card to play attribute

    def receive_resources(self, amount):
        # Method to increase the agent's resources
        self.resources += amount

    def can_play_card(self, card):
        # Check if the card can be played based on available resources and return the action
        if card.cost <= self.resources:
            return ('play_card', card)
        else:
            return ('receive_resources', None)

    def select_action(self, hand, numerical_game_state):
        # The game_state parameter should be a numerical representation
        state = numerical_game_state
        # Include an additional action for receiving resources
        available_actions = [('play_card', card) for card in hand if card.cost <= self.resources]
        available_actions.append(('receive_resources', None))  # Add the 'receive_resources' action
        action = self.choose_action(available_actions)
        self.card_to_play = action[1] if action and action[0] == 'play_card' else None
        return action
    
    def get_reward(self, game, action, done, agent_index, ties):
        # Reward function that gives a small reward for playing a high point value card,
        # a penalty for not playing a card, and a larger reward for winning the game.
        # and a larger reward for winning the game.
        agents = game.agents  # Access the agents from the game object
        reward = 0  

        if done:
            tie_calculator, winner, winner_index = game.get_winner(game)
            if tie_calculator > 1 and agents[agent_index].score == agents[winner_index].score:
                reward += 0.5  # Smaller reward for a tie
            elif agent_index == winner:
                reward += 1.0  # Large reward for winning
            else:
                reward = 0 # No additional reward or penalty if the AI loses
        elif action == 'receive_resources':
            reward = 0  # No reward for not playing a card
        elif action == 'play_card':
            card = game.agents[agent_index].card_to_play
            if card:
                reward = card.points * 0.01  # Small reward for the card's point value


            
        return reward
