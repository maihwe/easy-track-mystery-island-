"""Deterministic game rules, with no interactive input or printing."""

LOCATIONS = {
    "Beach": {
        "description": "Waves surround your wrecked boat. A trail leads into Jungle.",
        "forward": "Jungle", "back": None, "item": None,
    },
    "Jungle": {
        "description": "Vines cover the trail. A coil of rope may help at the bridge.",
        "forward": "Cave", "back": "Beach", "item": "rope",
    },
    "Cave": {
        "description": "A lantern waits in the cave. Its flame can restore the beacon.",
        "forward": "Old Bridge", "back": "Jungle", "item": "lantern",
    },
    "Old Bridge": {
        "description": "The damaged bridge leads to Lighthouse. You need rope to cross.",
        "forward": "Lighthouse", "back": "Cave", "item": None,
    },
    "Lighthouse": {
        "description": "The dark beacon needs your lantern. Light it to signal rescue!",
        "forward": None, "back": "Old Bridge", "item": None,
    },
}

ALIASES = {
    "1": "forward", "north": "forward", "next": "forward",
    "2": "back", "south": "back", "backward": "back",
    "3": "take", "pickup": "take", "pick up": "take",
    "4": "inventory", "5": "energy", "6": "light", "light beacon": "light",
    "7": "quit", "q": "quit", "exit": "quit",
}


def new_game(name="Explorer"):
    """Return fresh player state, including a separate inventory for each game."""
    return {
        "name": name.strip() or "Explorer",
        "location": "Beach",
        "energy": 5,
        "inventory": [],
        "game_over": False,
        "won": False,
    }


def can_cross_bridge(inventory):
    """Return whether an inventory contains the rope needed for the bridge."""
    return "rope" in inventory


def is_win(player):
    """Return whether this game ended in victory."""
    return player["won"]


def available_actions(player):
    """List actions relevant here; item gates are explained when attempted."""
    if player["game_over"]:
        return []
    room = LOCATIONS[player["location"]]
    actions = []
    if room["forward"]:
        actions.append("forward")
    if room["back"]:
        actions.append("back")
    if room["item"] and room["item"] not in player["inventory"]:
        actions.append("take")
    if player["location"] == "Lighthouse":
        actions.append("light")
    return actions + ["inventory", "energy", "quit"]


def show_inventory(inventory):
    """Return inventory text so the CLI can print it without changing state."""
    return "Inventory: " + (", ".join(inventory) if inventory else "empty")


def move_player(player, destination):
    """Move to an adjacent location, charging one energy only on success."""
    if player["game_over"]:
        return "This game has ended. Start a new game to play again."
    current = player["location"]
    room = LOCATIONS[current]
    if destination is None or destination not in (room["forward"], room["back"]):
        return "You cannot move there from here. No energy was used."
    crossing_bridge = {current, destination} == {"Old Bridge", "Lighthouse"}
    if crossing_bridge and not can_cross_bridge(player["inventory"]):
        return "The bridge is blocked. You need rope. No energy was used."

    player["location"] = destination
    player["energy"] = max(0, player["energy"] - 1)
    if player["energy"] == 0:
        player["game_over"] = True
    return f"You moved to {destination} and used 1 energy."


def pick_up_item(player, requested_item=None):
    """Collect the room's object once, without consuming energy."""
    if player["game_over"]:
        return "This game has ended. Start a new game to play again."
    item = LOCATIONS[player["location"]]["item"]
    if item is None or (requested_item is not None and requested_item != item):
        return "That object is not here. No energy was used."
    if item in player["inventory"]:
        return f"You already collected the {item}. No energy was used."
    player["inventory"].append(item)
    return f"You picked up the {item}!"


def light_beacon(player):
    """Win only at Lighthouse with rope, lantern, and remaining energy."""
    if player["game_over"]:
        return "This game has ended. Start a new game to play again."
    if player["location"] != "Lighthouse":
        return "You must reach Lighthouse before lighting its beacon."
    if not can_cross_bridge(player["inventory"]):
        return "You need rope to secure yourself at the damaged lighthouse."
    if "lantern" not in player["inventory"]:
        return "You need a lantern to light the lighthouse beacon."
    if player["energy"] <= 0:
        return "You have no energy left to light the beacon."
    player["won"] = True
    player["game_over"] = True
    return "You restored the lighthouse beacon! A rescue boat is coming!"


def apply_action(player, action):
    """Apply one command and return feedback; rejected commands change nothing."""
    if player["game_over"]:
        return "This game has ended. Start a new game to play again."
    if not isinstance(action, str):
        return "Invalid choice. Enter a number from 1 to 7 or a listed command."
    action = action.strip().lower()
    action = ALIASES.get(action, action)
    room = LOCATIONS[player["location"]]

    if action in ("forward", "back"):
        return move_player(player, room[action])
    if action.startswith("move "):
        target = action[5:].strip()
        destination = None
        for name in LOCATIONS:
            if name.lower() == target:
                destination = name
                break
        return move_player(player, destination)
    if action == "take":
        return pick_up_item(player)
    if action.startswith("take "):
        return pick_up_item(player, action[5:].strip())
    if action == "inventory":
        return show_inventory(player["inventory"])
    if action == "energy":
        return f"Your current energy: {player['energy']}"
    if action == "light":
        return light_beacon(player)
    if action == "quit":
        player["game_over"] = True
        return "You decided to end your adventure."
    return "Invalid choice. Enter a number from 1 to 7 or a listed command."
