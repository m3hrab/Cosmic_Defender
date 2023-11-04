import pygame 
from pygame.sprite import Sprite 

class Enemy(Sprite):
    """A class to represent single enemyship in the fleet"""

    def __init__(self, settings, screen) -> None:
        super().__init__() # initialize the parent class 
        self.screen = screen 
        self.settings = settings 

        # Load the enemy ship image and set it's rect attribute 
        self.image = pygame.image.load("assets/enemyship.png")
        self.rect = self.image.get_rect()

        # Start each new enemyship near the top left to the screen 
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height 

        # Store the each enemyship's exact position 
        self.x = float(self.rect.x)

    def check_edges(self):
        """Return True if enemy is at edge of the screen."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True 
        elif self.rect.left <= 0:
            return True


    def update(self):
        """Move align the right or left"""
        self.x += (self.settings.enemy_speed_factor * self.settings.fleet_direction)
        self.rect.x = self.x

    def display(self):
        """Draw the enemy ship at its current location"""
        self.screen.blit(self.image, self.rect)