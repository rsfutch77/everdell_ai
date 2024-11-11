from agent import ReinforcementLearningAgent
import numpy as np
import matplotlib.pyplot as plt
import time
from player import AIPlayer
import random

class Game:

    def __init__(self, deck, agents, randomize_agents, turn_update_callback=None, episode_update_callback=None, ui_root=None, time_to_wait_entry=None, meadow_update_callback=None, hand_update_callback=None):
        self.undertaker_card_pick_frequency = {}  # Track card pick frequency after Undertaker activation
        self.chip_sweep_activation_frequency = {}  # Track card activation frequency after Chip Sweep activation
        self.card_play_frequency_discounters = {'Judge': 0, 'Innkeeper': 0, 'Crane': 0}  # Track specific card play frequency
        self.teacher_card_draw_frequency = {0: 0, 1: 0, 2: 0}  # Track how often 0, 1, or 2 cards are drawn
        self.teacher_card_giveaway_frequency = {}  # Track how often each card is given away
        self.teacher_card_kept_frequency = {}  # Track how often each card is kept
        self.courthouse_resource_choices = {'wood': 0, 'resin': 0, 'stone': 0}  # Track resource choices for Courthouse
        self.discard = []  # List to hold discarded cards
        self.revealed_cards = []  # List to hold revealed cards
        self.card_play_frequency = {}  # Dictionary to track the frequency of card plays
        self.worker_slots_available = {'wood3': 1, 'wood2_card': 4, 'resin2': 1, 'resin_card': 4, 'card2_token': 4, 'stone': 1, 'berry_card': 1, 'berry': 4}
        self.hand_update_callback = hand_update_callback
        self.meadow_update_callback = meadow_update_callback
        self.time_to_wait_entry = time_to_wait_entry
        self.turn_update_callback = turn_update_callback
        self.ui_root = ui_root
        self.initial_deck = list(deck)  # Store the initial state of the deck
        self.agents = agents
        self.ties = 0
        self.randomize_agents = randomize_agents  # Store the randomize_agents variable
        self.episode_update_callback = episode_update_callback  # Store the episode_update_callback

        self.max_meadow_cards = 8  # Define the maximum number of cards in the meadow
        self.reset_game

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
        self.reset_game()
        if len(self.meadow) != self.max_meadow_cards:
            raise Exception(f"The meadow has {len(self.meadow)} cards, expected {self.max_meadow_cards}.")
        
            agent.game = self

    def train(self, num_episodes):
        self.ties = 0
        # Initialize a list to store the average TD errors for all episodes
        all_episodes_td_errors = []
        # Reset the Courthouse resource choices tracking
        self.courthouse_resource_choices = {'wood': 0, 'resin': 0, 'stone': 0}
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
            done = False
            while not done:
                state = self.get_numerical_game_state()  # Capture the state before the turn
                actions_taken = self.play_turn()  # Get the actions taken during the turn
                next_state = self.get_numerical_game_state()  # Capture the state after the turn
                done = self.is_game_over()
                for agent_index, agent in enumerate(self.agents):
                    action = actions_taken[agent_index]  # Use the action taken by the agent
                    reward = agent.get_reward(self, action, done, agent_index)
                    agent.learn(state, action, reward, next_state, done)

            # Collect and average TD errors for the episode
            if self.randomize_agents.get():
                episode_td_errors = [agent.td_errors[-1] for agent in self.agents if agent.td_errors]
                average_td_error = sum(episode_td_errors) / len(episode_td_errors) if episode_td_errors else 0
                all_episodes_td_errors.append(average_td_error)  # Store the average TD error for the episode

            tie_calculator, winner = self.get_winner(self)

            #Apply record of wins and ties
            if tie_calculator > 1:
                self.ties += 1
            else:
                self.agents[winner].wins += 1


            # Update the episode counter in the UI
            if self.episode_update_callback:
                self.episode_update_callback(episode + 1)

            print(f"Episode {episode + 1}:")
            for agent in self.agents:
                win_rate = agent.wins / (episode + 1)
                agent.win_rates.append(win_rate)
                print(f"AI {self.agents.index(agent)} score: {agent.score},")
                if not self.randomize_agents.get():
                    print(f"AI {self.agents.index(agent)} Win Rate: {agent.wins / (episode + 1):.2%}")
            print(f"Ties: {self.ties / (episode + 1):.2%}")

        if not self.randomize_agents.get():
            plt.figure()  # Create a new figure
            for agent in self.agents:
                plt.plot(agent.td_errors)
            plt.title('TD Error Over Time')
            plt.xlabel('Learning Step')
            plt.ylabel('TD Error')
        # Plot the frequency of each card being played
        if self.card_play_frequency:
            plt.figure()
            card_names = list(self.card_play_frequency.keys())
            # Normalize frequencies by the quantity of each card in the deck
            card_quantities = {card.name: card.quantity for card in self.initial_deck}
            frequencies = [self.card_play_frequency[card_name] / card_quantities[card_name] for card_name in card_names]
            plt.bar(card_names, frequencies)
            plt.title('Card Play Frequency (Normalized)')
            plt.xlabel('Card Name')
            plt.ylabel('Frequency')
            plt.xticks(rotation=90)
            plt.tight_layout()  # Adjust layout to prevent label cutoff
        if not self.randomize_agents.get():
            # Plot the win rates over episodes
            plt.figure()  # Create a new figure
            for agent in self.agents:
                plt.plot(agent.win_rates)
            plt.title('AI Win Rate Over Time')
            plt.xlabel('Episode')
            plt.ylabel('Win Rate')
        # Plot the Courthouse resource choices
        plt.figure()
        resources = list(self.courthouse_resource_choices.keys())
        choices = list(self.courthouse_resource_choices.values())
        plt.bar(resources, choices)
        plt.title('Courthouse Resource Choices')
        plt.xlabel('Resource')
        plt.ylabel('Number of Times Chosen')
        # Plot the card play frequency for discounters (which of these cards is used most often to get a discount)
        plt.figure()
        card_names = ['Judge', 'Innkeeper', 'Crane']
        card_quantities = {card.name: card.quantity for card in self.initial_deck}
        plt.bar(card_names, card_quantities)
        plt.title('Card Play Frequency for Discounters')
        plt.xlabel('Card Name')
        plt.ylabel('Frequency')
        # Plot the Undertaker card pick frequency (which cards does the undertaker draw from the meadow)
        if self.undertaker_card_pick_frequency:
            plt.figure()
            card_names = list(self.undertaker_card_pick_frequency.keys())
            # Normalize frequencies by the quantity of each card in the deck
            card_quantities = {card.name: card.quantity for card in self.initial_deck}
            frequencies = [self.undertaker_card_pick_frequency[card_name] / card_quantities[card_name] for card_name in card_names]
            plt.bar(card_names, frequencies)
            plt.title('Undertaker Card Pick Frequency (Normalized)')
            plt.xlabel('Card Name')
            plt.ylabel('Frequency')
            plt.xticks(rotation=90)
            plt.tight_layout()  # Adjust layout to prevent label cutoff
        # Plot the Chip Sweep activation frequency
        if self.chip_sweep_activation_frequency:
            plt.figure()
            card_names = list(self.chip_sweep_activation_frequency.keys())
            # Normalize frequencies by the quantity of each card in the deck
            card_quantities = {card.name: card.quantity for card in self.initial_deck}
            frequencies = [self.chip_sweep_activation_frequency[card_name] / card_quantities[card_name] for card_name in card_names]
            plt.bar(card_names, frequencies)
            plt.title('Chip Sweep Activation Frequency')
            plt.xlabel('Card Name')
            plt.ylabel('Frequency')
            plt.xticks(rotation=90)
            plt.tight_layout()  # Adjust layout to prevent label cutoff
        # Plot the Teacher card draw frequency
        plt.figure()
        draw_counts = list(self.teacher_card_draw_frequency.keys())
        frequencies = list(self.teacher_card_draw_frequency.values())
        plt.bar(draw_counts, frequencies)
        plt.title('Teacher Card Draw Frequency')
        plt.xlabel('Number of Cards Drawn')
        plt.ylabel('Frequency')
        # Plot the Teacher card giveaway frequency
        if self.teacher_card_giveaway_frequency:
            plt.figure()
            card_names = list(self.teacher_card_giveaway_frequency.keys())
            # Normalize frequencies by the quantity of each card in the deck
            card_quantities = {card.name: card.quantity for card in self.initial_deck}
            frequencies = [self.teacher_card_giveaway_frequency[card_name] / card_quantities[card_name] for card_name in card_names]
            plt.bar(card_names, frequencies)
            plt.title('Teacher Card Giveaway Frequency (Normalized)')
            plt.xlabel('Card Name')
            plt.ylabel('Frequency')
            plt.xticks(rotation=90)
            plt.tight_layout()  # Adjust layout to prevent label cutoff
        # Plot the Teacher card kept frequency
        if self.teacher_card_kept_frequency:
            plt.figure()
            card_names = list(self.teacher_card_kept_frequency.keys())
            # Normalize frequencies by the quantity of each card in the deck
            card_quantities = {card.name: card.quantity for card in self.initial_deck}
            frequencies = [self.teacher_card_kept_frequency[card_name] / card_quantities[card_name] for card_name in card_names]
            plt.bar(card_names, frequencies)
            plt.title('Teacher Card Kept Frequency (Normalized)')
            plt.xlabel('Card Name')
            plt.ylabel('Frequency')
            plt.xticks(rotation=90)
            plt.tight_layout()  # Adjust layout to prevent label cutoff
        plt.show()

        # Save the AI model after training
        self.agents[0].save_model('ai_model.pkl')

    def draw_cards(self, number):
        drawn_cards = []
        for _ in range(number):
            if self.deck:
                drawn_cards.append(self.deck.pop(0))
        return drawn_cards

    def draw_to_meadow(self):
    # Replenish the meadow immediately after a card is taken
        new_cards = self.draw_cards(1)
        if new_cards:
            print(f"{new_cards[0].name} was drawn into the meadow")
            return new_cards
        else:
            return []

    def discard_cards(self, cards_to_discard):
        """
        Discard a list of cards to the discard pile.     
        """
        self.discard.extend(cards_to_discard)

    def reveal_cards(self, number):
        """
        Reveal cards from the top of the deck and add them to the revealed hand.
        """
        revealed = self.draw_cards(number)
        self.revealed_cards.extend(card for card in revealed)
        return revealed

    def reset_game(self):
        self.current_turn = 0
        self.deck = list(self.initial_deck)  # Copy the initial deck to reset it
        random.shuffle(self.deck)  # Shuffle the deck before each new game
        self.played_cards = []
        self.meadow = self.draw_cards(self.max_meadow_cards)  # Draw cards into the meadow
        for stating_amount_index, agent in enumerate(self.agents):
            agent.reset_agent()  # Reset all agent attributes
            agent.hand = self.draw_cards(agent.hand_starting_amount + stating_amount_index)  # Deal cards to the agent's hand from the shuffled deck

    def has_no_moves(self, agent):
        # Check if all agents are out of moves
        agent_out_of_moves = (agent.workers == 0 and agent.recalls == agent.max_recalls and not any(agent.can_play_card(card, self) for card in agent.hand + self.meadow))
        if agent_out_of_moves:
            print("Agent is out of moves")
            return True
        return False

    def is_game_over(self):
        # Check if all agents are out of moves
        all_agents_out_of_moves = all(self.has_no_moves(agent) for agent in self.agents)
        if all_agents_out_of_moves:
            print("All players are out of moves. The game is over.")
            return True
        return False

    def get_numerical_game_state(self, current_player_index=None):
        # Convert the game state into a numerical representation for the AI
        state_representation = []
        # Include the current turn as a feature
        state_representation.append(self.current_turn)
        # Include the points of played cards for each agent as features
        for agent in self.agents:
            played_points = [card.points for card in agent.played_cards]
            state_representation.extend(played_points)
            for card in agent.hand:
                state_representation.extend([card.points, card.wood, card.resin, card.stone, card.berries])
        for card in self.meadow:
            state_representation.extend([card.points, card.wood, card.resin, card.stone, card.berries])
        # Normalize or scale the features if necessary
        # ...
        return state_representation

    def play_card(self, agent, card, agent_index, game, action):
        # Check if the action is to play the card with the Innkeeper's effect
        if action == 'play_card_with_crane':
            self.card_play_frequency_discounters['Crane'] += 1  # Increment Crane usage
            resources_to_reduce = 3
            agent.stone -= max(card.stone - 3, 0)
            resources_to_reduce -= max(card.stone - 3, 0)
            if resources_to_reduce > 0:
                agent.resin -= max(card.resin - 3, 0)
            resources_to_reduce -= max(card.resin - 3, 0)
            if resources_to_reduce > 0:
                agent.wood -= max(card.wood - 3, 0)
            resources_to_reduce -= max(card.wood - 3, 0)
            print(f"Using Crane")
        elif action == 'play_card_with_innkeeper':
            # Reduce the berry cost by 3, but not below 0
            self.card_play_frequency_discounters['Innkeeper'] += 1  # Increment Innkeeper usage
            agent.berries -= max(card.berries - 3, 0)
            print(f"Using Innkeeper, the following card is played...")
        elif action == 'play_card_with_pigeon':
            # Eliminate the cost altogether if played with the pigeon's effect
            print(f"Using Pigeon, the following card is played...")
            pass
        elif action == 'play_card_with_judge':
            # Use the swapped resources instead of the card's original resources
            self.card_play_frequency_discounters['Judge'] += 1  # Increment Judge usage
            swapped_resources = agent.determine_swapped_resources(card)
            agent.wood -= swapped_resources['wood']
            agent.resin -= swapped_resources['resin']
            agent.stone -= swapped_resources['stone']
            agent.berries -= swapped_resources['berries']
            print(f"Using Judge, the following card is played...")
        else:
            # Deduct the cost from the AI player's resources
            agent.wood -= card.wood
            agent.resin -= card.resin
            agent.stone -= card.stone
            agent.berries -= card.berries
        agent.played_cards.append(card)
        print(f"AI {agent_index} plays {card.name}.")
        # Check for and trigger any on-trigger effects
        for trigger_card in agent.on_trigger:
            trigger_card.trigger(agent, game, card)
        # Activate the card's effect if it has one
        card.activate(agent, game)
        if card in game.meadow:
            self.meadow.remove(card)
            self.meadow.extend(self.draw_to_meadow())
            self.meadow_update_callback(self.meadow)  # Update the meadow display
            print(f"That card was played from the meadow.")
        elif card in agent.hand:
            agent.hand.remove(card)
            self.hand_update_callback(agent.hand, agent_index)
            print(f"That card was played from the hand.")
        # Update the card play frequency
        self.card_play_frequency[card.name] = self.card_play_frequency.get(card.name, 0) + 1

    def play_turn(self):

        for agent in self.agents:
            if len(agent.hand) > agent.max_cards_in_hand:
                raise Exception(f"AI {self.agents.index(agent)} has exceeded the maximum hand size with {len(agent.hand)} cards.")
            self.meadow_update_callback(self.meadow)  # Update the meadow display

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
        print(f"Meadow: {[card.name for card in self.meadow]}")

        actions_taken = []  # List to store the actions taken by each agent

        for agent in self.agents:
            print(f"Starting turn with AI {self.agents.index(agent)} Wood: {agent.wood} Resin: {agent.resin} Stone: {agent.stone} Berries: {agent.berries}")
            print(f"AI {self.agents.index(agent)} has {agent.workers} workers remaining.")
            print(f"AI {self.agents.index(agent)} hand: {[card.name for card in agent.hand]}")

        # AI attempts to select an action
        for agent_play_turn_index, agent in enumerate(self.agents):
            # Skip the turn if the agent is out of moves
            if self.has_no_moves(agent):
                print(f"AI {self.agents.index(agent)} is out of moves and will pass this turn.")
                actions_taken.append((None, None))  # Append a None action for this agent
                continue  # Skip the rest of the turn for this agent

            selected_action = agent.determine_available_actions(agent.hand, self.meadow, self)
            # Ensure selected_action is a tuple with three elements
            if selected_action is not None and len(selected_action) == 2:
                selected_action = selected_action + (None,)
            elif selected_action is None:
                selected_action = (None, None, None)
            actions_taken.append(selected_action)
            if selected_action is not None:
                if selected_action[0] == 'play_card_with_innkeeper':
                    action, card, innkeeper_card_to_discard = selected_action
                    # Discard the Innkeeper card after using its effect
                    if innkeeper_card_to_discard in agent.played_cards:
                        agent.played_cards.remove(innkeeper_card_to_discard)       
                        self.discard_cards([innkeeper_card_to_discard])
                        print(f"Innkeeper card discarded by AI to pay for the following...{agent_play_turn_index}")
                    self.play_card(agent, card, agent_play_turn_index, self, action)
                elif selected_action[0] == 'play_card_with_crane':
                    action, card, crane_card_to_discard = selected_action
                    # Discard the Crane card after using its effect
                    if crane_card_to_discard in agent.played_cards:
                        agent.played_cards.remove(crane_card_to_discard)       
                        self.discard_cards([crane_card_to_discard])
                        print(f"Crane card discarded by AI to pay for the following...{agent_play_turn_index}")
                    self.play_card(agent, card, agent_play_turn_index, self, action)
                elif selected_action[0] == 'play_card_with_judge':
                    action, card, judge = selected_action
                    self.play_card(agent, card, agent_play_turn_index, self, action)
                elif selected_action[0] == 'play_card':
                    action, card, _ = selected_action
                    self.play_card(agent, card, agent_play_turn_index, self, action)
                elif selected_action[0] == 'receive_resources' and agent.workers > 0:
                    received_resources, cards_to_draw = agent.receive_resources(agent.resource_pick, self)
                    new_cards = self.draw_cards(cards_to_draw)
                    if cards_to_draw > 0:
                        agent.draw_to_hand(new_cards, self)
                    print(f"AI {self.agents.index(agent)} receives {received_resources} resources.")
                elif selected_action[0] == 'recall_workers':
                    self.recall_workers(agent, agent_play_turn_index)

        print(f"Deck size after turn: {len(self.deck)}")
        self.current_turn += 1

        return actions_taken  # Return the list of actions taken

    def get_game_state(self):
        # Placeholder for more complex game state
        return {'turn': self.current_turn, 'played_cards': self.played_cards}

    def calculate_score(self):
        scores = []
        for agent in self.agents:
            base_score = sum(card.points for card in agent.played_cards + agent.non_city_cards)
            prosperity_score = 0
            for card in agent.prosperity_cards:
                prosperity_score = card.activate(agent, self)  # Activate endgame scoring for prosperity cards
            total_score = base_score + agent.tokens + prosperity_score
            scores.append(total_score)
        return scores

    def recall_workers(self, agent, player_index):
        """
        Handle the recall workers action for the agent.
        """
        if agent.workers == 0 and agent.recalls < agent.max_recalls:
            if agent.recalls == 0:
                agent.workers += 3  # Get another worker
                print(f"Spring.")
            elif agent.recalls == 1:
                agent.workers += 4  # Get another worker
                print(f"Summer.")
                # Allow the player to draw up to the quantity of cards, without exceeding 8 cards in hand
                agent.draw_to_hand(self.draw_cards(min(2, agent.max_cards_in_hand - len(agent.hand))), self)
            else:
                agent.workers += 6  # Get another 2 workers
                print(f"Bonus worker for Fall.")
            # Reset worker allocation for the agent
            for resource_type in agent.worker_allocation:
                self.worker_slots_available[resource_type] += agent.worker_allocation[resource_type]
                agent.worker_allocation[resource_type] = 0
            agent.recalls += 1  # Increment the recall count
            agent.max_workers = agent.workers  # Set max_workers to the current number of workers
            print(f"AI {self.agents.index(agent)} is preparing for season: recalling workers and getting an additional worker.")
        else:
            raise Exception(f"AI {self.agents.index(agent)} cannot recall workers at this time.")
