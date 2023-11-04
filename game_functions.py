import sys 
import pygame
from bullet import Bullet
from enemy import Enemy
from time import sleep 
pygame.mixer.init()

# Load the sounds
shoot_sound = pygame.mixer.Sound("assets/shoot.wav")
ship_hit_sound = pygame.mixer.Sound("assets/hit.wav")
lose_sound = pygame.mixer.Sound("assets/lose.wav")  

# Load the background image 
bg = pygame.image.load("assets/bg.jpg")

def update_bullets(settings, screen, status, sb, ship, enemies, bullets):
    """Update the bullet position and delete the old bullets that disappeard from the screen"""

    #update the bullets position 
    bullets.update()

    # Delete the old bullets that already disappeard
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet) 

    # check for any bullets that have hit the enemy
    # if so, get rid of the bullet and the enemy
    check_bullet_enemy_collisions(settings, screen, status, sb, ship, enemies, bullets)

def check_bullet_enemy_collisions(settings, screen, status, sb, ship, enemies, bullets):
    """Responds to bullet-enemy collision."""
    # Remove any bullet and enemys that have collided
    collisions = pygame.sprite.groupcollide(bullets, enemies, True, True) 

    if collisions:
        ship_hit_sound.play()
        for enemies in collisions.values():
            status.score += settings.enemy_points * len(enemies)
            sb.prep_score()
        check_high_score(status, sb)

    if len(enemies) == 0:
        bullets.empty()
        settings.increase_speed()

        # Increase level   
        status.level += 1
        sb.prep_level()

        create_fleet(settings, screen, ship, enemies)

def check_high_score(status, sb):
    """Check to see if there's a new high score."""
    if status.score > status.high_score:
        status.high_score = status.score
        sb.prep_high_score()


def fire_bullet(settings, screen, ship, bullets):
    """Fire a bulllet if limit not raeched yet."""
    # Crate a new bullet and add it to the bullets group
    if len(bullets) < settings.bullet_allowed:
        new_bullet = Bullet(settings, screen, ship)
        bullets.add(new_bullet)


def check_keydown_events(event, settings, screen, ship, bullets):
    """Respond to keydown events"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True 
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True 
    elif event.key == pygame.K_SPACE:
        shoot_sound.play()
        fire_bullet(settings, screen, ship, bullets)


    elif event.key == pygame.K_q:
        sys.exit()

def check_keyup_events(event, ship):
    """Respond to keyup events"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False 

def check_events(settings, screen, status, sb, play_button, ship, enemies, bullets):
    """ Responds to keypresses and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos() 
            check_play_button(settings, screen, status, sb, play_button, ship, enemies,
                    bullets, mouse_x, mouse_y)              
            

def check_play_button(settings, screen, status, sb, play_button, ship, enemies, bullets,
        mouse_x, mouse_y):
    """Start a new game when the player clicks Play."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not status.game_active:
        # Reset the game settings
        settings.initialize_dynamic_settings()

        # Hide the mouse cursor
        pygame.mouse.set_visible(False)

        # Reset the game statistics
        status.reset_status()
        status.game_active = True

        # Reset the scoreboard images
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # Empty the list of enemies and bullets
        enemies.empty()
        bullets.empty()

        # Create a new fleet and center the ship
        create_fleet(settings, screen, ship, enemies)
        ship.center_ship()
        

def get_number_rows(settings, ship_hight, enemy_height):
    """Determine the number of row of enemy that fit on the screen"""
    available_space_y = (settings.screen_height - 
                            (6 * enemy_height) - ship_hight)
    
    number_rows = int(available_space_y / (2 * enemy_height))

    return number_rows


def get_number_enemy_x(settings, enemyship_width):
    """Determine the number of enemy that fit in a row."""
    avail_sapce_x = settings.screen_width - 2 * enemyship_width
    number_enemies_x = int(avail_sapce_x / (2 * enemyship_width))
    return number_enemies_x


def create_enemy(settings, screen, enemies, enemy_number, row_number):
    """Create an enmey and place it in the row"""
    enemy = Enemy(settings, screen)
    enemyship_width = enemy.rect.width 
    enemy.x = enemyship_width + 2 * enemyship_width * enemy_number 
    enemy.rect.x = enemy.x 
    enemy.rect.y = 10 + enemy.rect.height + 2 * enemy.rect.height * row_number 
    enemies.add(enemy)

def create_fleet(settings, screen, ship, enemies):
    """Create a full fleet of enemies"""

    # create an enemy and find the number of enemies in a row
    # Spacing between each enemy is eqal to one enemy ship
    enemy = Enemy(settings, screen)
    number_enemy_x = get_number_enemy_x(settings, enemy.rect.width)
    number_rows = get_number_rows(settings, ship.rect.height,
                    enemy.rect.height)


    # Create the fleet of enemies
    for row_number in range(number_rows):
        for enemy_number in range(number_enemy_x):
            create_enemy(settings, screen, enemies, enemy_number, row_number)


def check_fleet_edges(settings, enemies):
    """Responds appropriately if any enemies have reached an edge"""
    for enemy in enemies.sprites():
        if enemy.check_edges():
            change_fleet_direction(settings, enemies)
            break

def change_fleet_direction(settings, enemies):
    """Drop the entire fleet and change the fleet direction."""
    for enemy in enemies.sprites():
        enemy.rect.y += settings.fleet_drop_speed 
    settings.fleet_direction *= -1

def check_enemies_bottom(settings, status, sb, screen, ship, enemies, bullets):
    """Check if any enemies have reached the bottom of the screen."""
    screen_rect = screen.get_rect()
    for enemy in enemies.sprites():
        if enemy.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship got hit.
            lose_sound.play()
            ship_hit(settings, status, sb, screen, ship, enemies, bullets)
            break

def ship_hit(settings, status, sb, screen, ship, enemies, bullets):
    """Respond to ship being hit by enemies."""
    if status.ship_left > 0:
        # Decrement ship left
        status.ship_left -= 1

        # Update scoreboard
        sb.prep_ships()

        # Empty the list of eenemies and bullets
        enemies.empty()
        bullets.empty()


        # Create a new fleet and center the ship 
        create_fleet(settings, screen, ship, enemies)
        ship.center_ship()

        # Pause
        sleep(0.5)
    else:
        status.game_active = False
        pygame.mouse.set_visible(True)



def update_enemies(settings, status, sb, screen, ship, enemies, bullets):
    """
    check if the fleet is in the edge,
        and then update the positions of all alliens int he fleet
    """
    check_fleet_edges(settings, enemies)
    enemies.update() 

    # Look for enemy-playership collisions.
    if pygame.sprite.spritecollideany(ship, enemies):
        lose_sound.play()
        ship_hit(settings, status, sb, screen, ship, enemies, bullets)

    # Look for enemies hitting the bottom of the screen.
    check_enemies_bottom(settings, status, sb, screen, ship, enemies, bullets)



def update_screen(screen, stars, sb, ship, enemies, bullets, play_button, status):
    """Updae images on the screen and flip to the next screen"""
    # Redraw the screen during each pass through the loop 
    screen.blit(bg, (0,0))
    stars.draw()
    ship.draw()
    enemies.draw(screen)
    # Redraw all the bullets behind the ship and enemys 
    for bullet in bullets.sprites():
        bullet.draw() 


    # Draw the score information
    sb.show_score()
    # Draw the play button if the game is inactive
        # Draw the play button if the game is inactive
    if not status.game_active:
        play_button.draw_button() 

    # Make the most recently drawn screen visible
    pygame.display.flip()