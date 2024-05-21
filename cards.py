
class Card:
    def __init__(self, name, points, wood, resin, berries, quantity):
        self.name = name
        self.points = points
        self.wood = wood
        self.resin = resin
        self.berries = berries
        self.quantity = quantity
        

#Card Name, Points, Cost (Wood, Resin, Stone, Berries), Quantity in Deck
cards = [
    #Basic cards that just provide a bonus on activation/harvest
    ("Farm"          ,  1, 2, 1, 0, 0, 8),
    ("Mine"          ,  2, 1, 1, 1, 0, 3),
    ("Twig Barge"    ,  1, 1, 0, 1, 0, 3), 
    ("Resin Refinery",  1, 0, 1, 1, 0, 3),
    ("Fairgrounds"   ,  3, 1, 2, 1, 0, 3),
    #Takes up space in opponent's city
    ("Fool"          , -2, 0, 0, 0, 3, 2),
    #Does not take up space
    ("Wanderer"      ,  1, 0, 0, 0, 2, 3), 
    #Prosperity cards
    ("Theater"       ,  3, 3, 1, 1, 0, 2),   
    ("Architect"     ,  2, 0, 0, 0, 4, 2),   
    ("Palace"        ,  1, 2, 3, 3, 0, 2),
    ("Gatherer"      ,  2, 0, 0, 0, 2, 4),
    ("School"        ,  2, 2, 2, 0, 0, 2),
    ("Castle"        ,  4, 2, 3, 3, 0, 2),
    ("Ever Tree"     ,  5, 3, 3, 3, 0, 2),
    ("King"          ,  4, 0, 0, 0, 6, 2),
    #Cards that reveal
    #("Postal Pigeon", 5, 7, 3),
    #Cards that activate on playing a card
    #("Historian", 5, 7, 3),
    #("Shopkeeper", 5, 7, 3),
    #("Courthouse", 5, 7, 2),
    #Cards that reduce cost
    #("Innkeeper", 5, 7, 3),
    #("Judge", 5, 7, 2),
    #("Crane", 5, 7, 3),
    #Discards from Meadow
    #("Undertaker", 5, 7, 2),
    #If/then cards
    #("Harvester", 5, 7, 4),
    #("Shepherd", 5, 7, 2),
    #("Barge Toad", 5, 7, 3),
    #("General Store", 5, 7, 3),
    #Harvests
    #("Miner Mole", 5, 7, 3),
    #("Chip Sweep", 5, 7, 3),
    #Moves worker
    #("Ranger", 5, 7, 2),
    #Gives to opponent
    #("Teacher", 5, 7, 3),
    #("Monk", 5, 7, 2),
    #Cards with pay requirements
    #("Clock Tower", 5, 7, 3),
    #("Woodcarver", 5, 7, 3),
    #("Peddler", 5, 7, 3),
    #("Doctor", 5, 7, 2),
    #Cards with locations
    #("Queen", 5, 7, 2),
    #("University", 5, 7, 2),
    #("Monastery", 5, 7, 2),
    #("Cemetery", 5, 7, 2),
    #("Lookout", 5, 7, 2),
    #("Storehouse", 5, 7, 3),
    #("Chapel", 5, 7, 2),
    #("Post Office", 5, 7, 3),
    #("Inn", 5, 7, 3),
    #Cards that discard
    #("Ruins", 5, 7, 3),
    #("Dungeon", 5, 7, 3),
    #("Bard", 5, 7, 3),
]