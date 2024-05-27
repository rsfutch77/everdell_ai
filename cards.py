class Card:
    def __init__(self, name, card_type, rarity, points, wood, resin, stone, berries, quantity, card_color):
        self.name = name
        self.card_type = card_type  # 'character', 'construction', etc.
        self.card_type = card_type  # 'character', 'construction', or 'prosperity'
        self.rarity = rarity  # 'unique' or 'common'
        self.points = points
        self.wood = wood
        self.resin = resin
        self.stone = stone
        self.berries = berries
        self.quantity = quantity
        self.card_color = card_color
        self.card_color = None  # Initialize card_color attribute
        self.activation_effect = self.get_activation_effect()
        self.trigger_effect = self.get_trigger_effect()

    def trigger(self, player, game):
        if self.trigger_effect:
            self.trigger_effect(player, game)

    def activate(self, player, game):
        if self.activation_effect:
            self.activation_effect(player, game)
        if self.card_type == 'prosperity':
            player.prosperity_cards.append(self)  # Add prosperity card to player's list for endgame scoring

    def get_activation_effect(self):
        return activation_effects.get(self.name, None)

    def get_trigger_effect(self):
        return trigger_effects.get(self.name, None)

# Define activation effects for cards
def farm_activation(player, *args):
    player.berries += 1
def mine_activation(player, *args):
    player.stone += 1
def twig_barge_activation(player, *args):
    player.wood += 2
def resin_refinery_activation(player, *args):
    player.resin += 1
def fairgrounds_activation(player, game, *args):
    player.draw_to_hand(game.draw_cards(min(2, player.max_cards_in_hand - len(player.hand))))
def fool_activation(player, game, *args):
    # Find the next available player in the game to give the fool to
    iterate_players = 0
    next_player_index = 0
    while True:
        next_player_index = (game.agents.index(player) + 1 + iterate_players) % len(game.agents)
        next_player = game.agents[next_player_index]
        if len(game.agents[next_player_index].played_cards) < game.agents[next_player_index].city_limit - 1:
            break
    # Move the Fool card to the next player's played cards
    fool_card = next((card for card in player.played_cards if card.name == "Fool"), None)
    if fool_card:
        player.played_cards.remove(fool_card)
        next_player.played_cards.append(fool_card)
        print(f"Fool card played into opponent's played cards by AI {game.agents.index(player)}")
def wanderer_activation(player, game, *args):
     # Draw cards for the Wanderer activation without adding it to played cards
     player.draw_to_hand(game.draw_cards(min(3, player.max_cards_in_hand - len(player.hand))))
     # Remove the Wanderer card from the player's hand
     wanderer_card = next((card for card in player.played_cards if card.name == "Wanderer"), None)
     if wanderer_card:
         player.played_cards.remove(wanderer_card)
         # Instead of adding to played_cards, add to a separate list that doesn't count towards the city limit
         player.non_city_cards.append(wanderer_card)
         print(f"Wanderer card activated by AI {game.agents.index(player)} but does not occupy space in city")
def theater_activation(player, game, *args):
    unique_characters = set()
    for card in player.played_cards:
        if card.card_type == 'character' and card.rarity == 'unique':
            unique_characters.add(card.name)
    return len(unique_characters)  # Add one point for each unique character
def architect_activation(player, *args):
    # Return the number of resin and stone the player has, maximizing at 6
    return min(6, player.resin + player.stone)
def palace_activation(player, *args):
    unique_constructions = set()
    for card in player.played_cards:
        if card.card_type == 'construction' and card.rarity == 'unique':
            unique_constructions.add(card.name)
    return len(unique_constructions)  # Return the number of unique construction cards
def gatherer_activation(player, *args):
    # Check for the presence of a card named "Harvester" in the played cards
    if any(card.name == "Harvester" for card in player.played_cards):
        return 3
    return 0
def school_activation(player, *args):
    common_characters = sum(1 for card in player.played_cards if card.card_type == 'character' and card.rarity == 'common')
    return common_characters
def castle_activation(player, *args):
    common_construction = sum(1 for card in player.played_cards if card.card_type == 'construction' and card.rarity == 'common')
    return common_construction
def ever_tree_activation(player, *args):
    # Add 1 point for each prosperity card the player ha 
    return len(player.prosperity_cards)
def king_activation(player, *args):
    pass
