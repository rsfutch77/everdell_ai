class Card:
    def __init__(self, name, points):
        self.name = name
        self.points = points

class AIPlayer:
    def select_card(self, hand, game_state):
        # Simple strategy: play the card with the highest points
        return max(hand, key=lambda card: card.points)

class Game:
    def __init__(self, deck, ai_player):
        self.deck = deck
        self.ai_player = ai_player
        self.turns = 5
        self.current_turn = 0
        self.played_cards = []

    def play_game(self):
        for _ in range(self.turns):
            self.play_turn()

    def play_turn(self):
        card_to_play = self.ai_player.select_card(self.deck, self.get_game_state())
        self.deck.remove(card_to_play)
        self.played_cards.append(card_to_play)
        self.current_turn += 1

    def get_game_state(self):
        # Placeholder for more complex game state
        return {'turn': self.current_turn, 'played_cards': self.played_cards}

    def calculate_score(self):
        return sum(card.points for card in self.played_cards)

if __name__ == "__main__":
    # Example setup
    deck = [Card('Card1', 3), Card('Card2', 5), Card('Card3', 2),
            Card('Card4', 4), Card('Card5', 1), Card('Card6', 6)]
    ai_player = AIPlayer()
    game = Game(deck, ai_player)
    game.play_game()
    print(f"Final score: {game.calculate_score()}")
