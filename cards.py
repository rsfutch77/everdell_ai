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
        self.activation_effect = self.get_activation_effect()
        self.trigger_effect = self.get_trigger_effect()

    def trigger(self, player, game, card_played):
        if self.trigger_effect:
            self.trigger_effect(player, game, card_played)

    def activate(self, player, game):
        if self.activation_effect:
            self.activation_effect(player, game, self)
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
def undertaker_activation(player, game, *args):
    discarded_cards = game.meadow[:3]
    game.discard.extend(discarded_cards)
    game.meadow = game.meadow[3:]
    # Replenish the meadow with new cards from the deck
    for _ in range(3):
        game.meadow.extend(game.draw_to_meadow())
    print(f"Undertaker effect: Discarded cards from the meadow: {[card.name for card in discarded_cards]}")
    # Allow the player to pick a card from the meadow
    if game.meadow:
        # Build a list of actions for the AI to choose from
        available_actions = [('pick_card', card) for card in game.meadow]
        # Use the AI's choose_action method to choose a card
        action = player.choose_action(available_actions)
        chosen_card = action[1] if action and action[0] == 'pick_card' else None
        if chosen_card:
            # Update the Undertaker card pick frequency
            game.undertaker_card_pick_frequency[chosen_card.name] = game.undertaker_card_pick_frequency.get(chosen_card.name, 0) + 1
            game.meadow.remove(chosen_card)
            player.hand.append(chosen_card)
            print(f"Undertaker effect: Player picked {chosen_card.name} from the meadow")
            game.meadow.extend(game.draw_to_meadow())
    # Update the meadow display if a callback is set
    if game.meadow_update_callback:
        game.meadow_update_callback(game.meadow)
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
        if len(game.agents[next_player_index].played_cards) <= game.agents[next_player_index].city_limit:
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
def postal_pigeon_activation(player, game, *args):
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
    print(f"Discarded due to not being able to play: {[card.name for card in cards_to_discard]}")
    # AI selects one card from the revealed cards using its machine learning model
    if game.revealed_cards:
        # Build a list of options for the AI to choose from
        available_actions = [('pick_card', card) for card in game.revealed_cards]
        # Use the AI's select_action method to choose a card
        action = player.choose_action(available_actions)
        if action and action[0] == 'pick_card':
            # Discard any remaining revealed cards
            selected_card = action[1]
            remaining_cards = [card for card in game.revealed_cards if card != selected_card]
            print(f"Discarding remaining revealed cards: {[card.name for card in remaining_cards]}")
            game.discard_cards(game.revealed_cards)
            game.revealed_cards.clear()
            selected_card = action[1]
            game.play_card(player, selected_card, game.agents.index(player), game, 'play_card_with_pigeon')
            print(f"AI {game.agents.index(player)} immediately plays {selected_card.name} from the revealed cards.")
    else:
        print(f"AI {game.agents.index(player)} could not play any cards from the pigeon's effect.")
    print(f"Pigeon activation complete")
def historian_activation(player, _, card, *args):
    player.on_trigger.append(card)
def historian_trigger_effect(player, game, *args):
    # Historian's trigger effect is that the player draws a card
    player.draw_to_hand(game.draw_cards(min(1, player.max_cards_in_hand - len(player.hand))))
def shopkeeper_activation(player, _, card, *args):
    player.on_trigger.append(card)
def shopkeeper_trigger_effect(player, game, card_played):
    if card_played.card_type == 'character':
        player.berries += 1
        print(f"Shopkeeper effect: AI {game.agents.index(player)} gains 1 berry for playing a character card.")
def courthouse_activation(player, _, card, *args):
    player.on_trigger.append(card)
def courthouse_trigger_effect(player, game, card_played):
    if card_played.card_type == 'construction':
        available_actions = ['wood', 'resin', 'stone']
        # Use the AI's method to choose
        action = player.choose_action(available_actions)
        if action and action == 'wood':
            player.wood += 1
            game.courthouse_resource_choices['wood'] += 1
        elif action and action == 'resin':
            player.resin += 1
            game.courthouse_resource_choices['resin'] += 1
        elif action and action == 'stone':
            player.stone += 1
            game.courthouse_resource_choices['stone'] += 1
        print(f"Courthouse gains {action[0]}")
