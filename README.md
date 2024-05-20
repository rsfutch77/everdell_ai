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

1. Seasons
2. Meadow
3. Hands

Below is a list of game functions that are not yet handled:

1. Basic Events
2. Special Events
3. Forest Locations
4. Haven
5. Journey
6. Real card names, points, cost
7. Real resources
8. Occupation
9. Occupation lock
10. Real card rules
11. Fools occupation
12. Wanderer free spot
13. Dungeon
14. Ruins
15. 


AI Limitiations
---------------
- 

Contributing
------------
Contributions to this project are welcome. Please fork the repository and submit a pull request with your changes.
