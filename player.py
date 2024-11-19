import sys
import os
import tkinter as tk
from tkinter import messagebox
from cards import lookout_trigger_effect
# Add the parent directory to sys.path to allow for everdell_ai imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from everdell_ai.agent import ReinforcementLearningAgent

class AIPlayer(ReinforcementLearningAgent):      

    def __init__(self, alpha=0.01, gamma=0.9, epsilon=0.1, wins=0):
        self.reset_agent()  # Reset all agent attributes to their initial values
        super().__init__(alpha, gamma, epsilon)
        self.wins = wins  # Initialize the number of wins for the AIPlayer
        self.hand_starting_amount = 5  # Initialize the hand limit for the AIPlayer
        self.card_to_play = None  # Initialize the card to play attribute
        self.resource_pick = None
        self.recalls = 0  # Initialize the recall count for the AIPlayer
        self.max_recalls = 3  # Maximum number of recalls allowed per game
        self.max_cards_in_hand = 8
        self.max_workers = 2  # Set the maximum number of workers
        self.city_limit = 15
        self.worker_allocation = {  # Initialize the worker allocation for each resource
            'wood3': 0, 'wood2_card': 0, 'resin2': 0, 'resin_card': 0,
            'card2_token': 0, 'stone': 0, 'berry_card': 0, 'berry': 0, 'lookout': 0
        }
        self.berries_given_during_monk_activation = 0  # Track berries given during Monk's activation
        self.event_tickets = 0  # Initialize the event tickets count
        self.prosperity_cards = []  # Initialize the list of prosperity cards for endgame scoring
        self.on_trigger = []  # Initialize the list of cards with effects that trigger when other cards are played

    def update_learning_rate(self, episode, total_episodes):
        # Implement a learning rate schedule that decreases over time
        self.alpha = self.alpha * (1 - episode / total_episodes)

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
        self.event_tickets = 0  # Reset the event tickets count for the next game
        self.prosperity_cards = []  # Reset the list of prosperity cards for the next game
        self.on_trigger = []  # Reset the list of on trigger cards for the next game


    def receive_resources(self, resource_type, game):
        if resource_type in game.forest:
            resource_type.trigger(self, game, None)  # Trigger the forest card effect
            self.workers -= 1  # Deduct a worker
            print(f"AI {game.agents.index(self)} places a worker on {resource_type.name} and receives its benefit.")
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
        if resource_type == 'lookout':
            lookout_trigger_effect(self, game, None)
        self.workers -= 1  # Decrement a worker to receive resources
        self.worker_allocation[resource_type] += 1  # Increment the worker count for the resource
        game.worker_slots_available[resource_type] -= 1
        # Check if worker slots available went below zero
        if game.worker_slots_available[resource_type] < 0:
            raise Exception(f"Worker slots for {resource_type} went below zero.")
        
        return resource_type, cards_to_draw

    def choose_berries_to_give(self, max_berries, game):
        # AI logic to decide how many berries to give
        # Use the AI's choose_action method to decide how many berries to give
        available_actions = list(range(max_berries + 1))  # Options: 0 to max_berries
        action = self.choose_action(available_actions)
        chosen_berries = action if action is not None else 0  # Default to 0 if no action is chosen
        game.berry_give_choices[chosen_berries] += 1  # Update the berry give choices frequency
        return chosen_berries

    def add_tokens(self, amount):
        # Method to increase the agent's tokens
        self.tokens += amount
        print(f"Player receives {amount} tokens.")

    def draw_to_hand(self, new_cards, game, *args):
        if new_cards is not None:
            # Only add cards up to the maximum hand limit
            cards_to_add = min(len(new_cards), self.max_cards_in_hand - len(self.hand))
            self.hand.extend(new_cards[:cards_to_add])
            # Discard any excess cards that couldn't be added to the hand
            excess_cards = new_cards[cards_to_add:]
            if excess_cards:
                print(f"Discarding excess cards when the next AI made the following move: {[card.name for card in excess_cards]}")
                game.discard_cards(excess_cards)

    def can_play_card(self, card, game):
        # Check if the card can be played based on available resources and return the action
        unique_card_already_played = card.rarity == "unique" and card.name != "Fool" and any(played_card.name == card.name for played_card in self.played_cards)
        innkeeper_card = next((played_card for played_card in self.played_cards if played_card.name == "Innkeeper"), None)
        can_use_innkeeper = innkeeper_card and card.card_type == 'character' and self.resources_less_than_cost(card) and self.resources_at_least_reduced_cost(card)
        crane_card = next((played_card for played_card in self.played_cards if played_card.name == "Crane"), None)
        can_use_crane = crane_card and self.resources_less_than_cost(card) and self.resources_at_least_reduced_cost(card)
        judge_card = next((played_card for played_card in self.played_cards if played_card.name == "Judge"), None)
        can_use_judge = judge_card and self.determine_swapped_resources(card, check_only=True)
        if (card.name == "Fool" and card.berries <= self.berries and any(len(agent.played_cards) < self.city_limit and not any(card.name == "Fool" for card in agent.played_cards) for agent in game.agents)):
            return ('play_card', card)
        elif len(self.played_cards) > self.city_limit:
            return None
        elif unique_card_already_played:
            return None
        elif (card.wood <= self.wood and card.resin <= self.resin and card.stone <= self.stone and card.berries <= self.berries):
            return ('play_card', card)
        elif can_use_innkeeper:
            return ('play_card_with_innkeeper', card, innkeeper_card)
        elif can_use_crane:
            return ('play_card_with_crane', card, crane_card)
        elif can_use_judge:
            return ('play_card_with_judge', card, judge_card)
        else:
            return None

    def determine_swapped_resources(self, card, check_only=False):
        # Determine the swapped resources for the Judge card and check if the resources meet at least the reduced cost
        for resource in ['wood', 'resin', 'stone', 'berries']:
            if getattr(self, resource) > 0:
                for target_resource in ['wood', 'resin', 'stone', 'berries']:
                    if resource != target_resource:
                        swapped_resources = {
                            'wood': self.wood - 1 if resource == 'wood' else self.wood,
                            'resin': self.resin - 1 if resource == 'resin' else self.resin,
                            'stone': self.stone - 1 if resource == 'stone' else self.stone,
                            'berries': self.berries - 1 if resource == 'berries' else self.berries,
                            target_resource: getattr(self, target_resource) + 1
                        }
                        if (swapped_resources['wood'] >= card.wood and
                            swapped_resources['resin'] >= card.resin and
                            swapped_resources['stone'] >= card.stone and
                            swapped_resources['berries'] >= card.berries):
                            #Fix all the swapped resources here becuase I don't understand what this funciton is above
                            #Target resource is what we need
                            #Resource is what we have extra of
                            #It fails to subtract the cost of the target resource from the card
                            #It seems to add all of the agent's other resources, except then it subtracts 1 from the resource that we are swapping
                            #So what we do here is set swapped resources back to the card's orginial values, subtract 1 target, and add one resource
                            swapped_resources['wood'] = card.wood
                            swapped_resources['resin'] = card.resin
                            swapped_resources['stone'] = card.stone
                            swapped_resources['berries'] = card.berries
                            swapped_resources[target_resource] = getattr(card, target_resource) - 1
                            swapped_resources[resource] = getattr(card, resource) + 1
                            if check_only:
                                return True
                            return swapped_resources
        return False
    
    def resources_less_than_cost(self, card):
        return (card.wood > self.wood or card.resin > self.resin or card.stone > self.stone or card.berries > self.berries)

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
            if any(card.name == "Lookout" for card in self.played_cards):
                if game.worker_slots_available['lookout'] > 0:
                    available_actions.append(('receive_resources', 'lookout'))
            for resource_type in ['wood3', 'wood2_card', 'resin2', 'resin_card', 'card2_token', 'stone', 'berry_card', 'berry']:
                if game.worker_slots_available[resource_type] > 0:
                    available_actions.append(('receive_resources', resource_type))
            # Add basic events actions
            basic_events = []
            # Check for the monument action
            blue_cards_count = sum(1 for card in self.played_cards if card.card_type == 'construction' and card.rarity == 'unique')
            if blue_cards_count >= 3 and 'monument' not in game.claimed_events:
                basic_events.append('monument')
            # Check for the red card event
            red_cards_count = sum(1 for card in self.played_cards if card.card_color == 'red')
            if red_cards_count >= 3 and 'tour' not in game.claimed_events:
                basic_events.append('tour')
            # Check for the green card event
            green_cards_count = sum(1 for card in self.played_cards if card.card_color == 'green')
            if green_cards_count >= 3 and 'festival' not in game.claimed_events:
                basic_events.append('festival')
            # Check for the tan card event
            tan_cards_count = sum(1 for card in self.played_cards if card.card_color == 'tan')
            if tan_cards_count >= 3 and 'expedition' not in game.claimed_events:
                basic_events.append('expedition')
            # Add basic events to available actions
            for event in basic_events:
                available_actions.append(('basic_event', event))

        if (self.workers == 0 or all(game.worker_slots_available[resource_type] == 0 for resource_type in ['wood3', 'wood2_card', 'resin2', 'resin_card', 'card2_token', 'stone', 'berry_card', 'berry'])) and self.recalls < self.max_recalls:
            available_actions.append(('recall_workers', None))
        action = self.choose_action(available_actions)
        #TODO CHOOSE whether to use Innkeeper or Judge or...: The AI currently prioritizes using innkeepers, then cranes, then judges, but ideally it should be able to choose between these. This also skews the stats towards innkeepers and away from judges.
        if action and action[0] == 'play_card_with_innkeeper':
            self.card_to_play = action[1]
            self.innkeeper_card_to_discard = action[2]
            self.swapped_resources = None
        elif action and action[0] == 'play_card_with_crane':
            self.card_to_play = action[1]
            self.crane_card_to_discard = action[2]
            self.swapped_resources = None
        elif action and action[0] == 'play_card_with_judge':
            #TODO CHOOSE whether to use the Judge or not: "The AI currently only uses the Judge when it has to, but in theory it could choose to use the Judge even when it could otherwise afford the card
            self.card_to_play = action[1]
            self.judge_card_to_use = action[2]
            self.swapped_resources = self.determine_swapped_resources(action[1])
        elif action and action[0] == 'play_card':
            self.card_to_play = action[1]
            self.innkeeper_card_to_discard = None
            self.judge_card_to_use = None
            self.swapped_resources = None
        else:
            self.card_to_play = None
            self.innkeeper_card_to_discard = None
            self.judge_card_to_use = None
            self.swapped_resources = None
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
                reward += 5  # Smaller reward for a tie
            elif agent_index == winner:
                reward += 10  # Large reward for winning
            else:
                reward = 0 # No additional reward or penalty if the AI loses
        elif action == 'receive_resources':
            # Reward for placing a worker on a token location
            if agents[agent_index].resource_pick == 'card2_token':
                reward = 1  # Small reward for choosing a token location
            else:
                reward = 0.1  # Small reward for gathering other resources
        elif action is not None and isinstance(action, tuple) and action[0] == 'basic_event':
            reward = 3  # Small reward for claiming an event
        elif action is not None and isinstance(action, tuple) and action[0] is not None and action[0].startswith('play_card'):
            card = game.agents[agent_index].card_to_play  # Assuming card_to_play is now an instance of Card
            if card:
                # Add reward for tokens received during Monk's activation
                if card.name == "Monk":
                    # Reward for tokens received during Monk's activation
                    berries_given = game.agents[agent_index].berries_given_during_monk_activation
                    reward += berries_given * 0.1
                else:
                    reward = card.points * 1  # Small reward for the card's point value (even when playing a fool into someone else's city)
                # Add a small reward for adding a card of the same color, unless there are already 3 of the same card
                if card.card_type != 'prosperity':
                    same_color_cards = [played_card for played_card in agents[agent_index].played_cards if played_card.card_color == card.card_color]
                    if len(same_color_cards) < 3:
                        reward += 0.5  # Small reward for adding a card of the same color
        return reward
