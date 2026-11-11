# Mystery Island: The Lost Lighthouse

An interactive Python text adventure. A storm has left you on Mystery Island.
Collect rope and a lantern, cross the damaged bridge, and restore the lighthouse
beacon before you run out of energy.

## Setup and run

Requires Python 3. Uses only the standard library; no packages, API keys,
database, or network connection are required. Verified with Python 3.12.3.

From the repository directory:

```sh
python3 main.py
```

If Python 3 is named `python` on your machine, run `python main.py`.
For a local environment that provides the assignment's exact `python` command:

```sh
python3 -m venv --without-pip .venv
source .venv/bin/activate
python main.py
python -m unittest discover -s tests -v
```

The activation command above is for bash/zsh. On Windows, use
`.venv\Scripts\activate` after creating the environment with your Python 3
interpreter. No pip is needed because the game has no external dependencies.

## Controls

Enter your explorer name. A blank name becomes `Explorer`.
The menu accepts numbers or these text commands:

| Number | Command | Action |
| --- | --- | --- |
| 1 | `forward`, `north`, `next` | Move to the next location |
| 2 | `back`, `south`, `backward` | Move to the previous location |
| 3 | `take`, `pickup`, `pick up` | Collect the object in this room |
| 4 | `inventory` | List collected objects |
| 5 | `energy` | Show remaining energy |
| 6 | `light`, `light beacon` | Light the lighthouse beacon |
| 7 | `quit`, `exit`, `q` | End this game |

You can also type `move jungle`, `move old bridge`, or another adjacent
location's name after `move`. `take rope` and `take lantern` name an object
explicitly. Commands ignore surrounding whitespace and capitalization:
` EXIT ` works. An invalid number, blank command, impossible move, or unavailable
action gives feedback and leaves game state unchanged.

After any ending, enter `y`/`yes` to replay or `n`/`no` to stop.
Invalid replay answers prompt again. Ctrl-C or end of input exits cleanly.

## Map and game rules

```text
Beach <-> Jungle <-> Cave <-> Old Bridge <-> Lighthouse
          rope      lantern     rope required to cross
```

- Start at Beach with 5 energy and an empty inventory.
- Each legal move to an adjacent location consumes exactly 1 energy.
  Arriving at a location does not charge a second cost.
- Collect rope in Jungle and a lantern in Cave. Pickups are free and unique.
  Revisiting a room cannot give you another copy of its object.
- Crossing the bridge between Old Bridge and Lighthouse requires rope.
  A blocked crossing consumes no energy and does not move the player.
- Inventory/energy checks, rejected commands, and repeated pickups are free.
- Light the beacon only at Lighthouse with both rope and lantern and energy
  greater than 0. This free action wins immediately and summons the rescue boat.
- Using the final energy point on a legal move causes immediate loss, even
  when that move reaches Lighthouse. Energy never becomes negative.
- Quit ends the current game without counting as a win or energy-exhaustion loss.
- Ended games accept no more gameplay actions. Replay creates fresh state and
  a new inventory, retaining only the explorer's name.
- Rules are deterministic. There is no resting or random energy recovery.

The important decisions are whether to collect each required object, whether
to spend scarce energy moving backward, and whether to light the beacon before
making another move. Skipping an object blocks progress; unnecessary movement
can cause loss.

## Example demonstrations

After entering your name, a complete winning path is:

```text
1 -> 3 -> 1 -> 3 -> 1 -> 1 -> 6 -> n
```

This visits all five locations, collects rope and lantern, and lights the beacon
with 1 energy remaining. The ending includes:

```text
You restored the lighthouse beacon! A rescue boat is coming!

Congratulations! The rescue boat followed your beacon.
You escaped Mystery Island! You won the game!
```

A losing path is `1 -> 2 -> 1 -> 2 -> 1 -> n`. The fifth move uses the final
energy point and prints `You ran out of energy. Game over!`.

An invalid-input demonstration is `banana -> 5 -> EXIT -> n`. The invalid
command prompts a retry, the energy check still shows 5, and `EXIT` quits.

For replay, use `1 -> 3 -> 7 -> y -> 4 -> 7 -> n`. The second game starts
at Beach with 5 energy and prints `Inventory: empty`.

## Function design

`main.py` handles terminal input, scenes, the menu, endings, and replay.
Its `if __name__ == "__main__"` guard prevents an import from starting the game.

