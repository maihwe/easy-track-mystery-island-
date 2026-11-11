"""Run the Mystery Island terminal adventure."""

from game import LOCATIONS, apply_action, available_actions, is_win, new_game


def read_input(prompt):
    """Read a line, or return None when input ends or the player presses Ctrl-C."""
    try:
        return input(prompt)
    except (EOFError, KeyboardInterrupt):
        print()
        return None


def show_title():
    """Explain the mission and the rules before the first game."""
    print("==============================")
    print("     THE LOST LIGHTHOUSE")
    print("       MYSTERY ISLAND")
    print("==============================")
    print("A terrible storm destroyed your boat. You washed ashore on Mystery Island.")
    print("Find rope in Jungle and a lantern in Cave. Reach Lighthouse and light its beacon.")
    print("You start with 5 energy. Every legal move costs 1; other actions are free.")
    print("At 0 energy you lose, even if you have just reached Lighthouse.")
    print("Choose a menu number or type a command. Type quit or exit to leave.")


def show_scene(player):
    """Display the current room, energy, and any uncollected object."""
    location = player["location"]
    room = LOCATIONS[location]
    print(f"\n===== {location.upper()} =====")
    print(f"Explorer: {player['name']} | Energy: {player['energy']}")
    print(room["description"])
    if room["item"] and room["item"] not in player["inventory"]:
        print(f"You see a {room['item']}. Use take to collect it.")


def show_menu(player):
    """Show fixed menu numbers and the destinations beside movement choices."""
    room = LOCATIONS[player["location"]]
    print(f"1. Move forward ({room['forward'] or 'no path'})")
    print(f"2. Move back ({room['back'] or 'no path'})")
    print("3. Pick up the object here")
    print("4. Show inventory")
    print("5. Check energy")
    print("6. Light the lighthouse beacon")
    print("7. Quit game")
    print("Actions here: " + ", ".join(available_actions(player)))


def choose_move():
    """Return the player's command; ending terminal input means quit."""
    choice = read_input("Choose an option (1-7) or command: ")
    if choice is None:
        return "quit"
    return choice.strip().lower()


def show_outcome(player):
    """Print a distinct message for winning, losing, or quitting."""
    if is_win(player):
        print("\nCongratulations! The rescue boat followed your beacon.")
        print("You escaped Mystery Island! You won the game!")
    elif player["energy"] == 0:
        print("\nYou ran out of energy. Game over!")
    else:
        print("\nYou quit the game. Your adventure has ended.")


def ask_replay():
    """Ask again on invalid replay input and return a boolean."""
    while True:
        answer = read_input("Play again? (y/n): ")
        if answer is None:
            return False
        answer = answer.strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no", "q", "quit", "exit"):
            return False
        print("Please enter y or n.")


def main():
    """Run complete games, creating fresh state on each replay."""
    show_title()
    name = read_input("What is your name, explorer? ")
    if name is None:
        print("Goodbye, explorer!")
        return

    while True:
        player = new_game(name)
        print(f"\nWelcome to Mystery Island, {player['name']}!")
        while not player["game_over"]:
            show_scene(player)
            show_menu(player)
            print(apply_action(player, choose_move()))
        show_outcome(player)
        if not ask_replay():
            break
    print("Thanks for playing!")


if __name__ == "__main__":
    main()
