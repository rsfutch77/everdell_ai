import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import ai_game
from player import AIPlayer
from cards import Card as GameCard, cards
import random
randomize_agents_var = None  # Global variable for the randomize agents checkbox state

def update_meadow_display(meadow_cards):
    card_names_in_deck = list(set(name for name, card_type, rarity, points, wood, resin, stone, berries, quantity, card_color in (card + (0,) * (8 - len(card)) for card in cards)))
    for i, combobox in enumerate(meadow_card_comboboxes):
        combobox['values'] = card_names_in_deck
        if meadow_cards != None:
            if i < len(meadow_cards):
                combobox.set(meadow_cards[i].name)
            else:
                combobox.set("")

def update_hand_display(hand_cards, player_index):
     card_names_in_deck = list(set(name for name, card_type, rarity, points, wood, resin, stone, berries, quantity, card_color in (card + (0,) * (8 - len(card)) for card in cards)))
     for i, combobox in enumerate(hand_combo_boxes[player_index]):
         combobox['values'] = card_names_in_deck
         if i < len(hand_cards):
             # Check if the hand_cards entry is a card object and set the combobox value accordingly
             if isinstance(hand_cards[i], GameCard):
                 combobox.set(hand_cards[i].name)
             else:
                 combobox.set(hand_cards[i])
         else:
             combobox.set("")

def train_model(root, num_agents_entry, num_episodes_entry, randomize_agents_var):
    # Function to train the model
    try:
        # Read the value from the num_episodes_entry and convert it to an integer
        num_episodes = int(num_episodes_entry.get())
    except ValueError:
        # If the value is not a valid integer, default to 100 episodes
        num_episodes = 100
    # Define the agents based on the number of agents entry or randomize if checked
    if randomize_agents_var.get():
        # Randomize the number of agents for each episode
        number_of_agents = random.randint(1, 4)  # Assuming a range of 1 to 4 agents
    else:
        try:
            # Read the value from the num_agents_entry and convert it to an integer
            number_of_agents = int(num_agents_entry.get())
        except ValueError:
            # If the value is not a valid integer, default to 2 agents
            number_of_agents = 2
    agents = [AIPlayer(alpha=0.1, gamma=0.9, epsilon=0.1) for _ in range(number_of_agents)]
    card_dict = setup_cards()
    game = ai_game.Game(card_dict, agents, randomize_agents_var, turn_update_callback=update_turn_counter, episode_update_callback=update_episode_counter, ui_root=root, time_to_wait_entry=time_to_wait_entry, meadow_update_callback=update_meadow_display, hand_update_callback=update_hand_display)
    game.train(num_episodes)
    messagebox.showinfo("Training", "Model training complete!")

def toggle_num_agents_entry():
    # Function to enable or disable the num_agents_entry based on the checkbox state
    if randomize_agents_var.get():
        num_agents_entry.config(state='disabled')
    else:
        num_agents_entry.config(state='normal')

def setup_cards():
    # Create a list of Card objects using the quantity attribute from the cards definition
    # Handle tuples with different lengths by providing default values
    return [GameCard(name, card_type, rarity, points, wood, resin, stone, berries, quantity, card_color)
            for name, card_type, rarity, points, wood, resin, stone, berries, quantity, card_color in
            (card + (0,) * (8 - len(card)) for card in cards)
            for _ in range(quantity)]

def user_selects_meadow_card(meadow_card_comboboxes, root):
    # Function to handle user selection of meadow cards
    update_meadow_display(None)
    # Wait for the user to make a selection for the specified combobox
    print(f"Waiting for user to select meadow card.")
    selection = meadow_card_comboboxes[7].get() #Since the meadow currently just shifts all the cards up one index, we always get the last index here
    while not selection:
        root.update_idletasks()
        root.update()
        selection = meadow_card_comboboxes[7].get()
    # Create a dictionary mapping card names to Card objects
    card_dict = {name: GameCard(name, card_type, rarity, points, wood, resin, stone, berries, quantity, card_color) for name, card_type, rarity, points, wood, resin, stone, berries, quantity, card_color in cards}
    # Find the card object by name using the dictionary
    selected_card = card_dict.get(selection, None)
    return selected_card

