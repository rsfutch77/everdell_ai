# Everdell AI - Requirements

This document outlines the requirements for the Everdell AI project, organized by major features and their associated tasks. The checkbox notation indicates implementation status.

## Reinforcement Learning AI System

[ ] 1. AI Agent Implementation
[ ] 1.1 Base Reinforcement Learning Agent
[ ] 1.1.1 Q-learning algorithm
[ ] 1.1.2 State representation
[ ] 1.1.3 Action selection mechanism
[ ] 1.1.4 Learning rate and exploration strategies
[ ] 1.1.5 Model saving and loading capabilities

[ ] 1.2 Game-Specific Agent
[ ] 1.2.1 Game-specific actions and decisions
[ ] 1.2.2 Resource management
[ ] 1.2.3 Card playing logic
[ ] 1.2.4 Worker placement strategy

[ ] 1.3 Training Process
[ ] 1.3.1 Episode structure
[ ] 1.3.2 Reward calculation
[ ] 1.3.3 Learning updates
[ ] 1.3.4 Performance tracking

[ ] 1.4 Testing Mode
[ ] 1.4.1 Model evaluation
[ ] 1.4.2 User interaction during testing
[ ] 1.4.3 AI move recommendations

## Game Engine

[ ] 2. Game State Management
[ ] 2.1 Turn Structure
[ ] 2.1.1 Player turns
[ ] 2.1.2 Season progression
[ ] 2.1.3 Game end conditions

[ ] 2.2 Resource System
[ ] 2.2.1 Resource types (wood, resin, stone, berries)
[ ] 2.2.2 Resource acquisition
[ ] 2.2.3 Resource usage for card playing

[ ] 2.3 Worker Placement
[ ] 2.3.1 Worker allocation
[ ] 2.3.2 Location types and effects
[ ] 2.3.3 Worker recall mechanism

[ ] 2.4 Scoring System
[ ] 2.4.1 Point calculation
[ ] 2.4.2 End-game scoring
[ ] 2.4.3 Tiebreaker rules

## Card System

[ ] 3. Card Types and Properties
[ ] 3.1 Card Attributes
[ ] 3.1.1 Name, type, rarity, points
[ ] 3.1.2 Resource costs
[ ] 3.1.3 Card colors and their significance

[ ] 3.2 Card Effects
[ ] 3.2.1 Activation effects
[ ] 3.2.2 Trigger effects
[ ] 3.2.3 Forest card effects

[ ] 3.3 Card Interactions
[ ] 3.3.1 Card synergies
[ ] 3.3.2 Special card rules
[ ] 3.3.3 Card effect resolution

[ ] 3.4 Card Management
[ ] 3.4.1 Deck management
[ ] 3.4.2 Meadow system
[ ] 3.4.3 Hand management
[ ] 3.4.4 City building constraints

## User Interface

[ ] 4. Training Interface
[ ] 4.1 Configuration Options
[ ] 4.1.1 Number of agents
[ ] 4.1.2 Number of episodes
[ ] 4.1.3 Agent randomization
[ ] 4.1.4 Live view toggle

[ ] 4.2 Progress Display
[ ] 4.2.1 Episode counter
[ ] 4.2.2 Turn counter
[ ] 4.2.3 Training status indicators

[ ] 4.3 Game State Visualization
[ ] 4.3.1 Meadow display
[ ] 4.3.2 Hand display
[ ] 4.3.3 Resource display

[ ] 4.4 Results Visualization
[ ] 4.4.1 Chart selection
[ ] 4.4.2 Performance metrics display
[ ] 4.4.3 Training results analysis

## Data Visualization

[ ] 5. Live Plotting
[ ] 5.1 Real-time Visualization
[ ] 5.1.1 TD error visualization
[ ] 5.1.2 Score tracking
[ ] 5.1.3 Win rate analysis

[ ] 5.2 Chart Types
[ ] 5.2.1 Training metrics charts
[ ] 5.2.2 Card play frequency charts
[ ] 5.2.3 Resource choice analysis charts

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

## Planned Features (V1)

[ ] 7. V1 Planned Features
[ ] 7.1 Card rules that add a worker location
[ ] 7.2 Card rules that activate when a card is played
[ ] 7.3 Forest locations (AI needs state updated with which forest cards are in which location)
[ ] 7.4 Special Events
[ ] 7.5 King card rules
[ ] 7.6 Haven
[ ] 7.7 Journey
[ ] 7.8 Occupation and bonus occupations
[ ] 7.9 Occupation lock
[ ] 7.10 Open Destination cards
[ ] 7.11 Testing pause functionality
[ ] 7.12 Undertaker card selection logic

## Future Improvements (V2)

[ ] 8. V2 Planned Features
[ ] 8.1 Address the CHOOSE TODOs throughout the code
[ ] 8.2 Gatherer-Harvester pair mechanics
[ ] 8.3 Extra forest locations for 4 players
[ ] 8.4 Hand limit management when donating cards
[ ] 8.5 Meadow replenishment logic
[ ] 8.6 Passed player restrictions
[ ] 8.7 Tiebreaker improvements
[ ] 8.8 Deck reshuffling
[ ] 8.9 Card counting strategy
[ ] 8.10 Chapel and Shepherd implementation