from ai_game import Card, Game as AIGame, ReinforcementLearningAgent

cards = [
    ("Card1", 3, 2),
    ("Card2", 2, 1),
    ("Card3", 4, 3),
    ("Card4", 1, 1),
    ("Card5", 5, 4),
    ("Card6", 6, 5),
    ("Card7", 3, 2),
    ("Card8", 2, 1),
    ("Card9", 7, 6),
    ("Card10", 2, 1),
    ("Card11", 3, 2),
    ("Card12", 1, 1),
    ("Card13", 4, 3),
    ("Card14", 5, 4),
    ("Card15", 6, 5),
]

deck = [Card(name, points, cost) for name, points, cost in cards]
number_of_agents = 2
agents = [ReinforcementLearningAgent(alpha=0.1, gamma=0.9, epsilon=0.1) for _ in range(number_of_agents)]
game = AIGame(deck, agents)
num_episodes = 100  # Number of episodes to train the AI