`game.py` contains the location dictionary and game decisions. It never calls
`input()` or `print()`. Player state is a dictionary containing name, location,
energy, inventory, game_over, and won. Inventory is a list because the game
needs a small ordered collection and simple membership checks.

| Function | Responsibility |
| --- | --- |
| `new_game(name)` | Return fresh initial state, with a newly created inventory |
| `available_actions(player)` | Return commands relevant to the current room |
| `can_cross_bridge(inventory)` | Return a boolean without changing anything |
| `move_player(player, destination)` | Validate adjacency/rope; move and charge energy |
| `pick_up_item(player, requested_item)` | Add a locally available object once |
| `show_inventory(inventory)` | Return readable inventory text |
| `light_beacon(player)` | Check location/items/energy and set victory flags |
| `apply_action(player, action)` | Normalize and dispatch one command; return feedback |
| `is_win(player)` | Return the game's victory flag |
| `read_input(prompt)` | Read terminal input and handle EOF/Ctrl-C |
| `show_title()` | Display mission and instructions |
| `show_scene(player)` | Display location, energy, and uncollected object |
| `show_menu(player)` | Display controls and movement destinations |
| `choose_move()` | Read a command, converting ended input into quit |
| `show_outcome(player)` | Display the appropriate win/lose/quit ending |
| `ask_replay()` | Validate replay input and return a boolean |
| `main()` | Repeat games and stop when replay is declined |

Rule functions change the supplied player dictionary when an action succeeds,
and return text for the CLI to display. Rejected commands change nothing.
Tests can call these functions without interactive typing.

## Tests and acceptance evidence

Run all tests:

```sh
python3 -m unittest discover -s tests -v
```

Or use the assignment's `python -m unittest discover -s tests -v` after activating
the environment. There are 30 meaningful unittest tests, including all T1–T10:

| Rule | Test |
| --- | --- |
| T1: initial Beach, 5 energy, empty inventory | `test_t1_new_game_starts_at_beach_with_five_energy_and_empty_inventory` |
| T2: invalid input leaves state unchanged | `test_t2_invalid_commands_leave_all_state_unchanged` |
| T3: legal move costs exactly once | `test_t3_legal_move_changes_location_and_costs_exactly_one_energy` |
| T4: invalid movement costs nothing | `test_t4_wrong_direction_and_nonadjacent_moves_have_no_cost` |
| T5: unique rope pickup | `test_t5_rope_is_collected_once_without_energy_cost` |
| T6: bridge requires rope | `test_t6_bridge_is_blocked_without_rope` |
| T7: lighthouse requires lantern | `test_t7_lighthouse_cannot_be_lit_without_lantern` |
| T8: complete winning path | `test_t8_complete_winning_path_has_required_items_and_one_energy` |
| T9: loss at zero energy | `test_t9_fifth_legal_move_causes_loss_at_zero` |
| T10: replay creates fresh state | `test_t10_replay_resets_state_and_creates_a_separate_inventory` |

Additional tests cover lantern uniqueness, missing/wrong objects, wrong-location
victory, the final-energy move into Lighthouse, stopped games, normalized commands,
and independent inventories. Terminal tests run real subprocesses to verify
winning, losing, invalid input, replay after every ending, and safe imports.

Full execution output is in [docs/TEST_RESULTS.txt](docs/TEST_RESULTS.txt).

## Learning evidence and final submission

See [docs/LEARNING_LOG.md](docs/LEARNING_LOG.md) for two documented assistant
experiments, reflection prompts, and defence questions. At the learner's explicit
request, AI completed the implementation, tests, and documentation after reviewing
the original draft. The experiments are attributed to the assistant; they do not
claim that the learner ran them or has demonstrated mastery.

The learner still needs to perform an independent demonstration, answer the
defence questions, write their personal reflection, and obtain mentor/peer review.

Repository: https://github.com/maihwe/easy-track-mystery-island-

Record the submitted revision with:

```sh
git rev-parse HEAD
python3 --version
```

Submit the repository URL and final commit SHA with this README, test output,
your learning evidence, and your personal reflection.

## Known limits

Terminal only; no saved games, website, graphics, database, or AI API.
Forward/north and back/south are directions along the linear route, not a
two-dimensional compass map. The shortest winning route has only one spare
energy point; there is no alternative win path or energy recovery. The game-rule
API expects a player dictionary created by `new_game()`, not arbitrary corrupt
state. Name is retained on replay. Automated tests verify behavior, not the
learner's individual understanding.
