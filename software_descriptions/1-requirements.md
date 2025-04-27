# Everdell AI - Requirements

This document outlines the requirements for the Everdell AI project, organized by major features and their associated tasks. The checkbox notation indicates implementation status.

## Reinforcement Learning AI System

[x] 1. AI Agent Implementation
[x] 1.1 Base Reinforcement Learning Agent
[x] 1.1.1 Q-learning algorithm
[x] 1.1.2 State representation
[x] 1.1.3 Action selection mechanism
[x] 1.1.4 Learning rate and exploration strategies
[x] 1.1.5 Model saving and loading capabilities

[x] 1.2 Game-Specific Agent
[x] 1.2.1 Game-specific actions and decisions
[x] 1.2.2 Resource management
[x] 1.2.3 Card playing logic
[x] 1.2.4 Worker placement strategy

[x] 1.3 Training Process
[x] 1.3.1 Episode structure
[x] 1.3.2 Reward calculation
[x] 1.3.3 Learning updates
[x] 1.3.4 Performance tracking

[x] 1.4 Testing Mode
[x] 1.4.1 Model evaluation
[x] 1.4.2 User interaction during testing
[x] 1.4.3 AI move recommendations

## Game Engine

[x] 2. Game State Management
[x] 2.1 Turn Structure
[x] 2.1.1 Player turns
[x] 2.1.2 Season progression
[x] 2.1.3 Game end conditions

[x] 2.2 Resource System
[x] 2.2.1 Resource types (wood, resin, stone, berries)
[x] 2.2.2 Resource acquisition
[x] 2.2.3 Resource usage for card playing

[x] 2.3 Worker Placement
[x] 2.3.1 Worker allocation
[x] 2.3.2 Location types and effects
[x] 2.3.3 Worker recall mechanism

[x] 2.4 Scoring System
[x] 2.4.1 Point calculation
[x] 2.4.2 End-game scoring
[x] 2.4.3 Tiebreaker rules

## Card System

[x] 3. Card Types and Properties
[x] 3.1 Card Attributes
[x] 3.1.1 Name, type, rarity, points
[x] 3.1.2 Resource costs
[x] 3.1.3 Card colors and their significance

[x] 3.2 Card Effects
[x] 3.2.1 Activation effects
[x] 3.2.2 Trigger effects
[x] 3.2.3 Forest card effects (basic implementation with placeholder effects)

[x] 3.3 Card Interactions
[x] 3.3.1 Card synergies
[x] 3.3.2 Special card rules
[x] 3.3.3 Card effect resolution

[x] 3.4 Card Management
[x] 3.4.1 Deck management
[x] 3.4.2 Meadow system
[x] 3.4.3 Hand management
[x] 3.4.4 City building constraints

## User Interface

[x] 4. Training Interface
[x] 4.1 Configuration Options
[x] 4.1.1 Number of agents
[x] 4.1.2 Number of episodes
[x] 4.1.3 Agent randomization
[x] 4.1.4 Live view toggle

[x] 4.2 Progress Display
[x] 4.2.1 Episode counter
[x] 4.2.2 Turn counter
[x] 4.2.3 Training status indicators

[x] 4.3 Game State Visualization
[x] 4.3.1 Meadow display
[x] 4.3.2 Hand display
[x] 4.3.3 Resource display

[x] 4.4 Results Visualization
[x] 4.4.1 Chart selection
[x] 4.4.2 Performance metrics display
[x] 4.4.3 Training results analysis

## Data Visualization

[x] 5. Live Plotting
[x] 5.1 Real-time Visualization
[x] 5.1.1 TD error visualization
[x] 5.1.2 Score tracking
[x] 5.1.3 Win rate analysis

[x] 5.2 Chart Types
[x] 5.2.1 Training metrics charts
[x] 5.2.2 Card play frequency charts
[x] 5.2.3 Resource choice analysis charts

## Implemented Game Features

[x] 6. Core Game Mechanics
[x] 6.1 Recalling workers for each season
[x] 6.2 Meadow card system
[x] 6.3 Hand management
[x] 6.4 Drawing cards in summer
[x] 6.5 Card names, points, and costs
[x] 6.6 15 card city limit, including for the fool
[x] 6.7 Unique card constraints
[x] 6.8 Basic locations
[x] 6.9 Prosperity cards
[x] 6.10 Card rules that affect other cards in play
[x] 6.11 Forest locations (basic implementation)

## Partially Implemented Features

[~] 7. Partially Implemented Features
[~] 7.1 Forest locations (locations exist but AI state representation needs updating)
[~] 7.2 Card effects (many effects implemented but with limitations)
[~] 7.3 Card interactions (basic interactions implemented but with simplifications)
[~] 7.4 AI decision-making for special cards (currently uses fixed strategies)

## Planned Features (V1)

[ ] 8. V1 Planned Features
[ ] 8.1 Card rules that add a worker location
[ ] 8.2 Card rules that activate when a card is played
[ ] 8.3 Special Events
[ ] 8.4 King card rules
[ ] 8.5 Haven
[ ] 8.6 Journey
[ ] 8.7 Occupation and bonus occupations
[ ] 8.8 Occupation lock
[ ] 8.9 Open Destination cards
[ ] 8.10 Testing pause functionality
[ ] 8.11 Improved Undertaker card selection logic

## Future Improvements (V2)

[ ] 9. V2 Planned Features
[ ] 9.1 Address the CHOOSE TODOs throughout the code
[ ] 9.2 Gatherer-Harvester pair mechanics
[ ] 9.3 Extra forest locations for 4 players
[ ] 9.4 Hand limit management when donating cards
[ ] 9.5 Meadow replenishment logic
[ ] 9.6 Passed player restrictions
[ ] 9.7 Tiebreaker improvements
[ ] 9.8 Deck reshuffling
[ ] 9.9 Card counting strategy
[ ] 9.10 Chapel and Shepherd implementation
[ ] 9.11 AI strategic choice improvements for cards like Judge, Innkeeper, and Crane