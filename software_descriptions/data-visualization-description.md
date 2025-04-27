# Everdell AI - Data Visualization Description

## Overview

The Everdell AI project includes comprehensive data visualization capabilities to help analyze and understand the AI's performance during training and testing. These visualization tools are implemented primarily in `plotting.py` and the chart selection functionality in `ai_game.py`. The visualizations provide insights into various aspects of the AI's behavior, learning progress, and decision-making patterns.

## Live Plotting

The `plotting.py` file implements real-time visualization of training metrics using matplotlib's interactive mode. This allows users to monitor the AI's performance as it trains, providing immediate feedback on the learning process.

### Implementation

The live plotting functionality is implemented in the `plot_live` function:

```python
def plot_live(data_file, interval=1):
    plt.ion()  # Turn on interactive mode
    fig, axs = plt.subplots(3, 1, figsize=(10, 10))
    axs[0].set_title('TD Error Over Time')
    axs[0].set_xlabel('Episode')
    axs[0].set_ylabel('TD Error')
    axs[0].set_yscale('log')  # Set y-axis to log scale for TD Error
    axs[1].set_title('AI Scores Over Episodes')
    axs[1].set_xlabel('Episode')
    axs[1].set_ylabel('Score')
    axs[2].set_title('AI Win Rate Over Time')
    axs[2].set_xlabel('Episode')
    axs[2].set_ylabel('Win Rate')
    
    while True:
        try:
            with open(data_file, 'r') as f:
                content = f.read().strip()
                if not content:
                    print("Data file is empty. Skipping this iteration.")
                    time.sleep(interval)
                    continue
                try:
                    # Attempt to parse the JSON data
                    data = json.loads(content)
                except json.JSONDecodeError as e:
                    print(f"JSON decode error: {e}")
                    time.sleep(interval)
                    continue
            # ... update plots with new data
            plt.pause(interval)
        except Exception as e:
            print(f"Plotting error: {e}. Skipping this attempt and trying again later.")
            time.sleep(interval)
            continue
        time.sleep(interval)
```

This function runs in a separate process and continuously updates three plots:

1. **TD Error Over Time**: Shows the temporal difference error, which indicates how well the AI is learning
2. **AI Scores Over Episodes**: Shows the scores achieved by each AI agent in each episode
3. **Win Rate Over Time**: Shows the win rate of each AI agent over the course of training

### Data Source

The live plotting function reads data from a JSON file (`plot_data.json`) that is continuously updated during training:

```python
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
```

### Activation

The live plotting is activated when the "Enable Live View" checkbox is selected in the UI:

```python
if self.live_view_var.get():
    plot_process = Process(target=plot_live, args=(data_file,))
    plot_process.start()
```

## Chart Selection Window

After training is complete, the system displays a chart selection window that allows users to visualize various aspects of the AI's performance. This functionality is implemented in the `show_chart_selection_window` method of the `Game` class in `ai_game.py`.

### Available Charts

The chart selection window offers 17 different charts:

```python
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
```

### Chart Types and Implementation

#### Learning Progress Charts

These charts show the AI's learning progress over time:

1. **TD Error Over Time**:
   ```python
   if chart == "TD Error Over Time":
       for agent in self.agents:
           plt.plot(agent.td_errors)
       plt.title('TD Error Over Time')
       plt.xlabel('Learning Step')
       plt.ylabel('TD Error')
   ```

2. **TD Error Over Second Half of Episodes**:
   ```python
   elif chart == "TD Error Over Second Half of Episodes":
       for agent in self.agents:
           half_index = len(agent.td_errors) // 2
           plt.plot(agent.td_errors[half_index:], label=f'AI {self.agents.index(agent)}')
       plt.title('TD Error Over Second Half of Episodes')
       plt.xlabel('Learning Step (Second Half)')
       plt.ylabel('TD Error')
       plt.legend()
   ```

3. **AI Win Rate Over Time**:
   ```python
   elif chart == "AI Win Rate Over Time":
       for agent in self.agents:
           plt.plot(agent.win_rates)
       plt.title('AI Win Rate Over Time')
       plt.xlabel('Episode')
       plt.ylabel('Win Rate')
   ```

#### Performance Charts

These charts show the AI's performance in terms of scores:

1. **AI Scores and Moving Averages Over Episodes**:
   ```python
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
   ```

#### Decision-Making Charts

These charts show the AI's decision-making patterns for specific cards and actions:

1. **Card Play Frequency (Normalized)**:
   ```python
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
   ```

2. **Peddler Pay Choices**:
   ```python
   elif chart == "Peddler Pay Choices":
       resources = list(self.peddler_pay_choices.keys())
       choices = list(self.peddler_pay_choices.values())
       plt.bar(resources, choices)
       plt.title('Peddler Pay Choices')
       plt.xlabel('Resource')
       plt.ylabel('Number of Times Chosen')
   ```

3. **Peddler Receive Choices**:
   ```python
   elif chart == "Peddler Receive Choices":
       resources = list(self.peddler_receive_choices.keys())
       choices = list(self.peddler_receive_choices.values())
       plt.bar(resources, choices)
       plt.title('Peddler Receive Choices')
       plt.xlabel('Resource')
       plt.ylabel('Number of Times Chosen')
   ```

4. **Courthouse Resource Choices**:
   ```python
   elif chart == "Courthouse Resource Choices":
       resources = list(self.courthouse_resource_choices.keys())
       choices = list(self.courthouse_resource_choices.values())
       plt.bar(resources, choices)
       plt.title('Courthouse Resource Choices')
       plt.xlabel('Resource')
       plt.ylabel('Number of Times Chosen')
   ```

