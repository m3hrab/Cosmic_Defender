import pygame
import random

class Star(pygame.sprite.Sprite):
    def __init__(self, screen, settings):
        super().__init__()
        self.screen = screen
        self.settings = settings
        self.image = pygame.Surface((1, 1), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, self.settings.screen_width)
        self.rect.y = random.randint(0, self.settings.screen_height)
        self.scroll_speed = random.uniform(self.settings.min_scroll_speed, self.settings.max_scroll_speed)
        # self.color = random.choice([(200, 0, 0), (200, 200, 0), (250, 250, 250)])
        self.color = random.choice([
            (255, 255, 255),  # White Stars
            (255, 255, 0),    # Yellow Stars
            (0, 0, 255),      # Blue Stars
            (255, 0, 0),      # Red Stars
            (255, 165, 0),    # Orange Stars
            (128, 0, 128),    # Purple Stars
            (0, 128, 0),      # Green Stars
            (255, 105, 180),  # Pink Stars
            (0, 255, 255),    # Cyan Stars
            (0, 128, 128)     # Teal Stars
        ])

        self.image.fill(self.color)
        self.temp = float(self.rect.y)

    def update(self):
        self.temp += self.scroll_speed
        if self.temp >= self.settings.screen_height:
            self.temp = 0
            self.rect.x = random.randint(0, self.settings.screen_width)
        
        self.rect.y = self.temp 


class Stars():
    def __init__(self, screen, settings):
        self.screen = screen
        self.settings = settings
        self.stars = pygame.sprite.Group()

        for _ in range(self.settings.total_stars):
            star = Star(self.screen, self.settings)
            self.stars.add(star)

    def update(self):
        self.stars.update()

    def draw(self):
        self.stars.draw(self.screen)
