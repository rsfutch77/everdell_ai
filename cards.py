import tkinter as tk
from tkinter import messagebox

class Card:
    def __init__(self, name, card_type, rarity, points, wood=0, resin=0, stone=0, berries=0, quantity=1, card_color="green"):
        self.name = name
        self.card_type = card_type  # 'character', 'construction', etc.
        self.rarity = rarity  # 'unique' or 'common'
        self.points = points
        self.wood = wood
        self.resin = resin
        self.stone = stone
        self.berries = berries
        self.quantity = quantity
        self.card_color = card_color # e.g. 'prosperity'
        self.activation_effect = None if card_type == "forest" else self.get_activation_effect()
        self.trigger_effect = self.get_trigger_effect()

    def trigger(self, player, game, card_played):
        if self.trigger_effect:
            self.trigger_effect(player, game, card_played)

    def activate(self, player, game):
        if self.activation_effect and self.card_type != "forest":
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
    #TODO CHOOSE which cards the undertaker should discard instead of just the first three: AI is playing an Undertaker card. It currently only chooses the first 3 cards from the meadow to discard.
    for card in discarded_cards:
        game.undertaker_discard_frequency[card.name] = game.undertaker_discard_frequency.get(card.name, 0) + 1
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
            if len(player.hand) < player.max_cards_in_hand:
                player.hand.append(chosen_card)
                print(f"Undertaker effect: Player picked {chosen_card.name} from the meadow")
            else:
                game.discard_cards([chosen_card])
                print(f"Undertaker effect: {chosen_card.name} discarded as player's hand is full.")
            game.meadow.extend(game.draw_to_meadow())
    # Update the meadow display if a callback is set
    if game.meadow_update_callback:
        game.meadow_update_callback(game.meadow)
    print(f"Undertaker activation complete")
def resin_refinery_activation(player, *args):
    player.resin += 1
def fairgrounds_activation(player, game, *args):
    player.draw_to_hand(game.draw_cards(min(2, player.max_cards_in_hand - len(player.hand))), game)
def fool_activation(player, game, *args):
    fool_card = next((card for card in player.played_cards if card.name == "Fool"), None)
    #TODO CHOOSE a player for the fool instead of just the next player
    if len(game.agents) > 2:
        root = tk.Tk()
        root.withdraw()  # Hide the root window
        popup = tk.Toplevel(root)
        popup.title("Fool Card Warning")
        label = tk.Label(popup, text="AI is playing a Fool card in a game with more than two players. It currently only picks the next player with room for it instead of looking at which city would be advantageous to put the Fool in.")
        label.pack(padx=20, pady=20)
        if game.is_training_mode:
            popup.after(1000, popup.destroy)  # Destroy the popup after 1 second if in training mode
        else:
            button = tk.Button(popup, text="OK", command=popup.destroy)
            button.pack(pady=10)
    ###
    # Find the next available player in the game to give the card to
    next_player_index = game.agents.index(player)
    while True:
        next_player_index += 1
        if next_player_index > len(game.agents) - 1:
            next_player_index = 0
        next_player = game.agents[next_player_index]
        if next_player_index == game.agents.index(player):
            print(f"Fool card discarded due to error.")
            root = tk.Tk()
            root.withdraw()  # Hide the root window
            popup = tk.Toplevel(root)
            popup.title("Fool Error")
            label = tk.Label(popup, text="No suitable cities found for the fool. The AI does not yet check for full cities or cities already containing fools before activation. For now the card will be discarded.")
            label.pack(padx=20, pady=20)
            if game.is_training_mode:
                popup.after(1000, popup.destroy)  # Destroy the popup after 1 second if in training mode
            else:
                button = tk.Button(popup, text="OK", command=popup.destroy)
                button.pack(pady=10)
            break
        if len(game.agents[next_player_index].played_cards) <= game.agents[next_player_index].city_limit and not any(card.name == "Fool" for card in next_player.played_cards):
            # Move the Fool card to the next player's played cards
            next_player.played_cards.append(fool_card)
            print(f"Fool card played into AI {next_player_index} played cards by AI {game.agents.index(player)}")
            break
    player.played_cards.remove(fool_card)