5. **Card Play Frequency for Discounters (Normalized)**:
   ```python
   elif chart == "Card Play Frequency for Discounters (Normalized)":
       card_names = ['Judge', 'Innkeeper', 'Crane']
       card_quantities = {card.name: card.quantity for card in self.initial_deck}
       frequencies = [self.card_play_frequency_discounters[card_name] / card_quantities[card_name] for card_name in card_names]
       plt.bar(card_names, frequencies)
       plt.title('Card Play Frequency for Discounters (Normalized)')
       plt.xlabel('Card Name')
       plt.ylabel('Frequency')
   ```

#### Card Interaction Charts

These charts show how the AI interacts with specific cards:

1. **Undertaker Card Pick Frequency (Normalized)**:
   ```python
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
   ```

2. **Undertaker Discard Frequency (Normalized)**:
   ```python
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
   ```

3. **Chip Sweep Activation Frequency**:
   ```python
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
   ```

4. **Teacher Card Draw Frequency**:
   ```python
   elif chart == "Teacher Card Draw Frequency":
       draw_counts = list(self.teacher_card_draw_frequency.keys())
       frequencies = list(self.teacher_card_draw_frequency.values())
       plt.bar(draw_counts, frequencies)
       plt.title('Teacher Card Draw Frequency')
       plt.xlabel('Number of Cards Drawn')
       plt.ylabel('Frequency')
   ```

5. **Teacher Card Giveaway Frequency (Normalized)**:
   ```python
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
   ```

6. **Teacher Card Kept Frequency (Normalized)**:
   ```python
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
   ```

7. **Berry Give Choices Frequency**:
   ```python
   elif chart == "Berry Give Choices Frequency":
       berry_counts = list(self.berry_give_choices.keys())
       frequencies = list(self.berry_give_choices.values())
       plt.bar(berry_counts, frequencies)
       plt.title('Berry Give Choices Frequency')
       plt.xlabel('Number of Berries Given')
       plt.ylabel('Frequency')
   ```

8. **Event Selection Frequency**:
   ```python
   elif chart == "Event Selection Frequency":
       events = list(self.event_selection_frequency.keys())
       frequencies = list(self.event_selection_frequency.values())
       plt.bar(events, frequencies)
       plt.title('Event Selection Frequency')
       plt.xlabel('Event')
       plt.ylabel('Number of Times Selected')
   ```

## Data Collection

The data for visualization is collected during the training process. The `Game` class in `ai_game.py` maintains various counters and dictionaries to track the AI's behavior:

```python
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
    # ... other initialization
```

These counters are updated throughout the game as the AI makes decisions. For example, when the AI plays a card:

```python
def play_card(self, agent, card, agent_index, game, action):
    # ... card playing logic
    
    # Update card play frequency
    self.card_play_frequency[card.name] = self.card_play_frequency.get(card.name, 0) + 1
    
    # Update discounter card play frequency if applicable
    if card.name in self.card_play_frequency_discounters:
        self.card_play_frequency_discounters[card.name] += 1
    
    # ... more card playing logic
```

## Benefits of Visualization

The visualization tools provide several benefits:

1. **Learning Progress Monitoring**: The TD error and win rate charts help monitor the AI's learning progress over time
2. **Strategy Analysis**: The card play frequency and resource choice charts help understand the AI's strategic preferences
3. **Decision-Making Insights**: The card interaction charts provide insights into how the AI makes decisions with specific cards
4. **Performance Evaluation**: The score charts help evaluate the AI's performance over time
5. **AI Behavior Analysis**: The specialized charts for specific cards (Undertaker, Teacher, etc.) provide detailed insights into how the AI interacts with these cards

## Limitations and Future Improvements

The current visualization system has several limitations:

1. **Limited Real-Time Visualization**: The live plotting only shows three metrics (TD error, scores, win rate)
2. **No Interactive Exploration**: The charts are static and do not allow for interactive exploration
3. **No Export Functionality**: There is no way to export the charts or data for further analysis
4. **Limited Comparative Analysis**: There are limited tools for comparing different training runs
5. **No Visualization of Forest Card Effects**: The current system doesn't provide specific visualizations for forest card interactions
6. **Limited Visualization of AI Decision-Making Process**: The system doesn't show the AI's internal decision-making process, only the outcomes
7. **No Visualization of Card Synergies**: The system doesn't provide specific visualizations for card synergies and interactions

Potential future improvements include:

1. **More Interactive Visualizations**: Add interactive elements to the charts, such as zooming, panning, and filtering
2. **Export Functionality**: Add the ability to export charts and data for further analysis
3. **Comparative Analysis Tools**: Add tools for comparing different training runs
4. **More Detailed Visualizations**: Add more detailed visualizations of the AI's decision-making process
5. **Real-Time Strategy Visualization**: Add visualizations that show the AI's strategy evolving in real-time
6. **Forest Card Interaction Visualization**: Add specific visualizations for forest card interactions
7. **Card Synergy Visualization**: Add visualizations that show how different cards interact and create synergies
8. **Decision Tree Visualization**: Add visualizations that show the AI's decision-making process as a tree
9. **Resource Management Visualization**: Add visualizations that show how the AI manages resources over time
10. **Worker Placement Strategy Visualization**: Add visualizations that show the AI's worker placement strategy