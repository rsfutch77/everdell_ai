
class Card:
    def __init__(self, name, points, cost):
        self.name = name
        self.points = points
        self.cost = cost  # Assign the fixed cost

#Card Name, Points, Cost, Quantity in Deck
cards = [
    ("Card1", 2, 2, 6),
    ("Card2", 2, 1, 6),
    ("Card3", 2, 3, 4), 
    ("Card4", 3, 2, 4),
    ("Card5", 3, 3, 4),
    ("Card6", 4, 4, 2),
    ("Card7", 4, 5, 2), 
    ("Card8", 5, 7, 2),  
]