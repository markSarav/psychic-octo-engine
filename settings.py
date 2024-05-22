class Settings:
    """A class to store all setting for Alien Invasion."""

    def __init__(self) -> None:
        """Initialize the game's settings."""
        # Alien settings
        self.alien_speed = 1.0
        self.fleet_direction = 1
        self.fleet_drop_speed = 10

        # Bullet settings
        self.bullets_allowed = 8
        self.bullet_color = (57, 255, 20)
        self.bullet_height = 15
        self.bullet_speed = 10.0
        self.bullet_width = 5

        # Screen settings
        self.bg_color = (0, 0, 0)
        self.screen_height = 800
        self.screen_width = 1024

        # Ship settings
        self.ship_limit = 3
        self.ship_speed = 5.0