def innkeeper_activation(player, *args):
    pass  # Innkeeper card may have a different effect or no effect
def crane_activation(player, *args):
    pass  # Innkeeper card may have a different effect or no effect
def judge_activation(player, *args):
    pass  # Judge card may have a different effect or no effect
def crane_activation(player, *args):
    pass  # Crane card may have a different effect or no effect
def harvester_activation(player, *args):
    # Check if the player has both a Gatherer and a Farm
    has_gatherer = any(card.name == "Gatherer" for card in player.played_cards)
    has_farm = any(card.name == "Farm" for card in player.played_cards)
    
    if has_gatherer and has_farm:
        # Allow the player to pick one of the resources
        available_resources = ['wood', 'resin', 'stone']
        chosen_resource = player.choose_action(available_resources)
        
        if chosen_resource == 'wood':
            player.wood += 1
        elif chosen_resource == 'resin':
            player.resin += 1
        elif chosen_resource == 'stone':
            player.stone += 1
        
        print(f"Harvester activation: Player gains 1 {chosen_resource}.")
def shepherd_activation(player):
    pass  # Shepherd card may have a different effect or no effect
def barge_toad_activation(player, *args):
    # Calculate the number of farms in the player's city
    num_farms = sum(1 for card in player.played_cards if card.name == "Farm")
    # Gain two wood for each farm
    wood_gained = num_farms * 2
    player.wood += wood_gained
    print(f"Barge Toad activation: Player gains {wood_gained} wood for {num_farms} farms.")
def general_store_activation(player, *args):
    # Gain one berry
    berries_gained = 1
    # Check if the player has a Farm card
    if any(card.name == "Farm" for card in player.played_cards):
        berries_gained += 1
    player.berries += berries_gained
    print(f"General Store activation: Player gains {berries_gained} berries.")
def miner_mole_activation(player, game, *args):
    # Collect all green cards from opponents' played cards, excluding "Storehouse" and "Miner Mole"
    opponent_green_cards = [
        card for opponent in game.agents if opponent != player
        for card in opponent.played_cards
        if card.card_color == "green" and card.name not in ["Storehouse", "Miner Mole"]
    ]
    
    if opponent_green_cards:
        # Allow the player to choose one of the green cards to copy
        available_actions = [('copy_card', card) for card in opponent_green_cards]
        action = player.choose_action(available_actions)
        chosen_card = action[1] if action and action[0] == 'copy_card' else None
        
        if chosen_card:
            # Activate the chosen card's effect
            chosen_card.activate(player, game)
            print(f"Miner Mole activation: Player copies {chosen_card.name} from an opponent.")
def chip_sweep_activation(player, game, *args):
    # Filter the player's played cards to find those with a "green" card color
    green_cards = [card for card in player.played_cards if card.card_color == "green" and card.name != "Chip Sweep"]
    
    if green_cards:
        # Allow the player to choose one of the green cards to activate
        available_actions = [('activate_card', card) for card in green_cards]
        action = player.choose_action(available_actions)
        chosen_card = action[1] if action and action[0] == 'activate_card' else None
        
        if chosen_card:
            # Track the activation frequency of the chosen card
            game.chip_sweep_activation_frequency[chosen_card.name] = game.chip_sweep_activation_frequency.get(chosen_card.name, 0) + 1
            # Activate the chosen card
            chosen_card.activate(player, game)
            print(f"Chip Sweep activation: Player reactivates {chosen_card.name}.")
def ranger_activation(player, game, *args):
    # Retrieve a worker and allow the player to deploy it again
    if player.workers < player.max_workers:  # Check if any workers are deployed
        player.workers += 1
        # Choose a resource type to receive
        available_resources = ['wood3', 'wood2_card', 'resin2', 'resin_card', 'card2_token', 'stone', 'berry_card', 'berry']
        chosen_resource = player.choose_action(available_resources)
        if chosen_resource:
            player.receive_resources(chosen_resource)
        print(f"Ranger activation: Player retrieves a worker and receives {chosen_resource}.")
    else:
        print("Ranger activation failed: No workers are deployed to retrieve.")
    print("Ranger activation complete.")