def postal_pigeon_activation(player, game):
    # Reveal 2 cards from the deck
    game.reveal_cards(2)
    # Remove any cards with more than 3 points from the revealed cards and add them to the discard list
    cards_to_discard = [card for card in game.revealed_cards if card.points > 3]
    # Remove any unique cards from the revealed cards that match the player's played cards or cannot be played
    unique_played_card_names = {card.name for card in player.played_cards if card.rarity == 'unique' and card.name != "Fool"}
    cards_to_discard += [card for card in game.revealed_cards if card.name in unique_played_card_names]
    game.revealed_cards = [card for card in game.revealed_cards if card not in cards_to_discard]
    game.discard_cards(cards_to_discard)
    print(f"Postal Pigeon revealed: {[card.name for card in game.revealed_cards]}")
    print(f"Discarded: {[card.name for card in cards_to_discard]}")
    # AI selects one card from the revealed cards using its machine learning model
    if game.revealed_cards:
        # Build a list of options for the AI to choose from
        available_actions = [('pick_card', card) for card in game.revealed_cards]
        # Use the AI's select_action method to choose a card
        action = player.choose_action(available_actions)
        if action and action[0] == 'pick_card':
            # Discard any remaining revealed cards
            print(f"Discarding remaining revealed cards: {[card.name for card in game.revealed_cards]}")
            game.discard_cards(game.revealed_cards)
            game.revealed_cards.clear()
            selected_card = action[1]
            game.play_card(player, selected_card, game.agents.index(player), game)
            print(f"AI {game.agents.index(player)} immediately plays {selected_card.name} from the revealed cards.")
    else:
        print(f"AI {game.agents.index(player)} could not play any cards from the pigeon's effect.")
def historian_activation(player, game):
    # Historian card's activation effect is to be added to the on_trigger list
    historian_card = next((card for card in player.hand if card.name == "Historian"), None)
    if historian_card:
        player.on_trigger.append(historian_card)
def historian_trigger_effect(player, game):
    # Historian's trigger effect is that the player draws a card
    player.draw_to_hand(game.draw_cards(min(1, player.max_cards_in_hand - len(player.hand))))
def shopkeeper_activation(player):
    pass  # Shopkeeper card may have a different effect or no effect
def courthouse_activation(player):
    pass  # Courthouse card may have a different effect or no effect
def innkeeper_activation(player):
    pass  # Innkeeper card may have a different effect or no effect
def judge_activation(player):
    pass  # Judge card may have a different effect or no effect
def crane_activation(player):
    pass  # Crane card may have a different effect or no effect
def undertaker_activation(player):
    pass  # Undertaker card may have a different effect or no effect
def harvester_activation(player):
    pass  # Harvester card may have a different effect or no effect
def shepherd_activation(player):
    pass  # Shepherd card may have a different effect or no effect
def barge_toad_activation(player):
    pass  # Barge Toad card may have a different effect or no effect
def general_store_activation(player):
    pass  # General Store card may have a different effect or no effect
def miner_mole_activation(player):
    pass  # Miner Mole card may have a different effect or no effect
def chip_sweep_activation(player):
    pass  # Chip Sweep card may have a different effect or no effect
def ranger_activation(player):
    pass  # Ranger card may have a different effect or no effect
def teacher_activation(player):
    pass  # Teacher card may have a different effect or no effect
def monk_activation(player):
    pass  # Monk card may have a different effect or no effect
def clock_tower_activation(player):
    pass  # Clock Tower card may have a different effect or no effect
def woodcarver_activation(player):
    pass  # Woodcarver card may have a different effect or no effect
def peddler_activation(player):
    pass  # Peddler card may have a different effect or no effect
def doctor_activation(player):
    pass  # Doctor card may have a different effect or no effect
def queen_activation(player):
    pass  # Queen card may have a different effect or no effect
def university_activation(player):
    pass  # University card may have a different effect or no effect
def monastery_activation(player):
    pass  # Monastery card may have a different effect or no effect
def cemetery_activation(player):
    pass  # Cemetery card may have a different effect or no effect
def lookout_activation(player):
    pass  # Lookout card may have a different effect or no effect
def storehouse_activation(player):
    pass  # Storehouse card may have a different effect or no effect
def chapel_activation(player):
    pass  # Chapel card may have a different effect or no effect
def post_office_activation(player):
    pass  # Post Office card may have a different effect or no effect
def inn_activation(player):
    pass  # Inn card may have a different effect or no effect
def ruins_activation(player):
    pass  # Ruins card may have a different effect or no effect
