# Everdell AI - User Interface Description

## Overview

The Everdell AI project includes a graphical user interface (UI) implemented in `ui.py` that allows users to train the AI model, test it, and visualize the results. The UI provides controls for configuring training parameters, displays the game state during training and testing, and offers visualization tools for analyzing AI performance.

## UI Components

The UI is built using Python's Tkinter library and consists of several key components:

### Main Window

The main window is created in the `setup_ui` function and includes:

- Configuration controls for training parameters
- Display areas for the game state (meadow, hands)
- Progress indicators (turn counter, episode counter)
- Action buttons (Train Model, Load and Test Model)

```python
def setup_ui():
    root = tk.Tk()
    root.title("Everdell AI")
    # Turn counter label
    turn_counter_label = tk.Label(root, text="Turn: 0")
    turn_counter_label.pack(anchor='ne', padx=10, pady=10)
    # Episode counter label
    episode_counter_label = tk.Label(root, text="Episode: 0")
    episode_counter_label.pack(anchor='ne', padx=10, pady=5)
    # ... other UI components
```

### Configuration Controls

The UI includes several configuration controls:

#### Number of Agents

Controls the number of AI agents participating in the training:

```python
# Number of agents label and entry
num_agents_frame = tk.Frame(root)
num_agents_frame.pack(anchor='nw', padx=10, pady=10)
num_agents_label = tk.Label(num_agents_frame, text="Number of Agents:")
num_agents_label.pack(side=tk.LEFT)
num_agents_entry = tk.Entry(num_agents_frame, textvariable=tk.StringVar(value="2"))
num_agents_entry.pack(side=tk.LEFT)
```

#### Randomize Agents Checkbox

Allows randomizing the number of agents for each training episode:

```python
# Checkbox to randomize the number of agents
randomize_agents_var = tk.BooleanVar(value=False)
randomize_agents_checkbox = tk.Checkbutton(num_agents_frame, text="Randomize Agents", variable=randomize_agents_var, command=toggle_num_agents_entry)
randomize_agents_checkbox.pack(side=tk.LEFT)
```

#### Live View Checkbox

Enables real-time visualization of training metrics:

```python
# Checkbox to enable live view
live_view_var = tk.BooleanVar(value=False)
live_view_checkbox = tk.Checkbutton(root, text="Enable Live View", variable=live_view_var)
live_view_checkbox.pack(anchor='nw', padx=10, pady=5)
```

#### Number of Episodes

Controls the number of training episodes:

```python
num_episodes_frame = tk.Frame(root)
num_episodes_frame.pack(anchor='nw', padx=10, pady=10)
num_episodes_label = tk.Label(num_episodes_frame, text="Number of Episodes:")
num_episodes_label.pack(side=tk.LEFT)
num_episodes_entry = tk.Entry(num_episodes_frame, textvariable=tk.StringVar(value="30"))
num_episodes_entry.pack(side=tk.LEFT)
```

#### Time to Wait

Controls the delay between turns during training for visualization purposes:

```python
# Time to wait label and entry
time_to_wait_frame = tk.Frame(root)
time_to_wait_frame.pack(anchor='nw', padx=10, pady=10)
time_to_wait_label = tk.Label(time_to_wait_frame, text="Time to Wait (seconds):")
time_to_wait_label.pack(side=tk.LEFT)
time_to_wait_entry = tk.Entry(time_to_wait_frame, textvariable=tk.StringVar(value="0.001"))
time_to_wait_entry.pack(side=tk.LEFT)
```

### Game State Display

The UI includes components for displaying the game state:

#### Meadow Display

Shows the cards currently available in the meadow:

```python
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
```

The meadow display is updated using the `update_meadow_display` function:

```python
def update_meadow_display(meadow_cards):
    card_names_in_deck = list(set(name for name, card_type, rarity, points, wood, resin, stone, berries, quantity, card_color in (card + (0,) * (8 - len(card)) for card in cards)))
    for i, combobox in enumerate(meadow_card_comboboxes):
        combobox['values'] = card_names_in_deck
        if meadow_cards != None:
            if i < len(meadow_cards):
                combobox.set(meadow_cards[i].name)
            else:
                combobox.set("")
```

#### Hand Display

Shows the cards in each player's hand:

```python
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
```

The hand display is updated using the `update_hand_display` function:

```python
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
```

### Progress Indicators

The UI includes progress indicators to show the current state of training:

#### Turn Counter

Shows the current turn number:

```python
def update_turn_counter(turn):
    turn_counter_label.config(text=f"Turn: {turn + 1}")
```

#### Episode Counter

Shows the current episode number:

```python
def update_episode_counter(episode):
    episode_counter_label.config(text=f"Episode: {episode}")
```

### Action Buttons

The UI includes buttons for initiating training and testing:

#### Train Model Button

Starts the training process with the configured parameters:

