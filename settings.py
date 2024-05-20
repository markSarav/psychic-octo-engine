class Settings:
    """A class to store all setting for Alien Invasion."""

    def __init__(self) -> None:
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width = 1024
        self.screen_height = 800
        self.bg_color = (0, 0, 0)

        # Ship settings
        self.ship_speed = 5.0

        # Bullet settings
        self.bullet_speed = 10.0
        self.bullet_width = 5
        self.bullet_height = 15
        self.bullet_color = (57, 255, 20)
        self.bullets_allowed = 8