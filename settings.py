class Settings:
    """A class to store all setting for Alien Invasion."""

    def __init__(self) -> None:
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width = 1024
        self.screen_height = 800
        self.bg_color = (51, 102, 255)

        # Ship settings
        self.ship_speed = 5.0

        # Bullet settings
        self.bullet_speed = 10.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 8