def wanderer_activation(player, game, *args):
     # Draw cards for the Wanderer activation without adding it to played cards
     player.draw_to_hand(game.draw_cards(min(3, player.max_cards_in_hand - len(player.hand))), game)
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
    player.draw_to_hand(game.draw_cards(min(1, player.max_cards_in_hand - len(player.hand))), game)
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
        #TODO this is not printing the whole word
        print(f"Courthouse gains {action[0]}")
def innkeeper_activation(player, *args):
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
    green_cards = [card for card in player.played_cards if card.card_color == "green" and card.name != "Chip Sweep" and card.name != "Miner Mole"]
    
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
        # Choose a resource type where a worker is currently allocated
        allocated_resources = [resource for resource, count in player.worker_allocation.items() if count > 0]
        chosen_resource = player.choose_action(allocated_resources)
        player.workers += 1
        player.worker_allocation[chosen_resource] -= 1
        game.worker_slots_available[chosen_resource] += 1
        # Choose another spot
        available_resources = [resource for resource, slots in game.worker_slots_available.items() if slots > 0]
        if not available_resources:
            raise Exception("No available resources to choose from during Ranger activation.")
        
        new_chosen_resource = player.choose_action(available_resources)
        if new_chosen_resource:
            player.receive_resources(new_chosen_resource, game)
            print(f"Ranger activation: Player retrieves a worker and receives {new_chosen_resource}.")
        else:
            raise Exception("No resource chosen during Ranger activation.")
    else:
        print("Ranger activation failed: No workers are deployed to retrieve.")
    print("Ranger activation complete.")
def teacher_activation(player, game, *args):
    # Draw 2 cards to the player's hand
    new_cards = game.draw_cards(min(2, player.max_cards_in_hand - len(player.hand)))
    player.draw_to_hand(new_cards, game)
    # Update the teacher card draw frequency
    game.teacher_card_draw_frequency[len(new_cards)] += 1
    
    if len(new_cards) > 1:
        # Allow the player to choose one card to give to an opponent
        available_actions = [('give_card', card) for card in new_cards]
        action = player.choose_action(available_actions)
        chosen_card = action[1] if action and action[0] == 'give_card' else None

        player.hand.remove(chosen_card)
        #TODO CHOOSE a player for the teacher instead of just the next player
        # Find the next available player in the game to give the card to
        next_player_index = game.agents.index(player)
        while True:
            next_player_index += 1
            if next_player_index > len(game.agents) - 1:
                next_player_index = 0
            next_player = game.agents[next_player_index]
            if next_player_index == game.agents.index(player):
                root = tk.Tk()
                root.withdraw()  # Hide the root window
                popup = tk.Toplevel(root)
                popup.title("Teacher Warning")
                label = tk.Label(popup, text="Card was discarded since all opponent hands are full.")
                label.pack(padx=20, pady=20)
                if game.is_training_mode:
                    popup.after(1000, popup.destroy)  # Destroy the popup after 1 second if in training mode
                else:
                    button = tk.Button(popup, text="OK", command=popup.destroy)
                    button.pack(pady=10)
                game.discard_cards([chosen_card])
                print(f"Teacher activation: {chosen_card.name} discarded as all opponent AI hand's are full.")
                break
            if len(next_player.hand) < next_player.max_cards_in_hand:
                next_player.hand.append(chosen_card)
                # Update the teacher card giveaway frequency
                print(f"Teacher activation: Player gives {chosen_card.name} to opponent AI {next_player_index}.")
                game.teacher_card_giveaway_frequency[chosen_card.name] = game.teacher_card_giveaway_frequency.get(chosen_card.name, 0) + 1
                break
        for card in new_cards:
            if card != chosen_card:
                # Update the teacher card kept frequency
                game.teacher_card_kept_frequency[card.name] = game.teacher_card_kept_frequency.get(card.name, 0) + 1
    elif len(new_cards) == 1:
        print("Teacher activation: Only one card was drawn, so no card was given to an opponent.")
    else:
        print("Teacher activation: No cards were drawn, so no card was given to an opponent.")
    print("Teacher activation complete.")
