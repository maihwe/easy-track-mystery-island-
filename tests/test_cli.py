"""Check complete terminal sessions using real standard input and output."""

import subprocess
import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class CliTests(unittest.TestCase):
    def run_session(self, *answers):
        result = subprocess.run(
            [sys.executable, "main.py"], cwd=PROJECT_ROOT,
            input="\n".join(answers) + "\n", capture_output=True, text=True,
            timeout=5,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        return result.stdout

    def test_numbered_winning_path(self):
        output = self.run_session("Ada", "1", "3", "1", "3", "1", "1", "6", "n")
        self.assertIn("You escaped Mystery Island! You won the game!", output)
        self.assertIn("Play again?", output)
        self.assertIn("Energy: 1", output)

    def test_losing_path_stops_at_zero_and_offers_replay(self):
        output = self.run_session("Ada", "1", "2", "1", "2", "1", "n")
        self.assertIn("You ran out of energy. Game over!", output)
        self.assertIn("Play again?", output)
        self.assertNotIn("You won the game!", output)

    def test_invalid_commands_recover_and_normalized_exit_quits(self):
        output = self.run_session("Ada", "", "banana", " 5 ", " EXIT ", "n")
        self.assertEqual(output.count("Invalid choice."), 2)
        self.assertIn("Your current energy: 5", output)
        self.assertIn("You quit the game.", output)

    def test_replay_after_each_outcome_starts_fresh(self):
        paths = {
            "win": ["1", "3", "1", "3", "1", "1", "6"],
            "lose": ["1", "2", "1", "2", "1"],
            "quit": ["1", "3", "7"],
        }
        for ending, path in paths.items():
            with self.subTest(ending=ending):
                output = self.run_session("Ada", *path, " Y ", "4", "7", "n")
                self.assertEqual(output.count("Welcome to Mystery Island, Ada!"), 2)
                replay = output.split("Welcome to Mystery Island, Ada!")[-1]
                self.assertIn("===== BEACH =====", replay)
                self.assertIn("Energy: 5", replay)
                self.assertIn("Inventory: empty", replay)

    def test_invalid_replay_choice_retries(self):
        output = self.run_session("Ada", "7", "banana", " NO ")
        self.assertIn("Please enter y or n.", output)
        self.assertEqual(output.count("Play again?"), 2)
        self.assertIn("Thanks for playing!", output)

    def test_end_of_input_during_game_exits_without_traceback(self):
        output = self.run_session("Ada")
        self.assertIn("You quit the game.", output)
        self.assertIn("Thanks for playing!", output)

    def test_importing_main_does_not_start_interactive_game(self):
        result = subprocess.run(
            [sys.executable, "-c", "import main"], cwd=PROJECT_ROOT,
            input="", capture_output=True, text=True, timeout=5,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "")
        self.assertEqual(result.stderr, "")


if __name__ == "__main__":
    unittest.main()
