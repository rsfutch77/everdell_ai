import random
from agent import ReinforcementLearningAgent
import numpy as np
import matplotlib.pyplot as plt
import time
from player import AIPlayer
from cards import forest_deck
import tkinter as tk
from tkinter import messagebox
from tkinter import Toplevel, Button, StringVar, OptionMenu
from multiprocessing import Process
import json
import os
from plotting import plot_live

class Game:

    def __init__(self, deck, agents, randomize_agents, turn_update_callback=None, episode_update_callback=None, ui_root=None, time_to_wait_entry=None, meadow_update_callback=None, hand_update_callback=None, live_view_var=None):
        self.live_view_var = live_view_var
        self.is_training_mode = False  # Initialize training mode flag
        self.undertaker_card_pick_frequency = {}  # Track card pick frequency after Undertaker activation
        self.chip_sweep_activation_frequency = {}  # Track card activation frequency after Chip Sweep activation
        self.card_play_frequency_discounters = {'Judge': 0, 'Innkeeper': 0, 'Crane': 0, 'Monk': 0}  # Track specific card play frequency
        self.teacher_card_draw_frequency = {0: 0, 1: 0, 2: 0}  # Track how often 0, 1, or 2 cards are drawn
        self.teacher_card_giveaway_frequency = {}  # Track how often each card is given away
        self.teacher_card_kept_frequency = {}  # Track how often each card is kept
        self.undertaker_discard_frequency = {}  # Track frequency of cards discarded by the Undertaker
        self.courthouse_resource_choices = {'wood': 0, 'resin': 0, 'stone': 0}  # Track resource choices for Courthouse
        self.berry_give_choices = {0: 0, 1: 0, 2: 0}  # Track how often the AI chooses to give 0, 1, or 2 berries
        self.peddler_pay_choices = {'wood': 0, 'resin': 0, 'stone': 0, 'berries': 0}  # Track resource choices for Peddler payment
        self.peddler_receive_choices = {'wood': 0, 'resin': 0, 'stone': 0, 'berries': 0}  # Track resource choices for Peddler receipt
        self.discard = []  # List to hold discarded cards
        self.revealed_cards = []  # List to hold revealed cards
        self.card_play_frequency = {}  # Dictionary to track the frequency of card plays
        self.claimed_events = set()  # Track claimed events
        self.event_selection_frequency = {'monument': 0, 'tour': 0, 'festival': 0, 'expedition': 0}  # Track event selection frequency
        self.forest_deck = list(forest_deck)  # Initialize the forest deck
        random.shuffle(self.forest_deck)  # Shuffle the forest deck before each new game
        self.worker_slots_available = {'wood3': 1, 'wood2_card': 4, 'resin2': 1, 'resin_card': 4, 'card2_token': 4, 'stone': 1, 'berry_card': 1, 'berry': 4, 'lookout': 0}
        self.hand_update_callback = hand_update_callback
        self.meadow_update_callback = meadow_update_callback
        self.time_to_wait_entry = time_to_wait_entry
        self.turn_update_callback = turn_update_callback
        self.ui_root = ui_root
        self.initial_deck = list(deck)  # Store the initial state of the deck
        self.agents = agents
        self.forest_deck = list(forest_deck)  # Initialize the forest deck
        self.ties = 0
        self.is_training_mode = True  # Set training mode to True when training starts
        self.randomize_agents = randomize_agents  # Store the randomize_agents variable
        self.episode_update_callback = episode_update_callback  # Store the episode_update_callback

        self.max_meadow_cards = 8  # Define the maximum number of cards in the meadow
        self.scores_over_episodes = [[] for _ in self.agents]  # Initialize scores over episodes
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
            root = tk.Tk()
            root.withdraw()  # Hide the root window
            messagebox.showerror("Meadow Size Error", f"The meadow has {len(self.meadow)} cards, expected {self.max_meadow_cards}.")
            root.destroy()
            raise Exception(f"The meadow has {len(self.meadow)} cards, expected {self.max_meadow_cards}.")
        
            agent.game = self

    def train(self, num_episodes):
        self.ties = 0
        # Initialize a list to store the average TD errors for all episodes
        all_episodes_td_errors = []
        # Reset the Courthouse resource choices tracking
        self.courthouse_resource_choices = {'wood': 0, 'resin': 0, 'stone': 0}
        # Initialize a list to store scores for each agent over episodes
        self.scores_over_episodes = [[] for _ in self.agents]

        data_file = 'plot_data.json'
        plot_process = None
        if self.live_view_var.get():
            plot_process = Process(target=plot_live, args=(data_file,))
            plot_process.start()

        for episode in range(num_episodes):
            data = {
                'td_errors': [agent.td_errors for agent in self.agents],
                'scores': self.scores_over_episodes,
                'win_rates': [agent.win_rates for agent in self.agents],
                'window_size': 10
            }
            with open(data_file, 'w') as f:
                try:
                    json.dump(data, f)
                except (TypeError, OverflowError) as e:
                    print(f"Error writing JSON data: {e}")
                    continue
            # Randomize the number of agents for each episode if enabled
            if self.randomize_agents.get():
                number_of_agents = random.randint(2, 4)  # Randomly choose between 2, 3, or 4 agents
                self.agents = [AIPlayer(alpha=0.1, gamma=0.9, epsilon=0.1) for _ in range(number_of_agents)]
            for agent in self.agents:
                agent.update_epsilon(episode, num_episodes)
                agent.update_learning_rate(episode, num_episodes)
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

            # Collect scores for each agent
            for agent_index, agent in enumerate(self.agents):
                self.scores_over_episodes[agent_index].append(agent.score)
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


    def show_chart_selection_window(self):
        # Create a new window for chart selection
        window = Toplevel()
        window.title("Select Chart to Display")

        # Define available charts
        chart_options = [
            "TD Error Over Time",
            "AI Scores and Moving Averages Over Episodes",
            "TD Error Over Second Half of Episodes",
            "Peddler Pay Choices",
            "Peddler Receive Choices",
            "Card Play Frequency (Normalized)",
            "AI Win Rate Over Time",
            "Courthouse Resource Choices",
            "Card Play Frequency for Discounters (Normalized)",
            "Undertaker Card Pick Frequency (Normalized)",
            "Undertaker Discard Frequency (Normalized)",
            "Chip Sweep Activation Frequency",
            "Teacher Card Draw Frequency",
            "Teacher Card Giveaway Frequency (Normalized)",
            "Teacher Card Kept Frequency (Normalized)",
            "Berry Give Choices Frequency",
            "Event Selection Frequency"
        ]

        # Create a StringVar to hold the selected chart
        selected_chart = StringVar(window)
        selected_chart.set(chart_options[0])  # Set default value

        # Create an OptionMenu for chart selection
        chart_menu = OptionMenu(window, selected_chart, *chart_options)
        chart_menu.pack(pady=10)

        # Create a button to display the selected chart
        def display_chart():
            chart = selected_chart.get()
            plt.figure()
            if chart == "TD Error Over Time":
                for agent in self.agents:
                    plt.plot(agent.td_errors)
                plt.title('TD Error Over Time')
                plt.xlabel('Learning Step')
                plt.ylabel('TD Error')
            elif chart == "TD Error Over Second Half of Episodes":
                for agent in self.agents:
                    half_index = len(agent.td_errors) // 2
                    plt.plot(agent.td_errors[half_index:], label=f'AI {self.agents.index(agent)}')
                plt.title('TD Error Over Second Half of Episodes')
                plt.xlabel('Learning Step (Second Half)')
                plt.ylabel('TD Error')
                plt.legend()
            elif chart == "AI Scores and Moving Averages Over Episodes":
                for agent_index, scores in enumerate(self.scores_over_episodes):
                    plt.plot(scores, label=f'AI {agent_index}')
                window_size = max(1, len(self.scores_over_episodes[0]) // 5)
                for agent_index, scores in enumerate(self.scores_over_episodes):
                    if scores:  # Check if scores list is not empty
                        moving_avg = np.convolve(scores, np.ones(window_size)/window_size, mode='valid')
                        plt.plot(range(window_size - 1, len(scores)), moving_avg, linestyle='--', label=f'AI {agent_index} Moving Avg')
                plt.title('AI Scores and Moving Averages Over Episodes')
                plt.xlabel('Episode')
                plt.ylabel('Score')
                plt.legend()
            elif chart == "Peddler Pay Choices":
                resources = list(self.peddler_pay_choices.keys())
                choices = list(self.peddler_pay_choices.values())
                plt.bar(resources, choices)
                plt.title('Peddler Pay Choices')
                plt.xlabel('Resource')
                plt.ylabel('Number of Times Chosen')
            elif chart == "Peddler Receive Choices":
                resources = list(self.peddler_receive_choices.keys())
                choices = list(self.peddler_receive_choices.values())
                plt.bar(resources, choices)
                plt.title('Peddler Receive Choices')
                plt.xlabel('Resource')
                plt.ylabel('Number of Times Chosen')
            elif chart == "Card Play Frequency (Normalized)":
                if self.card_play_frequency:
                    card_names = list(self.card_play_frequency.keys())
                    card_quantities = {card.name: card.quantity for card in self.initial_deck}
                    frequencies = [self.card_play_frequency[card_name] / card_quantities[card_name] for card_name in card_names]
                    plt.bar(card_names, frequencies)
                    plt.title('Card Play Frequency (Normalized)')
                    plt.xlabel('Card Name')
                    plt.ylabel('Frequency')
                    plt.xticks(rotation=90)
                    plt.tight_layout()
            elif chart == "AI Win Rate Over Time":
                for agent in self.agents:
                    plt.plot(agent.win_rates)
                plt.title('AI Win Rate Over Time')
                plt.xlabel('Episode')
                plt.ylabel('Win Rate')
            elif chart == "Courthouse Resource Choices":
                resources = list(self.courthouse_resource_choices.keys())
                choices = list(self.courthouse_resource_choices.values())
                plt.bar(resources, choices)
                plt.title('Courthouse Resource Choices')
                plt.xlabel('Resource')
                plt.ylabel('Number of Times Chosen')
            elif chart == "Card Play Frequency for Discounters (Normalized)":
                card_names = ['Judge', 'Innkeeper', 'Crane']
                card_quantities = {card.name: card.quantity for card in self.initial_deck}
                frequencies = [self.card_play_frequency_discounters[card_name] / card_quantities[card_name] for card_name in card_names]
                plt.bar(card_names, frequencies)
                plt.title('Card Play Frequency for Discounters (Normalized)')
                plt.xlabel('Card Name')
                plt.ylabel('Frequency')
            elif chart == "Undertaker Card Pick Frequency (Normalized)":
                if self.undertaker_card_pick_frequency:
                    card_names = list(self.undertaker_card_pick_frequency.keys())
                    card_quantities = {card.name: card.quantity for card in self.initial_deck}
                    frequencies = [self.undertaker_card_pick_frequency[card_name] / card_quantities[card_name] for card_name in card_names]
                    plt.bar(card_names, frequencies)
                    plt.title('Undertaker Card Pick Frequency (Normalized)')
                    plt.xlabel('Card Name')
                    plt.ylabel('Frequency')
                    plt.xticks(rotation=90)
                    plt.tight_layout()
            elif chart == "Undertaker Discard Frequency (Normalized)":
                if self.undertaker_discard_frequency:
                    card_names = list(self.undertaker_discard_frequency.keys())
                    card_quantities = {card.name: card.quantity for card in self.initial_deck}
                    frequencies = [self.undertaker_discard_frequency[card_name] / card_quantities[card_name] for card_name in card_names]
                    plt.bar(card_names, frequencies)
                    plt.title('Undertaker Discard Frequency (Normalized)')
                    plt.xlabel('Card Name')
                    plt.ylabel('Frequency')
                    plt.xticks(rotation=90)
                    plt.tight_layout()
            elif chart == "Chip Sweep Activation Frequency":
                if self.chip_sweep_activation_frequency:
                    card_names = list(self.chip_sweep_activation_frequency.keys())
                    card_quantities = {card.name: card.quantity for card in self.initial_deck}
                    frequencies = [self.chip_sweep_activation_frequency[card_name] / card_quantities[card_name] for card_name in card_names]
                    plt.bar(card_names, frequencies)
                    plt.title('Chip Sweep Activation Frequency')
                    plt.xlabel('Card Name')
                    plt.ylabel('Frequency')
                    plt.xticks(rotation=90)
                    plt.tight_layout()
            elif chart == "Teacher Card Draw Frequency":
                draw_counts = list(self.teacher_card_draw_frequency.keys())
                frequencies = list(self.teacher_card_draw_frequency.values())
                plt.bar(draw_counts, frequencies)
                plt.title('Teacher Card Draw Frequency')
                plt.xlabel('Number of Cards Drawn')
                plt.ylabel('Frequency')
            elif chart == "Teacher Card Giveaway Frequency (Normalized)":
                if self.teacher_card_giveaway_frequency:
                    card_names = list(self.teacher_card_giveaway_frequency.keys())
                    card_quantities = {card.name: card.quantity for card in self.initial_deck}
                    frequencies = [self.teacher_card_giveaway_frequency[card_name] / card_quantities[card_name] for card_name in card_names]
                    plt.bar(card_names, frequencies)
                    plt.title('Teacher Card Giveaway Frequency (Normalized)')
                    plt.xlabel('Card Name')
                    plt.ylabel('Frequency')
                    plt.xticks(rotation=90)
                    plt.tight_layout()
            elif chart == "Teacher Card Kept Frequency (Normalized)":
                if self.teacher_card_kept_frequency:
                    card_names = list(self.teacher_card_kept_frequency.keys())
                    card_quantities = {card.name: card.quantity for card in self.initial_deck}
                    frequencies = [self.teacher_card_kept_frequency[card_name] / card_quantities[card_name] for card_name in card_names]
                    plt.bar(card_names, frequencies)
                    plt.title('Teacher Card Kept Frequency (Normalized)')
                    plt.xlabel('Card Name')
                    plt.ylabel('Frequency')
                    plt.xticks(rotation=90)
                    plt.tight_layout()
            elif chart == "Berry Give Choices Frequency":
                berry_counts = list(self.berry_give_choices.keys())
                frequencies = list(self.berry_give_choices.values())
                plt.bar(berry_counts, frequencies)
                plt.title('Berry Give Choices Frequency')
                plt.xlabel('Number of Berries Given')
                plt.ylabel('Frequency')
            elif chart == "Event Selection Frequency":
                events = list(self.event_selection_frequency.keys())
                frequencies = list(self.event_selection_frequency.values())
                plt.bar(events, frequencies)
                plt.title('Event Selection Frequency')
                plt.xlabel('Event')
                plt.ylabel('Number of Times Selected')

        display_button = Button(window, text="Display Chart", command=lambda: [display_chart(), plt.show()])
        display_button.pack(pady=10)

        # Save the AI model after training
        self.agents[0].save_model('ai_model.pkl')

    def draw_cards(self, number):
        drawn_cards = []
        for _ in range(number):
            if self.deck:
                drawn_cards.append(self.deck.pop(0))
        return drawn_cards

    def draw_from_forest(self, number):
        """Draw cards from the forest deck."""
        drawn_cards = []
        for _ in range(number):
            if self.forest_deck:
                drawn_cards.append(self.forest_deck.pop(0))
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
        self.forest_deck = list(forest_deck)  # Reset the forest deck
        random.shuffle(self.deck)  # Shuffle the deck before each new game
        self.worker_slots_available = {'wood3': 1, 'wood2_card': 4, 'resin2': 1, 'resin_card': 4, 'card2_token': 4, 'stone': 1, 'berry_card': 1, 'berry': 4, 'lookout': 0}
        self.played_cards = []
        self.meadow = self.draw_cards(self.max_meadow_cards)  # Draw cards into the meadow
        for stating_amount_index, agent in enumerate(self.agents):
            agent.reset_agent()  # Reset all agent attributes
            agent.hand = self.draw_cards(agent.hand_starting_amount + stating_amount_index)  # Deal cards to the agent's hand from the shuffled deck

    def has_no_moves(self, agent):
        # Check if all agents are out of moves
        agent_out_of_moves = ((agent.workers == 0 or all(self.worker_slots_available[resource_type] == 0 for resource_type in ['wood3', 'wood2_card', 'resin2', 'resin_card', 'card2_token', 'stone', 'berry_card', 'berry'])) and agent.recalls == agent.max_recalls and not any(agent.can_play_card(card, self) for card in agent.hand + self.meadow))
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
        #TODO CHOOSE which copy to play when you have the same card in the hand and meadow: play_card currently prioritizes taking cards from the meadow, but the AI should choose either a card from the hand or the meadow when there is a copy of the same card in each.
        # Check if the action is to play the card with the Innkeeper's effect
        if action == 'play_card_with_crane':
            self.card_play_frequency_discounters['Crane'] += 1  # Increment Crane usage
            resources_to_reduce = 3
            #TODO CHOOSE which resources to reduce for the crane: The crane currently only reduces the cost of resources starting with stone and any other resources if there is any leftover, the AI should be able to choose which of any combination of the resources to reduce.
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
            #TODO CHOOSE which resources to swap for the Judge: The AI currently has a fixed setting to choose the next resource on the list to replace another resource with when using the Judge. Ideally the AI would should be able to choose which resource to swap if there is more than one option.
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
                root = tk.Tk()
                root.withdraw()  # Hide the root window
                messagebox.showerror("Hand Size Error", f"AI {self.agents.index(agent)} has exceeded the maximum hand size with {len(agent.hand)} cards.")
                root.destroy()
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
                elif selected_action[0] == 'basic_event':
                    action, event, _ = selected_action
                    print(f"AI {self.agents.index(agent)} chooses basic event: {event}.")
                    agent.event_tickets += 1  # Increment event tickets for any basic event
                    self.claimed_events.add(event)  # Mark the event as claimed
                    self.event_selection_frequency[event] += 1  # Increment the event selection frequency

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
            event_score = len(self.claimed_events) * 3  # Each event is worth 3 points
            total_score = base_score + agent.tokens + prosperity_score + event_score
            scores.append(total_score)
        return scores

    def harvest(self, agent):
        """
        Activate all green cards in the player's city.
        """
        green_cards = [card for card in agent.played_cards if card.card_color == "green"]
        print(f"Harvest. Green cards in city: {[card.name for card in green_cards]}")
        for card in green_cards:
            card.activate(agent, self)

    def recall_workers(self, agent, player_index):
        """
        Handle the recall workers action for the agent.
        """
        # Trigger effects for cards like Clock Tower
        for card in agent.played_cards:
            if card.name == "Clock Tower" and card.get_trigger_effect():
                card.trigger(agent, self, None)
        if (agent.workers == 0 or all(self.worker_slots_available[resource_type] == 0 for resource_type in ['wood3', 'wood2_card', 'resin2', 'resin_card', 'card2_token', 'stone', 'berry_card', 'berry'])) and agent.recalls < agent.max_recalls:
            if agent.recalls == 0:
                agent.workers = 3  # Get another worker
                # On the first recall, perform the harvest
                self.harvest(agent)
            elif agent.recalls == 1:
                agent.workers = 4  # Get another worker
                print(f"Summer.")
                # Allow the player to draw up to the quantity of cards, without exceeding 8 cards in hand
                agent.draw_to_hand(self.draw_cards(min(2, agent.max_cards_in_hand - len(agent.hand))), self)
            else:
                agent.workers = 6  # Get another 2 workers
                print(f"Bonus worker for Fall.")
                # On the last recall, perform the harvest
                self.harvest(agent)
            # Reset worker allocation for the agent
            for resource_type in agent.worker_allocation:
                self.worker_slots_available[resource_type] += agent.worker_allocation[resource_type]
                agent.worker_allocation[resource_type] = 0
            agent.recalls += 1  # Increment the recall count
            agent.max_workers = agent.workers  # Set max_workers to the current number of workers
            print(f"AI {self.agents.index(agent)} is preparing for season: recalling workers and getting an additional worker.")
        else:
            root = tk.Tk()
            root.withdraw()  # Hide the root window
            messagebox.showerror("Recall Workers Error", f"AI {self.agents.index(agent)} cannot recall workers at this time.")
            root.destroy()
            raise Exception(f"AI {self.agents.index(agent)} cannot recall workers at this time.")
