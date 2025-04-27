# Everdell AI - Game Mechanics Description

## Overview

The Everdell AI project implements the core mechanics of the board game Everdell, focusing on the elements necessary for AI training and gameplay. This document describes the game mechanics implemented in the codebase, primarily in `ai_game.py` and `cards.py`.

## Game Engine

The game engine is implemented in the `Game` class in `ai_game.py`. It manages the game state, enforces rules, and facilitates the training process.

### Game State Management

The game state includes:

- **Resources**: Wood, resin, stone, and berries for each player
- **Workers**: Worker allocation and availability
- **Cards**: Deck, meadow, hands, played cards, and discard pile
- **Tokens**: Token count for each player
- **Seasons**: Current season and season progression
- **Locations**: Available worker placement locations and their status
- **Forest**: Forest cards and their associated locations

The game state is represented numerically for the AI using the `get_numerical_game_state` method:

```python
def get_numerical_game_state(self, current_player_index=None):
    state_representation = []
    # Include the current turn as a feature
    state_representation.append(self.current_turn)
    # Include the total number of agents as a feature
    state_representation.append(len(self.agents))
    for agent in self.agents:
        # Include each agent's resources
        state_representation.extend([agent.wood, agent.resin, agent.stone, agent.berries])
        # Include each agent's tokens
        state_representation.append(agent.tokens)
        # Include each agent's workers
        state_representation.append(agent.workers)
        # ... other state features
    return state_representation
```

### Turn Structure

The game follows a turn-based structure where players can:

1. Play a card from their hand or the meadow
2. Place a worker on a location to gather resources
3. Recall workers (once per season)
4. Claim events (when conditions are met)

The turn structure is implemented in the `play_turn` method:

```python
def play_turn(self):
    actions_taken = [None] * len(self.agents)
    for agent_index, agent in enumerate(self.agents):
        # Determine available actions
        action = agent.determine_available_actions(agent.hand, self.meadow, self)
        # Execute the chosen action
        if action and action[0] == 'play_card':
            self.play_card(agent, agent.card_to_play, agent_index, self, action[0])
            actions_taken[agent_index] = 'play_card'
        elif action and action[0].startswith('play_card_with'):
            self.play_card(agent, agent.card_to_play, agent_index, self, action[0])
            actions_taken[agent_index] = action[0]
        elif action and action[0] == 'receive_resources':
            resource_type, cards_to_draw = agent.receive_resources(action[1], self)
            actions_taken[agent_index] = 'receive_resources'
            # ... handle drawing cards
        elif action and action[0] == 'recall_workers':
            self.recall_workers(agent, agent_index)
            actions_taken[agent_index] = 'recall_workers'
        elif action and action[0] == 'basic_event':
            # ... handle claiming events
            actions_taken[agent_index] = 'basic_event'
    return actions_taken
```

### Game End Conditions

The game ends when all players are out of moves, which occurs when:

1. Players have no workers left to place
2. No worker placement locations are available
3. Players have used all their recalls
4. Players cannot play any cards from their hand or the meadow

```python
def is_game_over(self):
    # Check if all agents are out of moves
    all_agents_out_of_moves = all(self.has_no_moves(agent) for agent in self.agents)
    if all_agents_out_of_moves:
        print("All players are out of moves. The game is over.")
        return True
    return False

def has_no_moves(self, agent):
    agent_out_of_moves = ((agent.workers == 0 or self.are_worker_slots_empty(agent)) and 
                          agent.recalls == agent.max_recalls and 
                          not any(agent.can_play_card(card, self) for card in agent.hand + self.meadow))
    if agent_out_of_moves:
        print("Agent is out of moves")
        return True
    return False
```

## Card System

The card system is implemented in `cards.py` and defines the various cards in the game, their properties, and their effects.

### Card Types and Properties

Each card has the following properties:

- **Name**: Unique identifier for the card
- **Card Type**: Character, construction, prosperity, etc.
- **Rarity**: Unique or common
- **Points**: Victory points the card is worth
- **Resource Costs**: Wood, resin, stone, and berries required to play the card
- **Quantity**: Number of copies in the deck
- **Card Color**: Color category for scoring and effects
- **Activation Effect**: Effect triggered when the card is played
- **Trigger Effect**: Effect triggered by other game events