```python
# Add a button to train the model
train_button = tk.Button(frame, text="Train Model", command=lambda: train_model(root, num_agents_entry, num_episodes_entry, randomize_agents_var))
train_button.pack(side=tk.LEFT, padx=10)
```

The `train_model` function initializes the agents, creates the game, and starts the training process:

```python
def train_model(root, num_agents_entry, num_episodes_entry, randomize_agents_var):
    # Function to train the model
    try:
        # Read the value from the num_episodes_entry and convert it to an integer
        num_episodes = int(num_episodes_entry.get())
    except ValueError:
        # If the value is not a valid integer, default
        num_episodes = 30
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
    game = ai_game.Game(card_dict, agents, randomize_agents_var, turn_update_callback=update_turn_counter, episode_update_callback=update_episode_counter, ui_root=root, time_to_wait_entry=time_to_wait_entry, meadow_update_callback=update_meadow_display, hand_update_callback=update_hand_display, live_view_var=live_view_var)
    game.train(num_episodes)
    messagebox.showinfo("Training", "Model training complete!")
    game.show_chart_selection_window()  # Show the chart selection window after training
```

#### Load and Test Model Button

Loads a trained model and enters testing mode:

```python
# Add a button to load and test the model
test_button = tk.Button(frame, text="Load and Test Model", command=lambda:load_and_test_model(root))
test_button.pack(side=tk.LEFT, padx=10)
```

The `load_and_test_model` function loads the trained model and sets up the testing environment:

```python
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
    # ... testing logic
```

## Results Visualization

After training, the UI displays a chart selection window that allows users to visualize various aspects of the AI's performance:

```python
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
        # ... other chart options
```

The available charts include:

1. **TD Error Over Time**: Shows the temporal difference error over the training process
2. **AI Scores and Moving Averages Over Episodes**: Shows the scores achieved by each AI agent
3. **TD Error Over Second Half of Episodes**: Focuses on the later part of training
4. **Peddler Pay Choices**: Shows which resources the AI chooses to pay with the Peddler card
5. **Peddler Receive Choices**: Shows which resources the AI chooses to receive with the Peddler card
6. **Card Play Frequency (Normalized)**: Shows how often each card is played, normalized by its quantity in the deck
7. **AI Win Rate Over Time**: Shows the win rate of each AI agent over time
8. **Courthouse Resource Choices**: Shows which resources the AI chooses with the Courthouse card
9. **Card Play Frequency for Discounters (Normalized)**: Shows how often discount cards are played
10. **Undertaker Card Pick Frequency (Normalized)**: Shows which cards the AI picks with the Undertaker
11. **Undertaker Discard Frequency (Normalized)**: Shows which cards the AI discards with the Undertaker
12. **Chip Sweep Activation Frequency**: Shows which cards the AI activates with the Chip Sweep
13. **Teacher Card Draw Frequency**: Shows how many cards the AI draws with the Teacher
14. **Teacher Card Giveaway Frequency (Normalized)**: Shows which cards the AI gives away with the Teacher
15. **Teacher Card Kept Frequency (Normalized)**: Shows which cards the AI keeps with the Teacher
16. **Berry Give Choices Frequency**: Shows how many berries the AI gives with the Monk
17. **Event Selection Frequency**: Shows which events the AI claims

## User Interaction During Testing

During testing, the UI allows users to interact with the game by selecting cards for the meadow and hands:

### Meadow Card Selection

Users can select cards to be drawn into the meadow:

```python
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
```

### Hand Card Selection

Users can select cards to be drawn into a player's hand:

```python
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
```

## Planned Improvements

Based on the code review, several improvements are planned for the UI:

1. **Testing Pause Functionality**: Add the ability to pause after each draw to select the correct cards into all positions and wait for a continue button

2. **Better Card Selection for Undertaker**: Currently, the Undertaker card automatically discards the first 3 cards from the meadow. The AI should be improved to make strategic choices about which cards to discard.

3. **Forest Card Visualization**: Improve the UI to better display forest cards and their associated locations

4. **Resource Display**: Add visualization of each player's resources (wood, resin, stone, berries)

5. **Played Cards Display**: Add visualization of each player's played cards

6. **Card Effect Visualization**: Add visual indicators for card effects and interactions

## Limitations

The current UI implementation has several limitations:

1. **Limited Visualization of Game State**: The UI does not show all aspects of the game state, such as resources, tokens, and played cards

2. **Manual Card Selection During Testing**: Users must manually select cards during testing, which can be time-consuming

3. **No Support for Expansions**: The UI is designed for the base game only and does not support expansions

4. **Limited Error Handling**: Some edge cases in user interaction are not fully handled

5. **No Undo Functionality**: Users cannot undo actions during testing

6. **Fixed Card Selection Logic**: For cards like Undertaker, the AI uses fixed strategies rather than making optimal choices

7. **Limited Forest Card Support**: The UI doesn't provide clear visualization of forest cards and their effects

8. **No Pause Functionality During Testing**: There's no way to pause the testing process to examine the game state or make adjustments