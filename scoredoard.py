import pygame.font
from pygame.sprite import Group


class Life(pygame.sprite.Sprite):
    def __init__(self, screen, settings):
        super().__init__()
        self.screen = screen
        self.settings = settings
        # Load the heart image and get its rect.
        self.image = pygame.image.load('assets/heart.png')
        self.rect = self.image.get_rect()

    def draw(self):
        """Draw the heart at its current location"""
        self.screen.blit(self.image, self.rect)
        
class Scoreboard():
    """A class to report scoring information"""
    
    def __init__(self, settings, screen, status):
        """Initialize scorekeeping attributes"""
        self.screen = screen 
        self.screen_rect = screen.get_rect()
        self.settings = settings
        self.status = status 

        # Font settings for scoring information 
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont("comicsansms", 24)

        # Prepare the initial score image 
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        """Turn the score into a rendered image"""
        score_str = "Score: " + str(self.status.score)
        self.score_image = self.font.render(score_str, True, self.text_color)

        # Display the score at the top right of the screen 
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20 
        self.score_rect.top = 20

    def prep_high_score(self):
        """Turn the high score into a rendered image"""
        high_score_str = str(self.status.high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color)

        # Center the high score at the top of the screen 
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx 
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        """Turn the level into a rendered image"""
        level_str = "Level:" + str(self.status.level)
        self.level_image = self.font.render(level_str, True, self.text_color)

        # Position the level below the score 
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right 
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        """Show how many ships are left"""
        self.ships = Group()
        for ship_number in range(self.status.ship_left):
            ship = Life(self.screen, self.settings)
            ship.rect.x = 5 + ship_number * ship.rect.width 
            ship.rect.y = 5 
            self.ships.add(ship)
    
    def show_score(self):
        """Draw scores, level, and ships to the screen"""
        self.screen.blit(self.score_image, self.score_rect) 
        self.screen.blit(self.high_score_image, self.high_score_rect) 
        self.screen.blit(self.level_image, self.level_rect) 
        self.ships.draw(self.screen)