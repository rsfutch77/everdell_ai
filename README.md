AI Card Game
============

Overview
--------
This project implements a card game where players are controlled by AI agents using reinforcement learning. The agents learn to play cards to maximize their points while managing their resources.

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

Below is a list of game functions that are not yet handled:
V1 Plan:
- Real card rules that don't do anything until end game
- Real card rules that affect other cards in play
- Real card rules that simply gain stuff when played
- Real card rules that add a worker location
- Real card rules that activate when a card is played
- Real card rules that can change the cost of a card to play
- Both harvests
- Basic Events
- Shared locations
- Forest locations
- Special Events
- Haven
- Journey
- Occupation
- Occupation lock
- Open Destination cards
- Add ID# and details of each card to game state (if needed?)
- When testing, pause after each draw to select the correct cards into all positions and wait for a continue button
V2 Plan:
- Extra locations when there are 4 players
- Discarding cards that would be over the hand limit when donating cards to an opponent
- Drawing all cards from the meadow before replenishing when multiple cards are drawn from the meadow
- If a player has passed, they can not be given any resources or cards
- In the case of ties, the player with more events wins, if there is still a tie, then count resources
- Re-shuffling an empty deck in training mode
- AI deciding which person to give the fool to (currently just picks the next player)

AI Limitiations
---------------
- 

Contributing
------------
Contributions to this project are welcome. Please fork the repository and submit a pull request with your changes.
