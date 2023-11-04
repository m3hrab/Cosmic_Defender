class GameStats():
    """Track statistics for Cosmic Defenders"""

    def __init__(self, settings):
        """Initialize statistics"""
        self.settings = settings 
        self.reset_status() 

        # Start game in an inactive state
        self.game_active = False

    def reset_status(self):
        """Initialize statistic taht can change during the game."""
        self.ship_left = self.settings.ship_limit 
        self.score = 0
        self.level = 1
        self.high_score = 0
        