def monk_activation(player, game, *args):
    # AI decides how many berries to give, up to 2
    berries_to_give = player.choose_berries_to_give(min(player.berries, 2), game)
    if berries_to_give > 0:
        # Find the next available player in the game to give the card to
        next_player_index = game.agents.index(player)
        while True:
            next_player_index += 1
            if next_player_index > len(game.agents) - 1:
                next_player_index = 0
            next_player = game.agents[next_player_index]
            break
            if next_player_index == game.agents.index(player):
                print("No suitable player found to give berries.")
                break
        # Give the decided number of berries to the next player and receive tokens
        player.berries -= berries_to_give
        player.berries_given_during_monk_activation = berries_to_give
        next_player.berries += berries_to_give
        player.add_tokens(berries_to_give)
        print(f"Monk activation: Player gives {berries_to_give} berries to AI {next_player_index} and receives {berries_to_give} tokens.")
def clock_tower_activation(player, *args):
    # When activated, the player receives 3 tokens
    player.add_tokens(3)
    print(f"Clock Tower activation: Player receives 3 tokens.")
    #This card does not get added to the trigger list because it triggers on recall isntead of on a card play
def clock_tower_trigger_effect(player, game, *args):
    # AI chooses a resource to reactivate a worker from
    available_resources = [resource for resource, count in player.worker_allocation.items() if count > 0]
    if available_resources:
        chosen_resource = player.choose_action(available_resources)
        if chosen_resource:
            # AI decides whether to lose a token
            available_actions = ['lose_token', 'keep_token']
            action = player.choose_action(available_actions)
            if action == 'lose_token':
                player.tokens = max(0, player.tokens - 1)
                # Provide the resources associated with the chosen resource
                player.workers += 1
                player.worker_allocation[chosen_resource] -= 1
                game.worker_slots_available[chosen_resource] += 1
                resource_type, cards_to_draw = player.receive_resources(chosen_resource, game)
                new_cards = game.draw_cards(cards_to_draw)
                if cards_to_draw > 0:
                    player.draw_to_hand(new_cards, game)
                print(f"Clock Tower trigger: Player chooses to lose 1 token and receives resources from {chosen_resource}.")
                print(f"Clock Tower trigger: Player reactivates a worker from {chosen_resource}.")
            else:
                print(f"Clock Tower trigger: Player chooses to keep tokens.")
    else:
        print(f"Clock Tower trigger: Nothing to activate")
def woodcarver_activation(player, *args):
    # Check if the player has at least 3 wood
    if player.wood >= 0:
        # Allow the player to choose how much wood to exchange for tokens, up to 3
        available_actions = list(range(min(4, player.wood + 1)))  # Options: 0 to min(3, player.wood)
        wood_to_exchange = player.choose_action(available_actions)
        if wood_to_exchange is not None:
            player.wood -= wood_to_exchange
            player.add_tokens(wood_to_exchange)
            print(f"Woodcarver activation: Player exchanges {wood_to_exchange} wood for {wood_to_exchange} tokens.")
    else:
        print("Woodcarver activation: Not enough wood to exchange.")
