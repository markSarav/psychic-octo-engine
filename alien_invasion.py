import sys
from random import randint
from time import sleep

import pygame

from alien import Alien
from bullet import Bullet
from button import Button
from game_stats import GameStats
from scoreboard import Scoreboard
from settings import Settings
from ship import Ship
from stars import StarBackground


class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self) -> None:
        """Initialize the game, and create game resources."""
        pygame.init()
        pygame.display.set_caption("Alien Invasion")
        self.settings = Settings()
        self.game_active = False
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        self.clock = pygame.time.Clock()

        # Make all the buttons.
        self.play_button = Button(self, "'E' to Play!")
        self.easy_mode_button = Button(self, "Easy (1)")
        self.easy_mode_button.rect.top = (
            self.play_button.rect.top + 1.5 * self.play_button.rect.height
        )
        self.easy_mode_button.update_msg()
        self.hard_mode_button = Button(self, "Hard (2)")
        self.hard_mode_button.rect.top = (
            self.easy_mode_button.rect.top + 1.5 * self.play_button.rect.height
        )
        self.hard_mode_button.update_msg()

        # Create an instance to store game stats and create a scoreboard.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        # Create all game objects.
        self.aliens = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()
        self.ship = Ship(self)
        self._create_fleet()
        self._create_star_background()

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()

            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()
            self.clock.tick(60)

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _check_aliens_bottom(self):
        """Check if any alien have reached the bottom of the screen."""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                # Treat this the same as if the ship go hit.
                self._ship_hit()
                break

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        # Remove any bullets and aliens that have collided.
        collisions = pygame.sprite.groupcollide(  # noqa: F841
            self.bullets, self.aliens, True, True
        )

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            # Destroy existing bullets and create new fleet.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

    def _check_difficulty_buttons(self, mouse_pos):
        """Check which difficulty the user selected and set the game difficulty to that."""
        button_clicked_ez = self.easy_mode_button.rect.collidepoint(mouse_pos)
        button_clicked_hd = self.hard_mode_button.rect.collidepoint(mouse_pos)
        if button_clicked_ez and not self.game_active:
            self._set_game_difficulty(1)
        elif button_clicked_hd and not self.game_active:
            self._set_game_difficulty(2)

    def _check_events(self):
        """Responds to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
                self._check_difficulty_buttons(mouse_pos)

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _check_keydown_events(self, event):
        """Respond to key presses."""
        if event.key == pygame.K_d:
            self.ship.moving_right = True
        elif event.key == pygame.K_a:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_e:
            self._start_game()
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_1:
            self._set_game_difficulty(1)
        elif event.key == pygame.K_2:
            self._set_game_difficulty(2)

    def _check_keyup_events(self, event):
        """Resond to key releases."""
        if event.key == pygame.K_d:
            self.ship.moving_right = False
        elif event.key == pygame.K_a:
            self.ship.moving_left = False

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            # Reset the game settings.
            self._start_game()

    def _create_alien(self, x_position, y_position):
        """Create an alien and place it in the row."""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _create_fleet(self):
        """Create the fleet of aliens."""
        #  Create an alien and keep adding aliens untile there's no room
        #   left. Spacing between aliens is one alien width and one
        #    alien height.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width
            # Finished a row; reset x value, and increment y value.
            current_x = alien_width
            current_y += 2 * alien_height

    def _create_star(self, x_position, y_position):
        """Creates a Star sprite used for the background."""
        new_star = StarBackground(self)
        new_star.rect.x = x_position
        new_star.rect.y = y_position
        self.stars.add(new_star)

    def _create_star_background(self):
        """Creates a grid of random stars to use as a background."""
        star = StarBackground(self)
        star_width, star_height = star.rect.size
        current_x = star_width
        current_y = star_height
        while current_y < (self.settings.screen_height - star_height):
            while current_x < (self.settings.screen_width - star_width):
                self._create_star(current_x, current_y)
                current_x += randint(star_width, star_width * star_width)
            current_x = randint(star_width, star_width * star_width)
            current_y += star_height

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < (self.settings.bullets_allowed):
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _set_game_difficulty(self, setting_choice):
        """Sets the game's difficulty when selected."""
        if setting_choice == 1:
            self._start_game()
            self.settings.alien_speed *= 0.5
        elif setting_choice == 2:
            self._start_game()
            self.settings.alien_speed *= 1.5

    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        if self.stats.ships_left > 0:
            # Decrement ships_left.
            self.stats.ships_left -= 1
            # Get rid of any remaining bullets and aliens.
            self.bullets.empty()
            self.aliens.empty()
            # Create a new feet and center the ship.
            self._create_fleet()
            self.ship.center_ship()
            # Pause.
            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)

    def _start_game(self):
        """Respond to when user presses 'e' to start game."""
        if not self.game_active:
            self.stats.reset_stats()
            self.sb.prep_score()
            self.bullets.empty()
            self.aliens.empty()
            self._create_fleet()
            self.ship.center_ship()
            self.game_active = True
            pygame.mouse.set_visible(False)
            self.settings.initialize_dynamic_settings()

    def _update_aliens(self):
        """Update the positions of all aliens in the fleet."""
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Look for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions
        self.bullets.update()
        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        self.stars.draw(self.screen)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        self.ship.blitme()

        # Draw the score information.
        self.sb.show_score()
        # Draw the play button if the game is inactive.
        if not self.game_active:
            self.play_button.draw_button()
            self.easy_mode_button.draw_button()
            self.hard_mode_button.draw_button()

        pygame.display.flip()


if __name__ == "__main__":
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
