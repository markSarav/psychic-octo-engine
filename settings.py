class Settings:
    """A class to store all setting for Alien Invasion."""

    def __init__(self) -> None:
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (51, 102, 255)

        # Ship settings
        self.ship_speed = 1.5
        
