class Settings:
    """A class to store all setting for Alien Invasion."""

    def __init__(self) -> None:
        """Initialize the game's static settings."""
        # Alien settings
        self.alien_speed = 1
        self.fleet_direction = 1
        self.fleet_drop_speed = 10

        # Bullet settings
        self.bullets_allowed = 3
        self.bullet_color = (57, 255, 20)
        self.bullet_height = 15
        self.bullet_speed = 10.0
        self.bullet_width = 5

        # How quickly the game speeds up
        self.speedup_scale = 1.1

        # Scaling of score as rounds continue
        self.score_scale = 1.5

        # Screen settings
        self.bg_color = (0, 0, 0)
        self.screen_height = 800
        self.screen_width = 1024

        # Scoring settings
        self.alien_points = 50

        # Ship settings
        self.ship_limit = 3
        self.ship_speed = 5.0

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize setings that change throughout the game."""
        self.ship_speed = 1.5
        self.bullet_speed = 10.0
        self.alien_speed = 1
        self.fleet_direction = 1

    def increase_speed(self):
        """Increase speed settings."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
