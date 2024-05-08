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
    # Add more cards...
]

deck = [Card(name, points, cost) for name, points, cost in cards]
ai_player = ReinforcementLearningAgent(alpha=0.1, gamma=0.9, epsilon=0.1)
adversarial_ai_player = ReinforcementLearningAgent(alpha=0.1, gamma=0.9, epsilon=0.1)
game = AIGame(deck, ai_player, adversarial_ai_player)
num_episodes = 1000  # Number of episodes to train the AI