```python
class Card:
    def __init__(self, name, card_type, rarity, points, wood=0, resin=0, stone=0, berries=0, quantity=1, card_color="green"):
        self.name = name
        self.card_type = card_type
        self.rarity = rarity
        self.points = points
        self.wood = wood
        self.resin = resin
        self.stone = stone
        self.berries = berries
        self.quantity = quantity
        self.card_color = card_color
        self.activation_effect = None if card_type == "forest" else self.get_activation_effect()
        self.trigger_effect = self.get_trigger_effect()
```

### Card Effects

The card system implements various card effects:

#### Activation Effects

Activation effects are triggered when a card is played. Examples include:

- **Farm**: Gain 1 berry
- **Mine**: Gain 1 stone
- **Undertaker**: Discard cards from the meadow and pick a new card
- **Fool**: Move the card to another player's city
- **Wanderer**: Draw cards and remove the Wanderer from the city

```python
def activate(self, player, game):
    if self.activation_effect and self.card_type != "forest":
        self.activation_effect(player, game, self)
    if self.card_type == 'prosperity':
        player.prosperity_cards.append(self)  # Add prosperity card to player's list for endgame scoring
```

#### Trigger Effects

Trigger effects are activated by other game events. Examples include:

- **Historian**: Draw a card when another card is played
- **Shopkeeper**: Gain 1 berry when a character card is played
- **Courthouse**: Gain a resource when a construction card is played
- **Clock Tower**: Retrieve a worker during recall

```python
def trigger(self, player, game, card_played):
    if self.trigger_effect:
        self.trigger_effect(player, game, card_played)
```

### Card Interactions

The card system implements various card interactions:

- **Innkeeper**: Allows playing character cards at reduced cost
- **Judge**: Allows swapping resources to play cards
- **Crane**: Allows playing construction cards at reduced cost
- **Gatherer/Harvester**: Provide bonuses when paired together
- **Prosperity Cards**: Provide end-game scoring based on specific conditions

However, there are limitations in how these interactions are implemented:

- The AI currently prioritizes using Innkeepers over Judges or Cranes without strategic consideration
- The Crane currently only reduces the cost of resources starting with stone and any other resources if there is any leftover
- The Judge is only used when the AI cannot otherwise afford a card
- The Undertaker currently only chooses the first 3 cards from the meadow to discard

## Resource System

The resource system manages the four types of resources in the game:

1. **Wood**: Used for construction cards
2. **Resin**: Used for various cards
3. **Stone**: Used for higher-value cards
4. **Berries**: Used primarily for character cards

Resources are acquired through worker placement and card effects:

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

## Worker Placement

The worker placement system allows players to allocate workers to various locations to gather resources or trigger effects.

### Location Types

The game includes several types of locations:

- **Basic Locations**: Provide resources (wood, resin, stone, berries)
- **Card Locations**: Provide resources and cards
- **Token Locations**: Provide tokens and cards
- **Forest Locations**: Provide special effects based on forest cards

```python
self.locations = ['wood3', 'wood2_card', 'resin2', 'resin_card', 'card2_token', 'stone', 'berry_card', 'berry', 'forest_1', 'forest_2', 'forest_3', 'forest_4']
self.worker_slots_available = {
    'wood3': 1,
    'wood2_card': 4,
    'resin2': 1,
    'resin_card': 4,
    'card2_token': 4,
    'stone': 1,
    'berry_card': 1,
    'berry': 4,
    'forest_1': 1,
    'forest_2': 1,
    'forest_3': 1,
    'forest_4': 1
}
```

Forest locations are initialized in the game setup:

```python
self.forest_deck = list(forest_deck)  # Initialize the forest deck
self.forest = []  # Initialize the forest list
random.shuffle(self.forest_deck)  # Shuffle the forest deck before each new game
# Draw initial cards into the forest based on player count
forest_card_count = 4 if len(self.agents) >= 3 else 3
self.forest = self.draw_from_forest(forest_card_count)  # Draw initial cards into the forest
```

However, there are limitations in how forest locations are implemented:
- Forest card effects are implemented as placeholders
- The AI doesn't have a strategic approach to using forest locations
- There are issues handling special locations like lookout

### Worker Recall

Players can recall their workers once per season to reuse them:

```python
def recall_workers(self, agent, player_index):
    # Return all workers to the agent
    for resource_type in agent.worker_allocation:
        if resource_type == 'lookout':
            agent.lookout_slots_available += agent.worker_allocation[resource_type]
        else:
            self.worker_slots_available[resource_type] += agent.worker_allocation[resource_type]
        agent.worker_allocation[resource_type] = 0
    
    agent.workers = agent.max_workers
    agent.recalls += 1
    
    # Trigger Clock Tower effect if the agent has one
    clock_tower_card = next((card for card in agent.played_cards if card.name == "Clock Tower"), None)
    if clock_tower_card:
        clock_tower_trigger_effect(agent, self, None)
```

## Scoring System

The scoring system calculates points based on:

1. **Card Points**: Base points from cards
2. **Prosperity Cards**: Additional points based on specific conditions
3. **Events**: Points from claimed events

```python
def calculate_score(self):
    scores = []
    for agent in self.agents:
        # Base points from cards
        score = sum(card.points for card in agent.played_cards)
        
        # Points from prosperity cards
        for card in agent.prosperity_cards:
            if card.name == "Theater":
                score += theater_activation(agent)
            elif card.name == "Architect":
                score += architect_activation(agent)
            # ... other prosperity cards
        
        agent.score = score
        scores.append(score)
    return scores
```

## Events

The game includes basic events that players can claim when they meet specific conditions:

- **Monument**: Have 3 or more unique construction cards
- **Tour**: Have 3 or more red cards
- **Festival**: Have 3 or more green cards
- **Expedition**: Have 3 or more tan cards

```python
# Check for the monument action
blue_cards_count = sum(1 for card in self.played_cards if card.card_type == 'construction' and card.rarity == 'unique')
if blue_cards_count >= 3 and 'monument' not in game.claimed_events:
    basic_events.append('monument')
# ... other events
```

## Meadow System

The meadow is a shared area where cards are available for all players to play. It is replenished whenever a card is taken:

```python
def draw_to_meadow(self):
    # Replenish the meadow immediately after a card is taken
    new_cards = self.draw_cards(1)
    if new_cards:
        print(f"{new_cards[0].name} was drawn into the meadow")
        return new_cards
    else:
        return []
```

## Implemented Features

The game mechanics currently implement:

1. **Recalling workers** for each season
2. **Meadow** card system
3. **Hands** management
4. **Drawing cards** in summer
5. **Real card names, points, cost**
6. **15 card city limit**, including for the fool
7. **Unique cards** constraints
8. **Basic locations**
9. **Prosperity cards**
10. **Card rules** that affect other cards in play
11. **Forest locations** (basic implementation with placeholder effects)

## Partially Implemented Features

1. **Forest locations**: The locations exist and can be used, but:
   - Forest card effects are implemented as placeholders
   - The AI state representation needs updating to better handle forest cards
   - There are issues handling special locations like lookout

2. **Card effects**: Many effects are implemented but with limitations:
   - The Undertaker currently only chooses the first 3 cards from the meadow to discard
   - The Fool and Teacher currently only target the next player
   - The Crane has a fixed resource reduction strategy
   - The Judge is only used when necessary, not strategically

3. **Card interactions**: Basic interactions are implemented but with simplifications:
   - The AI prioritizes using Innkeepers over Judges or Cranes without strategic consideration
   - Gatherer-Harvester pair mechanics are not fully implemented

## Planned Features (V1)

The following features are planned but not yet implemented:

1. Card rules that add a worker location
2. Card rules that activate when a card is played
3. Special Events
4. King card rules
5. Haven and Journey mechanics
6. Occupation and bonus occupations
7. Occupation lock
8. Open Destination cards
9. Testing pause functionality
10. Improved Undertaker card selection logic

## Future Improvements (V2)

Future improvements include:

1. Address the CHOOSE TODOs throughout the code
2. Gatherer-Harvester pair mechanics
3. Extra forest locations for 4 players
4. Hand limit management when donating cards
5. Meadow replenishment logic
6. Passed player restrictions
7. Tiebreaker improvements
8. Deck reshuffling
9. Card counting strategy
10. Chapel and Shepherd implementation
11. Strategic decision-making for cards like Judge, Innkeeper, and Crane

## Limitations

The current implementation has several limitations:

1. Some card interactions are simplified
2. Not all card effects are fully implemented
3. Some edge cases in card interactions are not handled
4. Limited support for expansions (base game only)
5. Some heuristic assumptions are made in complex decision scenarios
6. The AI can "cheat" by seeing opponent hands in the state representation
7. Forest card effects are implemented as placeholders
8. The AI uses fixed strategies for cards like Undertaker, Judge, and Crane rather than making optimal choices