def peddler_activation(player, game, *args):
    # Calculate the total number of resources the player has
    total_resources = player.wood + player.resin + player.stone + player.berries

    if total_resources == 0:
        # Effect when the player has 0 resources
        print("Peddler activation: Player has 0 resources.")
        # Implement the effect for 0 resources here
    elif total_resources > 0:
        # Allow the player to choose how many resources to pay, up to 2
        max_resources_to_pay = min(2, total_resources)
        available_actions = list(range(max_resources_to_pay + 1))  # Options: 0 to max_resources_to_pay
        resources_to_pay = player.choose_action(available_actions)
        
        if resources_to_pay is not None:
            # Implement the effect based on the number of resources paid
            if resources_to_pay == 0:
                print("Peddler activation: Player chooses not to pay any resources.")
                # Implement the effect for paying 0 resources here
            elif resources_to_pay > 0:
                # Allow the player to choose which resources to give
                for _ in range(resources_to_pay):
                    available_resources = []
                    if player.wood > 0:
                        available_resources.append('wood')
                    if player.resin > 0:
                        available_resources.append('resin')
                    if player.stone > 0:
                        available_resources.append('stone')
                    if player.berries > 0:
                        available_resources.append('berries')
                    if available_resources:
                        chosen_resource = player.choose_action(available_resources)
                        if chosen_resource == 'wood':
                            player.wood -= 1
                        if chosen_resource == 'resin':
                            player.resin -= 1
                        elif chosen_resource == 'stone':
                            player.stone -= 1
                        elif chosen_resource == 'berries':
                            player.berries -= 1
                        game.peddler_pay_choices[chosen_resource] += 1
                    print(f"Peddler activation: Player pays resource: {chosen_resource}.")
                
                # Allow the player to choose which resources to receive
                resources_to_receive = []
                for _ in range(resources_to_pay):
                    chosen_resource = player.choose_action(['wood', 'resin', 'stone', 'berries'])
                    if chosen_resource:
                        resources_to_receive.append(chosen_resource)

                # Add the chosen resources to the player's inventory
                for resource in resources_to_receive:
                    if resource == 'wood':
                        player.wood += 1
                    elif resource == 'resin':
                        player.resin += 1
                    elif resource == 'stone':
                        player.stone += 1
                    elif resource == 'berries':
                        player.berries += 1
                    game.peddler_receive_choices[resource] += 1

                print(f"Peddler activation: Player receives {resources_to_receive}.")
def doctor_activation(player, game, *args):
    # Check if the player has at least 3 berries
    if player.berries >= 0:
        # Allow the player to choose how many berries to exchange for tokens, up to 3
        available_actions = list(range(min(4, player.berries + 1)))  # Options: 0 to min(3, player.berries)
        berries_to_exchange = player.choose_action(available_actions)
        if berries_to_exchange is not None:
            player.berries -= berries_to_exchange
            player.add_tokens(berries_to_exchange)
            print(f"Doctor activation: Player exchanges {berries_to_exchange} berries for {berries_to_exchange} tokens.")
    else:
        print("Doctor activation: Not enough berries to exchange.")
def queen_activation(player):
    pass  # Queen card may have a different effect or no effect
def university_activation(player):
    pass  # University card may have a different effect or no effect
def monastery_activation(player):
    pass  # Monastery card may have a different effect or no effect
def cemetery_activation(player):
    pass  # Cemetery card may have a different effect or no effect
def lookout_activation(player, game, *args):
    game.worker_slots_available['lookout'] += 1
def lookout_trigger_effect(player, game, card_played):
    # Example trigger effect for the Lookout card
    # Allow the player to choose a resource to gain
    available_resources = ['wood', 'resin', 'stone', 'berries']
    chosen_resource = player.choose_action(available_resources)
    if chosen_resource == 'wood':
        player.wood += 1
    elif chosen_resource == 'resin':
        player.resin += 1
    elif chosen_resource == 'stone':
        player.stone += 1
    elif chosen_resource == 'berries':
        player.berries += 1
    print(f"Lookout trigger: Player gains 1 {chosen_resource}.")
def storehouse_activation(player):
    pass  # Storehouse card may have a different effect or no effect
