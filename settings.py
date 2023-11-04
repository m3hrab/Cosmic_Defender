class Settings():
    """A class to store all the settings"""

    def __init__(self):
        """Initialize the game's settings"""

        # Screen Settings 
        self.screen_width = 800
        self.screen_height = 600
        self.bg_color =  (20, 33, 61)

        # Background stars settings 
        self.total_stars = 80
        self.min_scroll_speed = 0.08
        self.max_scroll_speed = 0.123


        # ship settings 
        self.ship_speed_factor = 1
        self.ship_limit = 3

        # Bullet Settings 
        self.bullet_speed_factor = 1.5
        self.bullet_width = 3
        self.bullet_height = 6 
        self.bullet_allowed = 20
        self.bullet_color =  (0, 204, 255) #(72, 202, 228) 

        # Enemy Settings 
        self.enemy_speed_factor = .8
        self.fleet_drop_speed = 5
        self.fleet_direction = 1

        # How quickly the game speeds up
        self.speedup_scale = 1.2

        # How quickly the enemy point values increase
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game"""
        self.ship_speed_factor = 1
        self.bullet_speed_factor = 1.5
        self.enemy_speed_factor = .8 

        # fleet_direction 1 represent right, -1 represent left
        self.fleet_direction = 1
        # Scoring 
        self.enemy_points = 50

    def increase_speed(self):
        """Increase speed settings and enemy point values"""
        self.ship_speed_factor *= self.speedup_scale 
        self.bullet_speed_factor *= self.speedup_scale 
        self.enemy_speed_factor *= self.speedup_scale 
        self.enemy_points = int(self.enemy_points * self.score_scale)