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

Contributing
------------
Contributions to this project are welcome. Please fork the repository and submit a pull request with your changes.
