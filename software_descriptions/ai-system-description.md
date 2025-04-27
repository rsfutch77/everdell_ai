# Everdell AI - AI System Description

## Overview

The Everdell AI project implements a reinforcement learning system to play the board game Everdell. The AI uses Q-learning, a model-free reinforcement learning algorithm, to learn optimal strategies through self-play. The system consists of a base reinforcement learning agent (implemented in `agent.py`) and a game-specific agent (implemented in `player.py`) that extends the base agent with game-specific actions and decision-making processes.

## Reinforcement Learning Agent

### Core Components

The base reinforcement learning agent (`ReinforcementLearningAgent` class in `agent.py`) implements the following core components:

#### Q-Learning Algorithm

The agent uses Q-learning, which is a value-based reinforcement learning algorithm that learns the value of actions in states by updating a Q-table. The Q-table is implemented as a nested defaultdict, which maps states to actions and their associated Q-values.

```python
self.q_table = defaultdict(default_q_value)
```

The learning process follows the Bellman equation:

```python
new_value = (1 - self.alpha) * old_value + self.alpha * (reward + self.gamma * next_max)
```

Where:
- `alpha` is the learning rate
- `gamma` is the discount factor
- `old_value` is the current Q-value
- `reward` is the immediate reward
- `next_max` is the maximum Q-value for the next state

#### State Representation

The game state is represented as a numerical vector that includes:
- Current turn
- Number of agents
- Each agent's resources (wood, resin, stone, berries)
- Each agent's tokens
- Each agent's workers
- Each agent's recalls
- Each agent's hand size
- Each agent's played cards and their points
- Card IDs and attributes in each agent's hand
- Card IDs and attributes in the meadow
- Forest card IDs and attributes

This state representation is converted to a tuple to be used as a key in the Q-table.

**Note:** The current implementation allows the AI to see all players' hands, which is a known limitation that needs to be addressed in future updates.

#### Action Selection

The agent uses an epsilon-greedy strategy for action selection:
- With probability `epsilon`, the agent explores by choosing a random action
- With probability `1 - epsilon`, the agent exploits by choosing the action with the highest Q-value

```python
def choose_action(self, available_actions):
    if random.uniform(0, 1) < self.epsilon:
        # Explore: choose a random action
        return random.choice(available_actions)
    # Exploit: choose the best action based on past experience
    q_values = {action: self.q_table[tuple(available_actions)][action] for action in available_actions if action in self.q_table[tuple(available_actions)]}
    if q_values:
        max_q_value = max(q_values.values())
        best_actions = [action for action, q in q_values.items() if q == max_q_value]
        return random.choice(best_actions)
    # If no known Q-values, choose randomly
    return random.choice(available_actions)
```

#### Learning Rate and Exploration Strategies

The agent implements dynamic learning rate and exploration rate strategies:

- Learning rate (`alpha`) decreases over time to stabilize learning:
  ```python
  self.alpha = self.alpha * (1 - episode / total_episodes)
  ```

- Exploration rate (`epsilon`) decays exponentially to transition from exploration to exploitation:
  ```python
  self.epsilon = self.initial_epsilon * math.exp(-10 * episode / total_episodes)
  ```

#### Model Saving and Loading

The agent can save and load its learned Q-table and parameters:

```python
def save_model(self, filename):
    with open(filename, 'wb') as file:
        pickle.dump({
            'q_table': self.q_table,
            'alpha': self.alpha,
            'gamma': self.gamma,
            'epsilon': self.epsilon
        }, file)

def load_model(self, filename):
    with open(filename, 'rb') as file:
        data = pickle.load(file)
        self.q_table = data['q_table']
        self.alpha = data['alpha']
        self.gamma = data['gamma']
        self.epsilon = data['epsilon']
```

## Game-Specific Agent

The game-specific agent (`AIPlayer` class in `player.py`) extends the base reinforcement learning agent with game-specific actions and decision-making processes.

### Game-Specific Actions and Decisions

The `AIPlayer` class implements methods for:

#### Resource Management

- Tracking resources (wood, resin, stone, berries)
- Receiving resources from worker placement
- Managing tokens
- Handling resource exchanges (e.g., for the Peddler card)

```python
def receive_resources(self, resource_type, game):
    # Method to increase the agent's resources and return the received resource
    cards_to_draw = 0
    if resource_type == 'wood3':
        self.wood += 3
    elif resource_type == 'wood2_card':
        self.wood += 2
        cards_to_draw = 1
    # ... other resource types
```

#### Card Playing Logic

- Determining if a card can be played based on available resources
- Handling special card effects (e.g., Innkeeper, Judge, Crane)
- Managing card interactions and synergies

```python
def can_play_card(self, card, game):
    # Check if the card can be played based on available resources
    unique_card_already_played = card.rarity == "unique" and card.name != "Fool" and any(played_card.name == card.name for played_card in self.played_cards)
    innkeeper_card = next((played_card for played_card in self.played_cards if played_card.name == "Innkeeper"), None)
    can_use_innkeeper = innkeeper_card and card.card_type == 'character' and self.resources_less_than_cost(card) and self.resources_at_least_reduced_cost(card)
    # ... other conditions
```

#### Worker Placement Strategy

- Determining available worker placement locations
- Allocating workers to locations
- Managing worker recall

```python
def determine_available_actions(self, hand, meadow, game):
    # Determine the available actions for the AI player
    available_actions = []
    # ... card playing actions
    if self.workers > 0:
        if any(card.name == "Lookout" for card in self.played_cards):
            if self.lookout_slots_available > 0:
                available_actions.append(('receive_resources', 'lookout'))
        for resource_type in game.locations:
            if game.worker_slots_available[resource_type] > 0:
                available_actions.append(('receive_resources', resource_type))
    # ... other actions
```

