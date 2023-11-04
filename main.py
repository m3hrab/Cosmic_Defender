import pygame
from pygame.sprite import Group
import game_functions as gf
from settings import Settings 
from ship import Ship
from stars import Stars
from game_status import GameStats 
from button import Button
from scoredoard import Scoreboard


def run_game():
    pygame.init()
    settings = Settings()
    screen = pygame.display.set_mode(
        (settings.screen_width, settings.screen_height))
    pygame.display.set_caption("Cosmic Defenders")

    # Create the stars 
    stars = Stars(screen, settings)
    # Creating a ship object 
    ship = Ship(screen, settings)
    # Create a group to store bullets in 
    bullets = Group()
    # Create a fleet of enemies
    enemies = Group()
    gf.create_fleet(settings, screen, ship,  enemies)

    status = GameStats(settings)
    sb = Scoreboard(settings, screen, status)
    play_button = Button(settings, screen, "Play")

    # Main game loop
    while True:

        gf.check_events(settings, screen, status, sb, play_button, ship, enemies, bullets)
        stars.update()
        if status.game_active:
            ship.update()
            gf.update_bullets(settings, screen, status, sb, ship, enemies, bullets)
            gf.update_enemies(settings, status, sb, screen, ship, enemies, bullets)
        
        gf.update_screen(screen, stars, sb, ship, enemies, bullets, play_button, status)
        
run_game()