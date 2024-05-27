import sys
import os
# Add the parent directory to sys.path to allow for everdell_ai imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from everdell_ai.agent import ReinforcementLearningAgent

class AIPlayer(ReinforcementLearningAgent):      

    def __init__(self, alpha=0.1, gamma=0.9, epsilon=0.1, resources=10, wins=0):
        self.reset_agent()  # Reset all agent attributes to their initial values
        super().__init__(alpha, gamma, epsilon)
        self.wins = wins  # Initialize the number of wins for the AIPlayer
        self.hand_starting_amount = 5  # Initialize the hand limit for the AIPlayer
        self.card_to_play = None  # Initialize the card to play attribute
        self.resource_pick = None
        self.recalls = 0  # Initialize the recall count for the AIPlayer
        self.max_recalls = 3  # Maximum number of recalls allowed per game
        self.max_cards_in_hand = 8
        self.city_limit = 15
        self.prosperity_cards = []  # Initialize the list of prosperity cards for endgame scoring
        self.on_trigger = []  # Initialize the list of cards with effects that trigger when other cards are played

    def reset_agent(self):
        # Reset all agent attributes to zero, then set specific values
        self.tokens = 0
        self.workers = 2
        self.hand = []
        self.wood = 0
        self.resin = 0
        self.stone = 0
        self.berries = 0
        self.played_cards = []
        self.non_city_cards = []
        self.recalls = 0
        self.card_to_play = None
        self.resource_pick = None
        self.prosperity_cards = []  # Reset the list of prosperity cards for the next game
        self.on_trigger = []  # Reset the list of on trigger cards for the next game

    def receive_resources(self, resource_type):
        # Method to increase the agent's resources and return the received resource
        cards_to_draw = 0
        if resource_type == 'wood3':
            self.wood += 3
        elif resource_type == 'wood2_card':
            self.wood += 2
            cards_to_draw = 1
        elif resource_type == 'resin2':
            self.resin += 2
        elif resource_type == 'resin_card':
            self.resin += 1
            cards_to_draw = 1
        elif resource_type == 'card2_token':
            self.add_tokens(1)
            cards_to_draw = 2
        elif resource_type == 'stone':
            self.stone += 1
        elif resource_type == 'berry_card':
            self.berries += 1
            cards_to_draw = 1
        elif resource_type == 'berry':
            self.berries += 1
        self.workers -= 1  # Decrement a worker to receive resources
        return resource_type, cards_to_draw

    def add_tokens(self, amount):
        # Method to increase the agent's tokens
        self.tokens += amount

    def draw_to_hand(self, new_cards, *args):
        if new_cards != None:
            self.hand.extend(new_cards)

    def can_play_card(self, card, game):
        # Check if the card can be played based on available resources and return the action
        unique_card_already_played = card.rarity == "unique" and card.name != "Fool" and any(played_card.name == card.name for played_card in self.played_cards)
        innkeeper_card = next((played_card for played_card in self.played_cards if played_card.name == "Innkeeper"), None)
        can_use_innkeeper = innkeeper_card and card.card_type == 'character' and self.resources_less_than_cost(card) and self.resources_at_least_reduced_cost(card)
        crane_card = next((played_card for played_card in self.played_cards if played_card.name == "Crane"), None)
        can_use_crane = crane_card and self.resources_less_than_cost(card) and self.resources_at_least_reduced_cost(card)
        if unique_card_already_played:
            return None
        elif (card.name == "Fool" and card.berries <= self.berries and any(len(agent.played_cards) < self.city_limit for agent in game.agents)):
            return ('play_card', card)
        elif (card.wood <= self.wood and card.resin <= self.resin and card.stone <= self.stone and card.berries <= self.berries and len(self.played_cards) < self.city_limit):
            return ('play_card', card)
        elif can_use_innkeeper:
            return ('play_card_with_innkeeper', card, innkeeper_card)
        elif can_use_crane:
            return ('play_card_with_crane', card, crane_card)
        else:
            return None

    def resources_less_than_cost(self, card):
        return (card.wood < self.wood or card.resin < self.resin or card.stone < self.stone or card.berries < self.berries)

    def resources_at_least_reduced_cost(self, card):
        return ((self.wood + self.resin + self.stone + self.berries) >= max((card.wood + card.resin + card.stone + card.berries) - 3, 0))

    def determine_available_actions(self, hand, meadow, game):
        # Determine the available actions for the AI player, including playing cards and receiving resources
        available_actions = []
        for card in hand + meadow:
            can_play = self.can_play_card(card, game)
            if can_play:
                available_actions.append(can_play)
        # Add the 'receive_resources' action only if there are workers available
        if self.workers > 0:
            for resource_type in ['wood3', 'wood2_card', 'resin2', 'resin_card', 'card2_token', 'stone', 'berry_card', 'berry']:
                available_actions.append(('receive_resources', resource_type))
        # Add the 'recall_workers' action only if the agent can recall workers
        if self.workers == 0 and self.recalls < self.max_recalls:
            available_actions.append(('recall_workers', None))
        action = self.choose_action(available_actions)
        if action and action[0] == 'play_card_with_innkeeper':
            self.card_to_play = action[1]
            self.innkeeper_card_to_discard = action[2]
        elif action and action[0] == 'play_card':
            self.card_to_play = action[1]
            self.innkeeper_card_to_discard = None
        else:
            self.card_to_play = None
            self.innkeeper_card_to_discard = None
        self.resource_pick = action[1] if action and action[0] == 'receive_resources' else None
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
                if card.name == "Fool":
                    reward = -card.points * 0.01  # Reverse reward for fool
                else:
                    reward = card.points * 0.01  # Small reward for the card's point value

            
        return reward