### Reward System

The `get_reward` method calculates rewards based on:
- Game outcome (win, tie, loss)
- Card point values
- Resource acquisition
- Event claiming
- Card color synergies

```python
def get_reward(self, game, action, done, agent_index):
    # Reward function
    agents = game.agents
    reward = 0  

    if done:
        tie_calculator, winner = game.get_winner(game)
        if tie_calculator > 1 and agents[agent_index].score == agents[winner].score:
            reward += 5  # Smaller reward for a tie
        elif agent_index == winner:
            reward += 10  # Large reward for winning
        else:
            reward = 0 # No additional reward or penalty if the AI loses
    # ... other reward calculations
    return reward
```

## Training Process

The training process is managed by the `Game` class in `ai_game.py`. The key components include:

### Episode Structure

Each training episode consists of:
1. Game initialization with shuffled deck and initial cards
2. Players taking turns until the game ends
3. Score calculation and winner determination
4. Learning updates based on rewards

```python
def train(self, num_episodes):
    # ... initialization
    for episode in range(num_episodes):
        # ... episode setup
        self.reset_game()
        done = False
        while not done:
            state = self.get_numerical_game_state()
            actions_taken = self.play_turn()
            next_state = self.get_numerical_game_state()
            done = self.is_game_over()
            for agent_index, agent in enumerate(self.agents):
                action = actions_taken[agent_index]
                reward = agent.get_reward(self, action, done, agent_index)
                agent.learn(state, action, reward, next_state, done)
        # ... episode wrap-up
```

### Performance Tracking

The system tracks various performance metrics:
- TD errors over time
- Scores over episodes
- Win rates
- Card play frequencies
- Resource choice frequencies

```python
# In Game.__init__
self.card_play_frequency = {}
self.courthouse_resource_choices = {'wood': 0, 'resin': 0, 'stone': 0}
self.berry_give_choices = {0: 0, 1: 0, 2: 0}
self.peddler_pay_choices = {'wood': 0, 'resin': 0, 'stone': 0, 'berries': 0}
# ... other tracking variables
```

## Testing Mode

The testing mode allows users to evaluate the trained AI and get move recommendations. Key components include:

### Model Evaluation

- Loading a trained model
- Disabling exploration (setting epsilon to 0)
- Running the AI against other agents or itself

```python
def load_and_test_model(root):
    agent = ai_game.ReinforcementLearningAgent()
    agent.load_model('ai_model.pkl')
    # Disable exploration to use the model for inference
    agent.epsilon = 0
    # ... testing setup
```

### User Interaction

- User selection of meadow cards
- User selection of hand cards
- AI move recommendations based on the current game state

```python
def user_selects_meadow_card(meadow_card_comboboxes, root):
    # Function to handle user selection of meadow cards
    update_meadow_display(None)
    # Wait for the user to make a selection
    # ... selection logic
```

## Limitations and TODOs

The AI system has several limitations and areas for improvement:

### Decision-Making Limitations

1. The AI currently makes heuristic assumptions in complex decision scenarios:
   ```python
   #TODO CHOOSE whether to use Innkeeper or Judge or...: The AI currently prioritizes using innkeepers, then cranes, then judges, but ideally it should be able to choose between these.
   ```

2. The AI uses fixed strategies for cards like Undertaker, Judge, and Crane rather than making optimal choices:
   ```python
   #TODO CHOOSE which resources to reduce for the crane: The crane currently only reduces the cost of resources starting with stone and any other resources if there is any leftover, the AI should be able to choose which of any combination of the resources to reduce.
   ```

3. The AI currently only uses the Judge when it has to, but could potentially use it strategically even when it could otherwise afford a card:
   ```python
   #TODO CHOOSE whether to use the Judge or not: "The AI currently only uses the Judge when it has to, but in theory it could choose to use the Judge even when it could otherwise afford the card
   ```

### State Representation Issues

1. The AI can "cheat" by seeing opponent hands in the state representation:
   ```python
   #TODO AI should only be able to use it's own hand in the game state representation. This allows it to cheat by seeing the opposing hand.
   ```

### Card Interaction Limitations

1. The AI uses a fixed approach for the Undertaker card rather than making strategic choices:
   ```python
   #TODO CHOOSE which cards the undertaker should discard instead of just the first three: AI is playing an Undertaker card. It currently only chooses the first 3 cards from the meadow to discard.
   ```

2. The AI uses a fixed approach for the Fool card rather than making strategic choices:
   ```python
   #TODO CHOOSE a player for the fool instead of just the next player
   ```

3. The AI uses a fixed approach for the Teacher card rather than making strategic choices:
   ```python
   #TODO CHOOSE a player for the teacher instead of just the next player
   ```

4. The AI has issues handling special locations:
   ```python
   #TODO Handle when a ranger chooses a lookout, for now we skip it
   #TODO Handle when a clocktower chooses a lookout, for now we skip it
   ```

5. The AI doesn't prioritize which copy of a card to play when the same card is in both hand and meadow:
   ```python
   #TODO CHOOSE which copy to play when you have the same card in the hand and meadow: play_card currently prioritizes taking cards from the meadow, but the AI should choose either a card from the hand or the meadow when there is a copy of the same card in each.
   ```

### Other Limitations

1. Limited support for expansions (base game only)
2. Forest locations are implemented but with placeholder effects
3. Some edge cases in card interactions are not fully implemented
4. The AI doesn't have a strategic approach to choosing resources for cards like Courthouse and Peddler

These limitations are documented in the code as TODOs and are planned for future improvements.