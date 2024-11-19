import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 20  # Slow down the simulation for observation
GRAVITY = 0.5  # Gravity constant
ANGLE = 75  # Angle in degrees
INITIAL_VELOCITY = 15  # Initial velocity

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)  # Color for Ball B
GREEN = (0, 255, 0)  # Color for Ball C
BLACK = (0, 0, 0)

# Ball settings
ball_radius = 20
ball_y_start = HEIGHT // 2  # Starting y-position for the ball

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Juggling Physics Engine")


# Ball class
class Ball:
    def __init__(self, x, y, velocity_x, velocity_y, color):
        self.x = x
        self.y = y
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.wait_time = 0  # Time remaining for the wait period after a bounce
        self.color = color  # Set the ball's color

    def update(self):
        if self.wait_time > 0:
            self.wait_time -= 1  # Decrease wait time if it's active
            return  # Skip the update if the ball is waiting

        # Apply gravity
        self.velocity_y += GRAVITY
        # Update position
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Check if the ball has hit the ground (starting y-value)
        if self.y >= ball_y_start and self.velocity_y > 0:
            self.y = ball_y_start  # Reset the ball's position to the starting height
            self.velocity_y = -self.velocity_y  # Reverse vertical velocity (elastic bounce)
            self.velocity_x = -self.velocity_x  # Reverse horizontal velocity (elastic bounce)

            # Commented out the print statement
            # print(f"Ball landed at x = {self.x}")  # Ball landing x-coordinate

            if self.wait_time == 0:  # If it's the first bounce
                self.wait_time = 180  # Start 3 seconds wait time after bounce

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), ball_radius)


# Game loop
clock = pygame.time.Clock()

# Create the first ball (A)
ball_a = Ball(300, ball_y_start, INITIAL_VELOCITY * math.cos(math.radians(ANGLE)),
              -INITIAL_VELOCITY * math.sin(math.radians(ANGLE)), RED)

# Create the second ball (B) at the landing position of ball A (x = 521.2902835626563), color blue
ball_b = Ball(521.2902835626563, ball_y_start, 0, 0, BLUE)

# Create the third ball (C) at the starting position of ball A (x = 300), color green
# Launch Ball C to the right initially (opposite direction from A in cascade)
ball_c = Ball(300, ball_y_start, INITIAL_VELOCITY * math.cos(math.radians(ANGLE)),
              -INITIAL_VELOCITY * math.sin(math.radians(ANGLE)), GREEN)

# Variable to track if Ball B has been launched
ball_b_launched = False

# Variable to track if Ball C has been launched
ball_c_launched = False


# Track the previous velocity_y for Ball A to detect the change in direction
previous_velocity_y_a = ball_a.velocity_y

# Track the previous velocity_y for Ball B to detect the change in direction
previous_velocity_y_b = ball_b.velocity_y

while True:
    screen.fill(WHITE)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Update the ball positions
    ball_a.update()

    # Print Ball A's vertical velocity for debugging
    print(f"Ball A velocity_y: {ball_a.velocity_y}")

    # Check if Ball A has reached its maximum height (negative velocity to positive velocity)
    if previous_velocity_y_a < 0 and ball_a.velocity_y >= 0 and not ball_b_launched:
        # Ball A has reached the maximum height
        ball_b.velocity_x = -INITIAL_VELOCITY * math.cos(math.radians(ANGLE))  # Throw left
        ball_b.velocity_y = -INITIAL_VELOCITY * math.sin(math.radians(ANGLE))  # Throw up
        ball_b_launched = True  # Ensure Ball B is only launched once

    # Update Ball B's movement if it has been launched
    if ball_b_launched:
        ball_b.update()

    # Check if Ball B has reached its maximum height (negative velocity to positive velocity)
    if previous_velocity_y_b < 0 and ball_b.velocity_y >= 0 and not ball_c_launched:
        # Ball B has reached the maximum height
        ball_c.velocity_x = INITIAL_VELOCITY * math.cos(math.radians(ANGLE))  # Throw right
        ball_c.velocity_y = -INITIAL_VELOCITY * math.sin(math.radians(ANGLE))  # Throw up
        ball_c_launched = True  # Ensure Ball C is only launched once

    # Update Ball C's movement if it has been launched
    if ball_c_launched:
        ball_c.update()

    # Draw the horizontal line at the starting y-value
    pygame.draw.line(screen, BLACK, (0, ball_y_start), (WIDTH, ball_y_start), 2)

    # Draw all three balls
    ball_a.draw(screen)
    ball_b.draw(screen)  # Ball B is blue and moving now
    ball_c.draw(screen)  # Ball C is green and moving right away

    # Update the previous_velocity_y for the next frame
    previous_velocity_y_a = ball_a.velocity_y
    previous_velocity_y_b = ball_b.velocity_y

    # Update the screen
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)
