import pygame
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Spaceship Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Spaceship size
spaceship_width = 50
spaceship_height = 50

# Create spaceship class
class Spaceship(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.image = pygame.Surface((spaceship_width, spaceship_height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 5

    def update(self, speed, direction):
        # Update the spaceship's position
        if direction == "left":
            self.rect.x -= speed
        elif direction == "right":
            self.rect.x += speed

        # Ensure the spaceship doesn't go off the screen
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > width:
            self.rect.right = width

# Laser class
class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, direction):
        super().__init__()
        self.image = pygame.Surface((5, 20))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = speed
        self.direction = direction  # "up" for player laser, "down" for AI laser

    def update(self):
        if self.direction == "up":
            self.rect.y -= self.speed
        elif self.direction == "down":
            self.rect.y += self.speed

# Create AI spaceship class with fuzzy logic
class AISpaceship(Spaceship):
    def __init__(self, x, y):
        super().__init__(x, y, GREEN)
        self.speed = 0
        self.fire_rate = 200  # AI fires every 200 frames (adjust this for slower firing)
        self.last_shot = 0

    def update(self, player_x, player_lasers):
        # Update AI movement using fuzzy logic and avoid player lasers
        distance = player_x - self.rect.centerx
        self.fuzzy_logic(distance)

        # Check if AI needs to dodge lasers
        self.dodge_lasers(player_lasers)

        # Move based on fuzzy logic output
        if self.speed > 0:
            self.rect.x += self.speed
        elif self.speed < 0:
            self.rect.x -= abs(self.speed)

        # Ensure the AI doesn't move off-screen
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > width:
            self.rect.right = width

    def fuzzy_logic(self, distance):
        # Define fuzzy sets for distance
        distance_input = ctrl.Antecedent(np.arange(-width // 2, width // 2, 1), 'distance')
        ai_speed_output = ctrl.Consequent(np.arange(-5, 6, 1), 'ai_speed')

        distance_input['close'] = fuzz.trimf(distance_input.universe, [-width // 2, 0, 0])
        distance_input['medium'] = fuzz.trimf(distance_input.universe, [0, 0, width // 2])
        distance_input['far'] = fuzz.trimf(distance_input.universe, [0, width // 2, width // 2])

        ai_speed_output['move_left'] = fuzz.trimf(ai_speed_output.universe, [-5, -2, 0])
        ai_speed_output['no_move'] = fuzz.trimf(ai_speed_output.universe, [-1, 0, 1])
        ai_speed_output['move_right'] = fuzz.trimf(ai_speed_output.universe, [0, 2, 5])

        # Define fuzzy rules
        rule1 = ctrl.Rule(distance_input['close'], ai_speed_output['move_left'])
        rule2 = ctrl.Rule(distance_input['medium'], ai_speed_output['no_move'])
        rule3 = ctrl.Rule(distance_input['far'], ai_speed_output['move_right'])

        # Create control system and simulation
        ai_control = ctrl.ControlSystem([rule1, rule2, rule3])
        ai_simulation = ctrl.ControlSystemSimulation(ai_control)

        # Input the distance value to the fuzzy system
        ai_simulation.input['distance'] = distance
        ai_simulation.compute()

        # Get output and set the AI's speed
        self.speed = ai_simulation.output['ai_speed']

    def dodge_lasers(self, player_lasers):
        # AI should dodge the lasers fired by the player
        for laser in player_lasers:
            # If laser is close to the AI spaceship
            if laser.rect.colliderect(self.rect):
                # AI dodges by moving in the opposite direction of the laser's position
                if laser.rect.centerx < self.rect.centerx:
                    self.rect.x += self.speed  # Move right to dodge
                else:
                    self.rect.x -= self.speed  # Move left to dodge

            # Predict laser trajectory and react based on direction
            if laser.direction == "up" and laser.rect.bottom < self.rect.top:
                # If the laser is coming down, AI should move left or right based on trajectory
                if laser.rect.centerx < self.rect.centerx:
                    self.rect.x += self.speed  # Move right to dodge
                else:
                    self.rect.x -= self.speed  # Move left to dodge

    def shoot(self):
        # AI shoots lasers at the player
        laser = Laser(self.rect.centerx, self.rect.bottom, 5, "down")
        return laser

# Create game sprites
player = Spaceship(width // 2, height - 50, WHITE)
ai_spaceship = AISpaceship(width // 2, 50)

# Group for lasers
player_lasers = pygame.sprite.Group()
ai_lasers = pygame.sprite.Group()

# Game loop
running = True
clock = pygame.time.Clock()
score = 0
game_over = False
winner = None  # "player" or "ai"

while running:
    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and not game_over:
            if event.key == pygame.K_SPACE:
                # Create a new laser when the player presses space
                laser = Laser(player.rect.centerx, player.rect.top, 7, "up")
                player_lasers.add(laser)

    if not game_over:
        # Get player input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.update(player.speed, "left")
        if keys[pygame.K_RIGHT]:
            player.update(player.speed, "right")

        # Update AI movement using fuzzy logic and dodge lasers
        ai_spaceship.update(player.rect.centerx, player_lasers)

        # AI fires lasers at regular intervals
        if pygame.time.get_ticks() - ai_spaceship.last_shot > ai_spaceship.fire_rate:
            ai_lasers.add(ai_spaceship.shoot())
            ai_spaceship.last_shot = pygame.time.get_ticks()

        # Update lasers
        player_lasers.update()
        ai_lasers.update()

        # Check for collisions between player lasers and AI spaceship
        for laser in player_lasers:
            if laser.rect.colliderect(ai_spaceship.rect):
                game_over = True
                winner = "player"

        # Check for collisions between AI lasers and player spaceship
        for laser in ai_lasers:
            if laser.rect.colliderect(player.rect):
                game_over = True
                winner = "ai"

        # Draw all sprites
        screen.blit(player.image, player.rect)
        screen.blit(ai_spaceship.image, ai_spaceship.rect)
        for laser in player_lasers:
            screen.blit(laser.image, laser.rect)
        for laser in ai_lasers:
            screen.blit(laser.image, laser.rect)

    # Show score and game over message
    if game_over:
        font = pygame.font.Font(None, 74)
        text = font.render(f"Game Over: {winner} Wins!", True, WHITE)
        screen.blit(text, (width // 2 - text.get_width() // 2, height // 2))

        restart_font = pygame.font.Font(None, 36)
        restart_text = restart_font.render("Press ENTER to restart", True, WHITE)
        screen.blit(restart_text, (width // 2 - restart_text.get_width() // 2, height // 2 + 50))

        if pygame.key.get_pressed()[pygame.K_RETURN]:
            game_over = False
            winner = None
            player.rect.centerx = width // 2
            player.rect.centery = height - 50
            ai_spaceship.rect.centerx = width // 2
            ai_spaceship.rect.centery = 50
            score = 0
            player_lasers.empty()
            ai_lasers.empty()

    pygame.display.update()
    clock.tick(60)

pygame.quit()