def user_selects_hand_card(hand_combo_boxes, root, player_index, hand_size):
    # Function to handle user selection of meadow cards
    hand_cards = [combobox.get() for combobox in hand_combo_boxes[player_index]]
    update_hand_display(hand_cards, player_index)
    # Wait for the user to make a selection for the specified combobox
    print(f"Waiting for player {player_index} to select hand card.")
    selection = hand_combo_boxes[player_index][hand_size].get() #Since the meadow currently just shifts all the cards up one index, we always get the last index here
    while not selection:
        root.update_idletasks()
        root.update()
        selection = hand_combo_boxes[player_index][hand_size].get()
    card_dict = {name: GameCard(name, card_type, rarity, points, wood, resin, stone, berries, quantity, card_color) for name, card_type, rarity, points, wood, resin, stone, berries, quantity, card_color in cards}
    # Create a dictionary mapping card names to Card objects
    card_dict = setup_cards()
    # Find the card object by name using the dictionary
    selected_card = card_dict.get(selection, None)
    return selected_card

def load_and_test_model(root):
    # Function to load and test the model
    agent = ai_game.ReinforcementLearningAgent()
    agent.load_model('ai_model.pkl')
    # Disable exploration to use the model for inference
    agent.epsilon = 0
    agents = [agent, ai_game.ReinforcementLearningAgent(alpha=0.1, gamma=0.9, epsilon=0.1)]
    card_dict = setup_cards()
    game = ai_game.Game(card_dict, agents, randomize_agents_var, turn_update_callback=update_turn_counter, episode_update_callback=update_episode_counter, ui_root=root, time_to_wait_entry=time_to_wait_entry, meadow_update_callback=update_meadow_display, hand_update_callback=update_hand_display)
    # Override the drawing when testing the model
    def draw_to_meadow_override():
        selected_card = user_selects_meadow_card(meadow_card_comboboxes, root)
        return [selected_card] if selected_card else []
    game.draw_to_meadow = draw_to_meadow_override
    def draw_to_hand_override(player_index, size_of_hand):
        selected_card = user_selects_hand_card(hand_combo_boxes, root, player_index, size_of_hand)
        return [selected_card] if selected_card else []
    game.draw_to_hand = lambda player_index, size_of_hand: draw_to_hand_override(player_index, size_of_hand)
    try:
        # Read the value from the num_episodes_entry and convert it to an integer
        num_episodes = int(num_episodes_entry.get())
    except ValueError:
        # If the value is not a valid integer, default to 100 episodes
        num_episodes = 100
    ai_wins = 0
    for episode in range(num_episodes):
        game.reset_game()
        while not game.is_game_over():
            game.play_turn()
        game.calculate_score()

def update_turn_counter(turn):
    turn_counter_label.config(text=f"Turn: {turn + 1}")
    
def update_episode_counter(episode):
    episode_counter_label.config(text=f"Episode: {episode}")