def teacher_activation(player, game, *args):
    # Draw 2 cards to the player's hand
    new_cards = game.draw_cards(min(2, player.max_cards_in_hand - len(player.hand)))
    player.draw_to_hand(new_cards)
    # Update the teacher card draw frequency
    game.teacher_card_draw_frequency[len(new_cards)] += 1
    
    if len(new_cards) > 1:
        # Allow the player to choose one card to give to an opponent
        available_actions = [('give_card', card) for card in new_cards]
        action = player.choose_action(available_actions)
        chosen_card = action[1] if action and action[0] == 'give_card' else None

        player.hand.remove(chosen_card)
        # Find the next available player in the game to give the card to
        iterate_players = 0
        next_player_index = 0
        while True:
            next_player_index = (game.agents.index(player) + 1 + iterate_players) % len(game.agents)
            next_player = game.agents[next_player_index]
            if len(next_player.played_cards) <= next_player.city_limit:
                break
        if len(next_player.hand) < next_player.max_cards_in_hand:
            next_player.hand.append(chosen_card)
            # Update the teacher card giveaway frequency
            print(f"Teacher activation: Player gives {chosen_card.name} to opponent AI {next_player_index}.")
        else:
            game.discard_cards([chosen_card])
            print(f"Teacher activation: {chosen_card.name} discarded as opponent AI {next_player_index}'s hand is full.")
        game.teacher_card_giveaway_frequency[chosen_card.name] = game.teacher_card_giveaway_frequency.get(chosen_card.name, 0) + 1
        for card in new_cards:
            if card != chosen_card:
                # Update the teacher card kept frequency
                game.teacher_card_kept_frequency[card.name] = game.teacher_card_kept_frequency.get(card.name, 0) + 1
    elif len(new_cards) == 1:
        print("Teacher activation: Only one card was drawn, so no card was given to an opponent.")
    else:
        print("Teacher activation: No cards were drawn, so no card was given to an opponent.")
    print("Teacher activation complete.")
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
    "Undertaker": undertaker_activation,
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
    "Courthouse": courthouse_activation,
    "Courthouse": courthouse_activation,
    "Innkeeper": innkeeper_activation,
    "Crane": crane_activation,
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
    "Shopkeeper": shopkeeper_trigger_effect,
    "Courthouse": courthouse_trigger_effect,
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
    ("Shopkeeper"    , "character",    "unique",  1, 0, 0, 0, 2, 3, "blue"),
    ("Courthouse"    , "construction", "unique",  2, 1, 1, 2, 0, 2, "blue"),
    #Cards that reduce cost
    ("Innkeeper"     , "character",    "unique",  1, 0, 0, 0, 1, 3, "blue"),
    ("Judge"         , "character",    "unique",  2, 0, 0, 0, 3, 2, "blue"),
    ("Crane"         , "construction", "unique",  1, 0, 0, 1, 0, 2, "blue"),
    #Discards from Meadow
    ("Undertaker"    , "character",    "unique",  1, 0, 0, 0, 2, 2, "adventure"),
    #If/then cards
    ("Harvester"     , "character",    "common", 2, 0, 0, 0, 3, 4, "green"),
    #("Shepherd"     , "character",    "x",      0, 0, 0, 0, 0, 0, "x"),
    ("Barge Toad"    , "character",    "common", 1, 0, 0, 0, 2, 3, "green"),
    ("General Store" , "construction", "common", 1, 0, 1, 1, 0, 3, "green"),
    #Harvests
    ("Miner Mole"    , "character",    "common", 1, 0, 0, 0, 3, 3, "green"),
    ("Chip Sweep"    , "character",    "common", 2, 0, 0, 0, 3, 3, "green"),
    #Moves worker
    ("Ranger"        , "character",    "unique", 1, 0, 0, 0, 2, 2, "adventure"),
    #Gives to opponent
    ("Teacher"       , "character",    "common", 2, 0, 0, 0, 2, 3, "green"),
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
