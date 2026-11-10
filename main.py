print("==============================")
print("     THE LOST LIGHTHOUSE")
print("       MYSTERY ISLAND")
print("==============================")

print("Welcome, brave explorer!")
print()
print("Your mission:")
print("A terrible storm destroyed your boat.")
print("You have washed ashore on Mystery Island.")
print("Find a way to reach the lighthouse.")
print("Restore its beacon and escape the island.")
print()

player_name = input("What is your name, explorer? ")

print()
print("Welcome to Mystery Island,", player_name)
print("Your adventure begins now!")

energy = 10
has_rope = False
has_key = False
has_crossed_bridge = False
beacon_lit = False
rescued = False

print()
print("Your starting energy:", energy)

while energy > 0:
    print()
    print("===== ISLAND MENU =====")
    print("1. Explore the island")
    print("2. Rest")
    print("3. Check energy")
    print("4. Cross the bridge")
    print("5. Enter the lighthouse")
    print("6. Call the rescue boat!")
    print("7. Quit game")

    choice = input("Choose an option (1-7): ").strip()

    if choice == "1":
        energy -= 2
        print("You explored the island.")
        print("You lost 2 energy.")

        if not has_rope:
            has_rope = True
            print("You found a rope!")

        elif not has_key:
            has_key = True
            print("You found a lighthouse key!")

        else:
            print("You found nothing else.")

    elif choice == "2":
        if energy < 10:
            energy = energy + 1
            print("You rested and recovered 1 energy.")
        else:
            print("Your energy is already full.")

    elif choice == "3":
        print("Your current energy:", energy)

    elif choice == "4":
        if has_rope:
            has_crossed_bridge = True
            print("You used the rope to cross the damaged bridge!")
            print("You have reached the lighthouse area.")
        else:
            print("The bridge is damaged.")
            print("You need a rope to cross it.")

    elif choice == "5":
        if not has_crossed_bridge:
            print("You must cross the bridge first.")
        elif not has_key:
            print("The lighthouse is locked.")
            print("You need the lighthouse key.")
        else:
            beacon_lit = True
            print("You unlocked the lighthouse!")
            print("You restored the lighthouse beacon!")
            print("The beacon is shining across the sea!")

    elif choice == "6":
        if beacon_lit:
            rescued = True
            print("You signalled the rescue boat!")
            print("The rescue boat has spotted the lighthouse beacon!")
            print("You have been rescued!")
            print("Congratulations! You won the game!")
            break
        else:
            print("The rescue boat cannot locate you.")
            print("You must restore the lighthouse beacon first.")
    elif choice == "7":
        break

    else:
        print("Invalid choice. Please select 1, 2, 3, 4, 5, 6 or 7.")

print()

if rescued:
    print("You escaped Mystery Island!")
elif energy <= 0:
    print("You ran out of energy.")
    print("Game over!")
else:
    print("You decided to leave the island.")
    print("Your adventure has ended.")