def setup_ui():
    global turn_counter_label, time_to_wait_entry, num_agents_entry, num_episodes_entry
    global turn_counter_label, time_to_wait_entry, num_agents_entry, num_episodes_entry, randomize_agents_var
    global episode_counter_label
    global meadow_card_comboboxes
    global hand_combo_boxes
    root = tk.Tk()
    root.title("Everdell AI")
    # Turn counter label
    turn_counter_label = tk.Label(root, text="Turn: 0")
    turn_counter_label.pack(anchor='ne', padx=10, pady=10)
    # Episode counter label
    episode_counter_label = tk.Label(root, text="Episode: 0")  # This label will be updated by the update_episode_counter function
    episode_counter_label.pack(anchor='ne', padx=10, pady=5)

    # Meadow cards frame
    meadow_frame = tk.Frame(root)
    meadow_frame.pack(anchor='nw', padx=10, pady=5)
    meadow_label = tk.Label(meadow_frame, text="Meadow Cards:")
    meadow_label.pack(side=tk.TOP)
    meadow_card_entries = []
    meadow_card_comboboxes = []
    for row in range(2):
        row_frame = tk.Frame(meadow_frame)
        row_frame.pack(side=tk.TOP, pady=2)
        for col in range(4):
            combobox = ttk.Combobox(row_frame, state='readonly', width=18)
            combobox.pack(side=tk.LEFT, padx=2)
            meadow_card_comboboxes.append(combobox)

    # Hand boxes sets frame
    hand_combo_boxes_frame = tk.Frame(root)
    hand_combo_boxes_frame.pack(anchor='nw', padx=10, pady=5)
    hand_combo_boxes_label = tk.Label(hand_combo_boxes_frame, text="Hands:")
    hand_combo_boxes_label.pack(side=tk.TOP)
    hand_combo_boxes = []
    for set_index in range(4):
        set_frame = tk.Frame(hand_combo_boxes_frame)
        set_frame.pack(side=tk.TOP, pady=2)
        combo_boxes_hand = []
        for text_box_index in range(8):
            combobox = ttk.Combobox(set_frame, state='readonly', width=12)
            combobox.pack(side=tk.LEFT, padx=2)
            combo_boxes_hand.append(combobox)
        hand_combo_boxes.append(combo_boxes_hand)

    # Number of agents label and entry
    num_agents_frame = tk.Frame(root)
    num_agents_frame.pack(anchor='nw', padx=10, pady=10)
    num_agents_label = tk.Label(num_agents_frame, text="Number of Agents:")
    num_agents_label.pack(side=tk.LEFT)
    num_agents_entry = tk.Entry(num_agents_frame, textvariable=tk.StringVar(value="2"))
    num_agents_entry.pack(side=tk.LEFT)
    # Checkbox to randomize the number of agents
    randomize_agents_var = tk.BooleanVar(value=False)
    randomize_agents_checkbox = tk.Checkbutton(num_agents_frame, text="Randomize Agents", variable=randomize_agents_var, command=toggle_num_agents_entry)
    randomize_agents_checkbox.pack(side=tk.LEFT)

    # Number of episodes label and entry
    num_episodes_frame = tk.Frame(root)
    num_episodes_frame.pack(anchor='nw', padx=10, pady=10)
    num_episodes_label = tk.Label(num_episodes_frame, text="Number of Episodes:")
    num_episodes_label.pack(side=tk.LEFT)
    num_episodes_entry = tk.Entry(num_episodes_frame, textvariable=tk.StringVar(value="100"))
    num_episodes_entry.pack(side=tk.LEFT)

    # Time to wait label and entry
    time_to_wait_frame = tk.Frame(root)
    time_to_wait_frame.pack(anchor='nw', padx=10, pady=10)
    time_to_wait_label = tk.Label(time_to_wait_frame, text="Time to Wait (seconds):")
    time_to_wait_label.pack(side=tk.LEFT)
    time_to_wait_entry = tk.Entry(time_to_wait_frame, textvariable=tk.StringVar(value="0.001"))
    time_to_wait_entry.pack(side=tk.LEFT)

    # Create a frame for the buttons
    frame = tk.Frame(root)
    frame.pack(pady=20)

    # Add a button to train the model
    train_button = tk.Button(frame, text="Train Model", command=lambda: train_model(root, num_agents_entry, num_episodes_entry, randomize_agents_var))
    train_button.pack(side=tk.LEFT, padx=10)

    # Add a button to load and test the model
    test_button = tk.Button(frame, text="Load and Test Model", command=lambda:load_and_test_model(root))
    test_button.pack(side=tk.LEFT, padx=10)

    # Start the main loop
    root.mainloop()

if __name__ == "__main__":
    setup_ui()
