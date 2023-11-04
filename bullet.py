import pygame 
from pygame.sprite import Sprite 

class Bullet(Sprite):
    """A class to manage bullets fired from the ship"""

    def __init__(self, settings, screen, ship):
        super().__init__()
        self.screen = screen 

        # Create a bullet rect and set it's position 
        self.rect = pygame.Rect(0,0, settings.bullet_width,
            settings.bullet_height)
        self.rect.centerx = ship.rect.centerx - 2
        self.rect.top = ship.rect.top - 2

        # Store the bullet's position as a decimal value 
        self.y = float(self.rect.y) 

        self.color = settings.bullet_color 
        self.speed_factor = settings.bullet_speed_factor 

    
    def update(self):
        """ Move the bullet up the screen"""
        self.y -= self.speed_factor # update the decimal position of the bullet
        # update the rect position 
        self.rect.y = self.y 

    def draw(self):
        """Draw the bullet to the screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)