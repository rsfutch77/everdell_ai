from ai_game import Card, AIPlayer, AdversarialAIPlayer, Game as AIGame, ReinforcementLearningAgent

cards = [
    ("Card1", 3),
    ("Card2", 2),
    ("Card3", 4),
    ("Card4", 1),
    ("Card5", 5),
    ("Card6", 6),
    ("Card7", 3),
    ("Card8", 2),
    ("Card9", 7),
    ("Card10", 2),
    ("Card11", 3),
    ("Card12", 1),
    ("Card13", 4),
    ("Card14", 5),
    ("Card15", 6),
    # Add more cards...
]

deck = [Card(name, points) for name, points in cards]
ai_player = AIPlayer()
adversarial_ai_player = AdversarialAIPlayer()
game = AIGame(deck, ai_player, adversarial_ai_player)
num_episodes = 1000  # Number of episodes to train the AI
