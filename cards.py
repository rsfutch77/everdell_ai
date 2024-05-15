
class Card:
    def __init__(self, name, points, cost):
        self.name = name
        self.points = points
        self.cost = cost  # Assign the fixed cost

#Card Name, Points, Cost, Quantity in Deck
cards = [
    ("Card1", 2, 2, 10),
    ("Card2", 2, 1, 10),
    ("Card3", 2, 3, 7), 
    ("Card4", 3, 2, 7),
    ("Card5", 3, 3, 7),
    ("Card6", 4, 4, 3),
    ("Card7", 4, 5, 3), 
    ("Card8", 5, 7, 3),  
]