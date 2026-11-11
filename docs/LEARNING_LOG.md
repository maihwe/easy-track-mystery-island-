# Learning log and defence preparation

These entries describe explanations and experiments performed by the assistant
during this session. They are evidence of AI assistance, not a claim that the
learner performed the experiments or has mastered the topics. Add your own
independent experiment and conclusion before submitting individual learning
evidence.

## Entry 1: Energy, conditions, and stopping the loop

**Topic:** Integer state, legal-action costs, and the loss condition.

**AI explanation:** Only successful movement should consume energy, and it
should consume exactly one point. After that move, reaching zero must end the
game before another action is accepted. Invalid actions must leave state alone.

**Assistant experiment:** In the original game, the choices
`1 -> 2 -> 1 -> 1 -> 1 -> 1 -> 1` caused energy to become -1: exploration
subtracted two points even when only one remained. In the completed game,
`forward -> back -> forward -> back -> forward` consumes exactly five points.
`test_t9_fifth_legal_move_causes_loss_at_zero` checks that the result is energy 0,
game_over True, and won False. The final-energy Lighthouse test also checks that
the player cannot light the beacon after the loss.

**Assistant conclusion:** Centralizing energy changes in `move_player()` makes
the cost explicit. Setting game_over when energy reaches zero, then rejecting
further actions, prevents negative energy and late victories in normal play.

**Your independent experiment:** Run a losing path and an invalid command before
a move. Record the energy before and after each action.

**Your conclusion:** To be written in your own words after the experiment.

## Entry 2: Lists, functions, and replay state

**Topic:** Inventory membership and creating a fresh mutable list.

**AI explanation:** `item in inventory` checks whether a list contains an item.
Before appending, check whether it is already present. Each replay must create
its own list; sharing the old inventory would carry objects between games.
`return` sends a value to the caller, while `print()` writes terminal output.

**Assistant experiment:** `test_t5_rope_is_collected_once_without_energy_cost`
collects rope, attempts another pickup, and compares the whole state with a
saved copy. The second pickup changes nothing. The replay acceptance test
creates another game and verifies its inventory is a different list. Adding
`map` to that new list does not affect the original game's rope and lantern.
CLI tests additionally verify an empty inventory after replay from win, loss,
and quit. All of these checks passed in the saved test run.

**Assistant conclusion:** `new_game()` creates a new list on each call. Membership
checks prevent duplicate objects, and separating rules from input/output lets
tests inspect both returned feedback and state changes without interactive typing.

**Your independent experiment:** Collect rope, quit, replay, and show inventory.
Then call `can_cross_bridge([])` and `can_cross_bridge(['rope'])` in a Python
shell. Record the returned values and explain why the function does not print.

**Your conclusion:** To be written in your own words after the experiment.

## Individual defence questions 

1. Why is energy an integer, location a string, and inventory a list?
2. What stops the inner game loop, and what stops the outer replay loop?
3. Trace one invalid action and explain why it changes no player state.
4. Show a function that returns a boolean. How does its caller use that result?
5. Why does replay call `new_game()` instead of resetting only energy?
6. Show the energy regression test and explain the original negative-energy bug.
7. Why is arriving at Lighthouse insufficient to win?
8. What did you test independently after receiving AI assistance?

## Personal reflection

Complete this yourself after running the experiments and explaining the code:

> The concept I understand now that I didn't before is…

Include the original misunderstanding, your experiment, the result, and why the
result supports your explanation. Obtain mentor/peer review before submission.