def chapel_activation(player):
    pass  # Chapel card may have a different effect or no effect
def post_office_activation(player):
    pass  # Post Office card may have a different effect or no effect
def inn_activation(player):
    pass  # Inn card may have a different effect or no effect
def ruins_activation(player, game, *args):
    # Filter the player's played cards to find constructions
    constructions = [card for card in player.played_cards if card.card_type == "construction"]
    
    if constructions:
        # Allow the player to choose one of the constructions to discard
        available_actions = [('discard_card', card) for card in constructions]
        action = player.choose_action(available_actions)
        chosen_card = action[1] if action and action[0] == 'discard_card' else None
        
        if chosen_card:
            # Discard the chosen construction card
            player.played_cards.remove(chosen_card)
            game.discard_cards([chosen_card])
            # Add the cost of the discarded card back to the player's resources
            player.wood += chosen_card.wood
            player.resin += chosen_card.resin
            player.stone += chosen_card.stone
            player.berries += chosen_card.berries
            print(f"Ruins activation: Player discards {chosen_card.name} and receives its cost back.")
    else:
        print("Dungeon activation: No constructions available to discard.")
def dungeon_activation(player):
    pass  # Dungeon card may have a different effect or no effect
def bard_activation(player, game, *args):
    
    # Allow the player to choose how many cards to discard, up to 5
    max_discard = min(5, len(player.hand))
    available_actions = list(range(max_discard + 1))  # Options: 0 to max_discard
    cards_to_discard = player.choose_action(available_actions)

    if cards_to_discard is not None:
        # Discard the chosen number of cards from the player's hand
        discarded_cards = player.hand[:cards_to_discard]
        player.hand = player.hand[cards_to_discard:]
        game.discard_cards(discarded_cards)
        player.add_tokens(cards_to_discard)
        print(f"Bard activation: Player discards {cards_to_discard} cards and receives {cards_to_discard} tokens.")

#Forest trigger functions
def forest_card_1_trigger(player, game, *args):
    # Example effect: Gain 1 wood
    player.wood += 1
    print(f"Forest Card 1 effect: Player gains 1 wood.")
def forest_card_2_trigger(player, game, *args):
    # Example effect: Gain 1 resin
    player.resin += 1
    print(f"Forest Card 2 effect: Player gains 1 resin.")
def forest_card_3_trigger(player, game, *args):
    # Example effect: Gain 1 stone
    player.stone += 1
    print(f"Forest Card 3 effect: Player gains 1 stone.")
def forest_card_4_trigger(player, game, *args):
    # Example effect: Gain 1 stone
    player.stone += 1
    print(f"Forest Card 4 effect: Player gains 1 stone.")

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
    "Shopkeeper": shopkeeper_activation,
    "Courthouse": courthouse_activation,
    "Innkeeper": innkeeper_activation,
    "Crane": crane_activation,
    "Judge": judge_activation,
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
}

trigger_effects = {
    "Historian": historian_trigger_effect,
    "Shopkeeper": shopkeeper_trigger_effect,
    "Courthouse": courthouse_trigger_effect,
    "Clock Tower": clock_tower_trigger_effect,
    #Forest triggers
    "Forest Card 1": forest_card_1_trigger,
    "Forest Card 2": forest_card_2_trigger,
    "Forest Card 3": forest_card_3_trigger,
    "Forest Card 4": forest_card_4_trigger,
}
        
# Define the forest deck
forest_deck = [
    ("Forest Card 1"),
    ("Forest Card 2"),
    ("Forest Card 3"),
    ("Forest Card 4"),
]

