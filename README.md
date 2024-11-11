Everdell AI
============

Overview
--------
The goal of this project is to train an AI to play Everdell. Note that you cannot actually play Everdell using this app, it is only for training an AI and testing it while using the real game. The AI trains by Generative Adversarial play against another AI. Then you can switch to test mode where you tell the AI what cards are on your board and it will recommend a best course of action. No expansions are included.

Setup
-----
To run the game, you will need Python 3.x installed on your system.

1. Clone the repository to your local machine.
2. Install the required dependencies by running `pip install -r requirements.txt`.

Running the Game
----------------
To start the game, run the `main.py` script from the command line:

```
python main.py
```

Training the AI
---------------
The AI agents can be trained by running the `train_model` function within `ui.py`. This function takes the number of episodes to train as an argument.

```
from ui import train_model
train_model(root, num_agents_entry, num_episodes_entry, randomize_agents_var)
```

Game Functions
---------------
Below is a list of game functions that are handled:

1. Recalling workers for each season
2. Meadow
3. Hands
4. Drawing cards in summer
5. Real card names, points, cost
6. 15 card city limit, including for the fool
7. Unique cards
8. Basic locations
9. Prosperity cards
10. Card rules that affect other cards in play

Below is a list of game functions that are not yet handled:
V1 Plan:
- Exceptions/warnings for AI limitations below
- Card rules that add a worker location
- Card rules that activate when a card is played
- Both harvests
- Basic Events
- Shared and limited locations (including the rangers ability)
- Forest locations
- Special Events
- King card rules
- Haven
- Journey
- Occupation and bonus occupations (i.e. Ranger adding another dungeon spot)
- Occupation lock
- Open Destination cards
- Add ID# and details of each card to game state (if needed?)
- When testing, pause after each draw to select the correct cards into all positions and wait for a continue button
- AI should choose which cards to discard for the undertaker rather than just picking the first 3 in the meadow
V2 Plan:
- play_card currently prioritizes taking cards from the meadow, but we need the ai to choose either the one from the hand or the meadow
- Gatherers should only add points for pairs with Harvesters, not just any lone Harvester.
- Similarly, harvesters should only grant resources when paired.
- Extra locations when there are 4 players
- Discarding cards that would be over the hand limit when donating cards to an opponent
- Drawing all cards from the meadow before replenishing when multiple cards are drawn from the meadow
- If a player has passed, they can not be given any resources or cards
- In the case of ties, the player with more events wins, if there is still a tie, then count resources
- Re-shuffling an empty deck in training mode
- The Chapel and Shepherd are not implemented yet because they are annoying

AI Limitiations and Future Improvements
---------------
- The crane currently only reduces the cost of resources starting with stone and any other resources if there is any leftover, the AI should be able to choose which of any combination of the resources to reduce
- The AI currently has a fixed setting to choose the next resource on the list to replace another resource with when using the judge. Ideally the AI would should be able to choose which resource to swap if there is more than one option. 
- The AI currently prioritizes using innkeepers, then cranes, then judges, but ideally it should be able to choose between these. This also skews the stats towards innkeepers and away from judges. 
- The AI currently only uses the judge when it has to, but in theory it could choose to use the judge even when it could otherwise afford the card

Contributing
------------
Contributions to this project are welcome. Please fork the repository and submit a pull request with your changes.

Bonus
------------
Check out this cool way to play Everdell online: https://github.com/ymichael/everdell
If there's any interest, we could probably connect these two apps to play against an AI with your friends. 
