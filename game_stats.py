import json
from pathlib import Path


class GameStats:
    """Track statistics for Alien Invasion."""

    def __init__(self, ai_game) -> None:
        """Initialize statistics."""
        self.settings = ai_game.settings
        self.reset_stats()
        self.high_score = 0
        self.create_high_scores_file()

    def check_highscore_beaten(self):
        """Returns True if highscore has been beaten."""
        return self.high_score < self.score

    def create_high_scores_file(self):
        """Creates json dump file for highscores."""
        path = Path("highscore.json")
        if path.exists():
            print("found highscores, loading latest one")
            self.load_latest_highscore()
        else:
            print("no highscore found, making new highscore file")
            self.high_score = self.score
            contents = json.dumps(self.high_score)
            path.write_text(contents)

    def load_latest_highscore(self):
        """Load the latest highscore."""
        path = Path("highscore.json")
        contents = path.read_text()
        high_score = json.loads(contents)
        self.high_score = int(high_score)

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
