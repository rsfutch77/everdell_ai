from agent import ReinforcementLearningAgent

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
    
    def get_reward(self, game, action, done, agent_index, ties):
        # Reward function that gives a small reward for playing a high point value card,
        # a penalty for not playing a card, and a larger reward for winning the game.
        agents = game.agents  # Access the agents from the game object
        if action is not None:
            reward = action.points * 0.1  # Small reward for the card's point value
        else:
            reward = -0.1  # Penalty for not playing a card
        if done:

            tie_calculator, winner, winner_index = game.get_winner(game)
            
            if tie_calculator > 1 and agents[agent_index].score == agents[winner_index].score:
                reward += 0.5  # Smaller reward for a tie
            elif agent_index == winner:
                reward += 1.0  # Large reward for winning
            # No additional reward or penalty if the AI loses
            
        return reward