# Card Name, Points, Cost (Wood, Resin, Stone, Berries), Quantity in Deck
cards = [
    #Basic cards that just provide a bonus on activation/harvest
    ("Farm"          , "construction", "common",  1, 2, 1, 0, 0, 8, "green"),
    ("Mine"          , "construction", "common",  2, 1, 1, 1, 0, 3, "green"),
    ("Twig Barge"    , "construction", "common",  1, 1, 0, 1, 0, 3, "green"),
    ("Resin Refinery", "construction", "common",  1, 0, 1, 1, 0, 3, "green"),
    ("Fairgrounds"   , "construction", "unique",  3, 1, 2, 1, 0, 3, "green"),
    #Takes up space in opponent's city
    ("Fool"          , "character",    "unique", -2, 0, 0, 0, 3, 2, "tan"),
    #Does not take up space
    ("Wanderer"      , "character",    "common",  1, 0, 0, 0, 2, 3, "tan"),
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
    ("Postal Pigeon" , "character",    "common",  0, 0, 0, 0, 2, 3, "tan"),
    #Cards that activate on playing a card
    ("Historian"     , "character",    "unique",  1, 0, 0, 0, 2, 3, "blue"),
    ("Shopkeeper"    , "character",    "unique",  1, 0, 0, 0, 2, 3, "blue"),
    ("Courthouse"    , "construction", "unique",  2, 1, 1, 2, 0, 2, "blue"),
    #Cards that reduce cost
    ("Innkeeper"     , "character",    "unique",  1, 0, 0, 0, 1, 3, "blue"),
    ("Judge"         , "character",    "unique",  2, 0, 0, 0, 3, 2, "blue"),
    ("Crane"         , "construction", "unique",  1, 0, 0, 1, 0, 2, "blue"),
    #Discards from Meadow
    ("Undertaker"    , "character",    "unique",  1, 0, 0, 0, 2, 2, "tan"),
    #If/then cards
    ("Harvester"     , "character",    "common", 2, 0, 0, 0, 3, 4, "green"),
    #("Shepherd"     , "character",    "x",      0, 0, 0, 0, 0, 0, "x"),
    ("Barge Toad"    , "character",    "common", 1, 0, 0, 0, 2, 3, "green"),
    ("General Store" , "construction", "common", 1, 0, 1, 1, 0, 3, "green"),
    #Harvests
    ("Miner Mole"    , "character",    "common", 1, 0, 0, 0, 3, 3, "green"),
    ("Chip Sweep"    , "character",    "common", 2, 0, 0, 0, 3, 3, "green"),
    #Moves worker
    ("Ranger"        , "character",    "unique", 1, 0, 0, 0, 2, 2, "tan"),
    #Gives to opponent
    ("Teacher"       , "character",    "common", 2, 0, 0, 0, 2, 3, "green"),
    ("Monk"          , "character",    "unique", 0, 0, 0, 0, 1, 2, "green"),
    #Cards with pay requirements
    ("Clock Tower"   , "construction", "unique", 0, 3, 0, 1, 0, 3, "blue"),
    ("Woodcarver"    , "character",    "common", 2, 0, 0, 0, 2, 3, "green"),
    ("Peddler"       , "character",    "common", 1, 0, 0, 0, 2, 3, "green"),
    ("Doctor"        , "character",    "unique", 4, 0, 0, 0, 4, 2, "green"),
    #Cards with locations
    #("Queen", 5, 7, 2),
    #("University", 5, 7, 2),
    #("Monastery", 5, 7, 2),
    #("Cemetery", 5, 7, 2),
    ("Lookout"       , "construction", "unique", 2, 1, 1, 1, 0, 2, "red"),
    #("Storehouse", 5, 7, 3),
    #("Chapel"     , "x",    "x",      0, 0, 0, 0, 0, 0, "x"),
    #("Post Office", 5, 7, 3),
    #("Inn", 5, 7, 3),
    #Cards that discard
    ("Ruins"        , "construction", "common", 0, 0, 0, 0, 0, 3, "tan"),
    #("Dungeon", 5, 7, 3),
    ("Bard"         , "character",    "unique", 0, 0, 0, 0, 3, 2, "tan")
    
]
