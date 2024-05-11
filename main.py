from ai_game import Game as AIGame
from player import AIPlayer
from cards import cards, Card

deck = [Card(name, points, cost) for name, points, cost in cards]
number_of_agents = 2
# Replace ReinforcementLearningAgent with AIPlayer to ensure the agents have the necessary methods
agents = [AIPlayer(alpha=0.1, gamma=0.9, epsilon=0.1) for _ in range(number_of_agents)]
game = AIGame(deck, agents)
num_episodes = 100  # Number of episodes to train the AI
