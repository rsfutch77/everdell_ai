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
Once the app is started, it is recommended to train with at least 100 episodes.
Enter the number of Episodes in the text box.
At this stage it is recommended to train with only two players, but ideally we will finish the 4 player rules and you can then train with a randomized number of players which should result in a more capable AI against a variety of player counts.
Once your settings are entered, click the "Train" button.
Training 100 epiosdes takes about 1 minute on my old Gen 3 i7.
When training is complete it will show some charts about the most commonly played cards that you can use to judge whether the training was effective and then use those same common strategies against your friends. 

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
11. Shared and limited locations (including the rangers ability)

Below is a list of game functions that are not yet handled:
V1 Plan:
#TODO V1 Card rules that add a worker location
#TODO V1 Card rules that activate when a card is played
#TODO V1 Forest locations (ai needs state updated with which forrest cards are in which location)
#TODO V1 Special Events
#TODO V1 King card rules
#TODO V1 Haven
#TODO V1 Journey
#TODO V1 Occupation and bonus occupations (i.e. Ranger adding another dungeon spot)
#TODO V1 Occupation lock
#TODO V1 Open Destination cards (currently the available action is only added for cards in the player's own city)
#TODO V1 When testing, pause after each draw to select the correct cards into all positions and wait for a continue button
#TODO V1 AI should choose which cards to discard for the undertaker rather than just picking the first 3 in the meadow
V2 Plan:
#TODO V2 address the CHOOSE TODOs throughout the code
#TODO V2 Gatherers should only add points for pairs with Harvesters, not just any lone Harvester.
#TODO V2 Harvesters should only grant resources when paired.
#TODO V2 Extra forrest locations when there are 4 players
#TODO V2 Discarding cards that would be over the hand limit when donating cards to an opponent
#TODO V2 Drawing all cards from the meadow before replenishing when multiple cards are drawn from the meadow
#TODO V2 If a player has passed, they can not be given any resources or cards
#TODO V2 In the case of ties, the player with more events wins, if there is still a tie, then count resources
#TODO V2 Re-shuffling an empty deck
#TODO V2 A very smart AI would count cards and change what to play based on the likelihood of the remaining cards in the deck being drawn. This is not currently in the state representation.
#TODO V2 The Chapel and Shepherd are not implemented yet because they are annoying

AI Limitiations and Future Improvements
---------------
See the TODOs with the CHOOSE tag throughout the code that identify places where we currently make heuristic assumptions that would prefferably be AI choices. Most of these are rare cases or cases that would be complex to implement via AI so I have left these for later.

Contributing
------------
Contributions to this project are welcome. Please fork the repository and submit a pull request with your changes.

Bonus
------------
Check out this cool way to play Everdell online: https://github.com/ymichael/everdell
If there's any interest, we could probably connect these two apps to play against an AI with your friends. 
