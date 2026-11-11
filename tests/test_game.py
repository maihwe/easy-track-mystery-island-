"""Acceptance tests for game rules, without terminal input."""

import unittest
from copy import deepcopy

from game import (
    apply_action, available_actions, can_cross_bridge, is_win, light_beacon,
    move_player, new_game, pick_up_item,
)


class GameTests(unittest.TestCase):
    def setUp(self):
        self.player = new_game("Ada")

    def play(self, *actions):
        for action in actions:
            apply_action(self.player, action)

    def test_t1_new_game_starts_at_beach_with_five_energy_and_empty_inventory(self):
        self.assertEqual(self.player, {
            "name": "Ada", "location": "Beach", "energy": 5,
            "inventory": [], "game_over": False, "won": False,
        })

    def test_t2_invalid_commands_leave_all_state_unchanged(self):
        for command in ("banana", "", "   ", "0", "8", "1.0", None):
            with self.subTest(command=command):
                before = deepcopy(self.player)
                self.assertIn("Invalid choice", apply_action(self.player, command))
                self.assertEqual(self.player, before)

    def test_t3_legal_move_changes_location_and_costs_exactly_one_energy(self):
        apply_action(self.player, "forward")
        self.assertEqual(self.player["location"], "Jungle")
        self.assertEqual(self.player["energy"], 4)
        self.assertFalse(self.player["game_over"])

    def test_t4_wrong_direction_and_nonadjacent_moves_have_no_cost(self):
        for command in ("back", "move cave", "move lighthouse", "move ocean"):
            with self.subTest(command=command):
                before = deepcopy(self.player)
                apply_action(self.player, command)
                self.assertEqual(self.player, before)

    def test_t5_rope_is_collected_once_without_energy_cost(self):
        self.play("forward", "take rope")
        before = deepcopy(self.player)
        self.assertEqual(self.player["inventory"], ["rope"])
        self.assertEqual(self.player["energy"], 4)
        self.assertIn("already collected", apply_action(self.player, "take"))
        self.assertEqual(self.player, before)

    def test_lantern_is_collected_once(self):
        self.play("forward", "forward", "take lantern")
        before = deepcopy(self.player)
        apply_action(self.player, "take lantern")
        self.assertEqual(self.player["inventory"], ["lantern"])
        self.assertEqual(self.player, before)

    def test_t6_bridge_is_blocked_without_rope(self):
        self.play("forward", "forward", "forward")
        before = deepcopy(self.player)
        self.assertIn("need rope", apply_action(self.player, "forward"))
        self.assertEqual(self.player, before)

    def test_t7_lighthouse_cannot_be_lit_without_lantern(self):
        self.play("forward", "take", "forward", "forward", "forward")
        before = deepcopy(self.player)
        self.assertIn("need a lantern", apply_action(self.player, "light"))
        self.assertEqual(self.player, before)
        self.assertFalse(is_win(self.player))

    def test_t8_complete_winning_path_has_required_items_and_one_energy(self):
        self.play("forward", "take rope", "forward", "take lantern",
                  "forward", "forward", "light")
        self.assertEqual(self.player["location"], "Lighthouse")
        self.assertEqual(self.player["inventory"], ["rope", "lantern"])
        self.assertEqual(self.player["energy"], 1)
        self.assertTrue(is_win(self.player))
        self.assertTrue(self.player["game_over"])

    def test_t9_fifth_legal_move_causes_loss_at_zero(self):
        self.play("forward", "back", "forward", "back", "forward")
        self.assertEqual(self.player["energy"], 0)
        self.assertEqual(self.player["location"], "Jungle")
        self.assertTrue(self.player["game_over"])
        self.assertFalse(is_win(self.player))

    def test_t10_replay_resets_state_and_creates_a_separate_inventory(self):
        self.play("forward", "take", "forward", "take", "forward", "forward", "light")
        replay = new_game(self.player["name"])
        self.assertEqual(replay["location"], "Beach")
        self.assertEqual(replay["energy"], 5)
        self.assertEqual(replay["inventory"], [])
        self.assertFalse(replay["game_over"])
        self.assertFalse(replay["won"])
        self.assertIsNot(replay["inventory"], self.player["inventory"])
        replay["inventory"].append("map")
        self.assertEqual(self.player["inventory"], ["rope", "lantern"])

    def test_invalid_action_with_inventory_does_not_mutate_the_list(self):
        self.play("forward", "take")
        before = deepcopy(self.player)
        apply_action(self.player, "banana")
        self.assertEqual(self.player, before)

    def test_checks_do_not_change_player_state(self):
        self.play("forward", "take")
        before = deepcopy(self.player)
        self.assertIn("rope", apply_action(self.player, "inventory"))
        self.assertIn("4", apply_action(self.player, "energy"))
        self.assertEqual(self.player, before)

    def test_wrong_object_and_unavailable_pickup_do_not_change_state(self):
        before = deepcopy(self.player)
        apply_action(self.player, "take rope")
        self.assertEqual(self.player, before)
        self.play("forward")
        before = deepcopy(self.player)
        apply_action(self.player, "take lantern")
        self.assertEqual(self.player, before)

    def test_cannot_win_away_from_lighthouse_even_with_both_items(self):
        self.play("forward", "take", "forward", "take")
        before = deepcopy(self.player)
        apply_action(self.player, "light")
        self.assertEqual(self.player, before)
        self.assertFalse(is_win(self.player))

    def test_lighthouse_also_requires_rope(self):
        self.player["location"] = "Lighthouse"
        self.player["inventory"] = ["lantern"]
        before = deepcopy(self.player)
        self.assertIn("need rope", apply_action(self.player, "light"))
        self.assertEqual(self.player, before)

    def test_final_energy_move_to_lighthouse_loses_before_lighting(self):
        self.play("forward", "take", "forward", "take", "forward")
        self.player["energy"] = 1
        self.play("forward")
        self.assertEqual(self.player["location"], "Lighthouse")
        self.assertEqual(self.player["energy"], 0)
        self.assertTrue(self.player["game_over"])
        before = deepcopy(self.player)
        apply_action(self.player, "light")
        self.assertEqual(self.player, before)
        self.assertFalse(is_win(self.player))

    def test_ended_games_reject_all_actions_without_mutation(self):
        for ending in ("win", "lose", "quit"):
            with self.subTest(ending=ending):
                self.player = new_game("Ada")
                if ending == "win":
                    self.play("forward", "take", "forward", "take", "forward", "forward", "light")
                elif ending == "lose":
                    self.play("forward", "back", "forward", "back", "forward")
                else:
                    self.play("quit")
                before = deepcopy(self.player)
                for action in ("forward", "back", "take", "light", "quit"):
                    apply_action(self.player, action)
                    self.assertEqual(self.player, before)
                move_player(self.player, "Cave")
                pick_up_item(self.player)
                light_beacon(self.player)
                self.assertEqual(self.player, before)
                self.assertEqual(available_actions(self.player), [])

    def test_whitespace_case_and_numbered_commands(self):
        self.play(" NORTH ", " 3 ", " MOVE CAVE ", " TAKE LANTERN ")
        self.assertEqual(self.player["location"], "Cave")
        self.assertEqual(self.player["energy"], 3)
        self.assertEqual(self.player["inventory"], ["rope", "lantern"])

    def test_exit_with_spaces_and_capitals_quits_without_energy_cost(self):
        apply_action(self.player, " EXIT ")
        self.assertTrue(self.player["game_over"])
        self.assertFalse(is_win(self.player))
        self.assertEqual(self.player["energy"], 5)

    def test_bridge_predicate_returns_a_boolean_without_mutating_inventory(self):
        inventory = ["lantern"]
        self.assertFalse(can_cross_bridge(inventory))
        inventory.append("rope")
        self.assertTrue(can_cross_bridge(inventory))
        self.assertEqual(inventory, ["lantern", "rope"])

    def test_available_actions_follow_location_and_pickup_state(self):
        self.assertEqual(available_actions(self.player), ["forward", "inventory", "energy", "quit"])
        self.play("forward")
        self.assertIn("back", available_actions(self.player))
        self.assertIn("take", available_actions(self.player))
        self.play("take")
        self.assertNotIn("take", available_actions(self.player))

    def test_blank_name_uses_a_friendly_default(self):
        self.assertEqual(new_game("   ")["name"], "Explorer")


if __name__ == "__main__":
    unittest.main()