def dungeon_activation(player):
    pass  # Dungeon card may have a different effect or no effect
def bard_activation(player):
    pass  # Bard card may have a different effect or no effect

# Map card names to their activation functions
activation_effects = {
    "Farm": farm_activation,
    "Mine": mine_activation,
    "Twig Barge": twig_barge_activation,
    "Resin Refinery": resin_refinery_activation,
    "Fairgrounds": fairgrounds_activation,
    "Fool": fool_activation,
    "Wanderer": wanderer_activation,
    "Theater": theater_activation,
    "Architect": architect_activation,
    "Palace": palace_activation,
    "Gatherer": gatherer_activation,
    "School": school_activation,
    "Castle": castle_activation,
    "Ever Tree": ever_tree_activation,
    "King": king_activation,
    "Postal Pigeon": postal_pigeon_activation,
    "Historian": historian_activation,
    "Historian": historian_activation,
    "Shopkeeper": shopkeeper_activation,
    "Courthouse": courthouse_activation,
    "Innkeeper": innkeeper_activation,
    "Judge": judge_activation,
    "Crane": crane_activation,
    "Undertaker": undertaker_activation,
    "Harvester": harvester_activation,
    "Shepherd": shepherd_activation,
    "Barge Toad": barge_toad_activation,
    "General Store": general_store_activation,
    "Miner Mole": miner_mole_activation,
    "Chip Sweep": chip_sweep_activation,
    "Ranger": ranger_activation,
    "Teacher": teacher_activation,
    "Monk": monk_activation,
    "Clock Tower": clock_tower_activation,
    "Woodcarver": woodcarver_activation,
    "Peddler": peddler_activation,
    "Doctor": doctor_activation,
    "Queen": queen_activation,
    "University": university_activation,
    "Monastery": monastery_activation,
    "Cemetery": cemetery_activation,
    "Lookout": lookout_activation,
    "Storehouse": storehouse_activation,
    "Chapel": chapel_activation,
    "Post Office": post_office_activation,
    "Inn": inn_activation,
    "Ruins": ruins_activation,
    "Dungeon": dungeon_activation,
    "Bard": bard_activation,
    # Add other card activation functions here
}

# Map card names to their trigger functions
trigger_effects = {
    "Historian": historian_trigger_effect,
    # Add other card trigger functions here
}
        

#Card Name, Points, Cost (Wood, Resin, Stone, Berries), Quantity in Deck
cards = [
    #Basic cards that just provide a bonus on activation/harvest
    ("Farm"          , "construction", "common",  1, 2, 1, 0, 0, 8, "green"),
    ("Mine"          , "construction", "common",  2, 1, 1, 1, 0, 3, "green"),
    ("Twig Barge"    , "construction", "common",  1, 1, 0, 1, 0, 3, "green"),
    ("Resin Refinery", "construction", "common",  1, 0, 1, 1, 0, 3, "green"),
    ("Fairgrounds"   , "construction", "unique",  3, 1, 2, 1, 0, 3, "green"),
    #Takes up space in opponent's city
    ("Fool"          , "character",    "unique", -2, 0, 0, 0, 3, 2, "adventure"),
    #Does not take up space
    ("Wanderer"      , "character",    "common",  1, 0, 0, 0, 2, 3, "adventure"),
    #Prosperity cards
    ("Theater"       , "construction", "unique",  3, 3, 1, 1, 0, 2, "prosperity"),
    ("Architect"     , "character",    "unique",  2, 0, 0, 0, 4, 2, "prosperity"),
    ("Palace"        , "construction", "unique",  1, 2, 3, 3, 0, 2, "prosperity"),
    ("Gatherer"      , "character",    "common",  2, 0, 0, 0, 2, 4, "prosperity"),
    ("School"        , "construction", "unique",  2, 2, 2, 0, 0, 2, "prosperity"),
    ("Castle"        , "construction", "unique",  4, 2, 3, 3, 0, 2, "prosperity"),
    ("Ever Tree"     , "construction", "unique",  5, 3, 3, 3, 0, 2, "prosperity"),
    ("King"          , "character",    "unique",  4, 0, 0, 0, 6, 2, "prosperity"),
    #Cards that reveal
    ("Postal Pigeon" , "character",    "common",  0, 0, 0, 0, 2, 3, "adventure"),
    #Cards that activate on playing a card
    ("Historian"     , "character",    "unique",  1, 0, 0, 0, 2, 3, "blue"),
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
