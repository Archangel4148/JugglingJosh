import math
import sys

import pygame

from juggling_tools import Ball, JugglingEnvironment

# ================  Constants (You can change these)  ================

# Pygame settings
SCREEN_WIDTH = 800  # in pixels
SCREEN_HEIGHT = 600  # in pixels
FPS = 60

# Juggling settings
USE_DISTANCE_AND_MAX_HEIGHT = True
ANGLE = 75  # Throw angle in degrees
THROW_VELOCITY = 5  # Velocity in m/s
HAND_DISTANCE = 0.4  # Distance between hands in meters
MAX_HEIGHT = 0.76  # Max height of throw in meters

# Ball settings
NUMBER_OF_BALLS = 3
BALL_RADIUS = 0.06  # in meters
USE_PASTEL_COLORS = False

if USE_PASTEL_COLORS:
    # Pastel colors
    BALL_COLORS = [
        (135, 206, 250),  # Light Sky Blue
        (255, 182, 193),  # Light Pink
        (144, 238, 144),  # Light Green
        (255, 250, 205),  # Lemon Chiffon
        (221, 160, 221),  # Plum
    ]
else:
    # Default colors
    BALL_COLORS = [
        (255, 0, 0),  # Red
        (0, 0, 255),  # Blue
        (0, 255, 0),  # Green
        (255, 255, 0),  # Yellow
        (255, 0, 255),  # Magenta
    ]

# Cosmetic settings
DRAW_CATCH_LINE = False
DRAW_HAND_MARKERS = True


# ====================================================================

def compute_throw_range(environment: JugglingEnvironment, velocity: float, angle: float) -> float:
    # Compute horizontal range in meters
    range_meters = (velocity ** 2) * math.sin(math.radians(2 * angle)) / environment.gravity

    # Convert to pixels
    return range_meters * environment.scaling_factor


def draw_background(main_screen: pygame.Surface, environment: JugglingEnvironment, marker_length: int):
    # Light pastel background
    main_screen.fill((240, 248, 255))  # Alice Blue
    floor_color = (150, 150, 150)  # Subtle gray for floor line
    marker_color = (50, 50, 150)  # Dark blue for hands

    # Draw "catch" line
    if DRAW_CATCH_LINE:
        pygame.draw.line(main_screen, floor_color, (0, environment.floor_y),
                         (environment.width_pix, environment.floor_y), 2)

    # Draw hand markers
    if DRAW_HAND_MARKERS:
        pygame.draw.line(main_screen, marker_color, (environment.left_hand_x, environment.floor_y),
                         (environment.left_hand_x, environment.floor_y + marker_length), 5)
        pygame.draw.line(main_screen, marker_color, (environment.right_hand_x, environment.floor_y),
                         (environment.right_hand_x, environment.floor_y + marker_length), 5)


def draw_reset_button(main_screen: pygame.Surface, environment: JugglingEnvironment, mouse_x: int, mouse_y: int):
    button_width = 150
    button_height = 50
    button_color = (240, 128, 128)  # Light Coral
    button_hover_color = (255, 160, 160)  # Lighter Coral for hover effect
    button_pressed_color = (200, 100, 100)  # Darker Coral for click effect
    shadow_color = (200, 100, 100)
    text_color = (255, 255, 255)
    button_x = environment.width_pix - button_width - 20
    button_y = 20

    # Check if the mouse is hovering over the button
    is_hovered = button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height

    # Check if the mouse click is within the button
    is_clicked = False
    if is_hovered and pygame.mouse.get_pressed()[0]:
        is_clicked = True

    # Use a different button color depending on hover and click state
    current_button_color = button_pressed_color if is_clicked else (button_hover_color if is_hovered else button_color)

    # Draw shadow
    pygame.draw.rect(main_screen, shadow_color, (button_x + 3, button_y + 3, button_width, button_height),
                     border_radius=10)

    # Draw rounded button with hover and click effects
    pygame.draw.rect(main_screen, current_button_color, (button_x, button_y, button_width, button_height),
                     border_radius=10)

    # Draw text
    font = pygame.font.SysFont("Arial", 28, bold=True)
    text = font.render("Reset", True, text_color)
    text_rect = text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
    main_screen.blit(text, text_rect)

    return button_x, button_y, button_width, button_height, is_clicked


def main():
    # Initialize Pygame
    pygame.init()

    # Set up the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Juggling Physics Engine")

    # Create physics environment
    environment = JugglingEnvironment(
        width_pix=screen.get_width(),
        height_pix=screen.get_height(),
        gravity=9.8,
        floor_y=screen.get_height() // 2,
        ceiling_y=0,
        scaling_factor=200,
        left_hand_x=None,
        right_hand_x=None,
        use_distance_and_max_height=USE_DISTANCE_AND_MAX_HEIGHT,
    )

    # Calculate throw range
    if not USE_DISTANCE_AND_MAX_HEIGHT:
        throw_range = compute_throw_range(environment, THROW_VELOCITY, ANGLE)
    else:
        throw_range = HAND_DISTANCE * environment.scaling_factor

    print(f"Throw range: {throw_range / environment.scaling_factor:.2f} m")

    # Find left and right hand positions to match throw range
    environment.left_hand_x = environment.width_pix // 2 - throw_range // 2
    environment.right_hand_x = environment.width_pix // 2 + throw_range // 2

    def create_balls():
        """Helper function to create a new list of balls."""
        new_balls = []
        for j in range(NUMBER_OF_BALLS):
            x = environment.left_hand_x if j % 2 == 0 else environment.right_hand_x
            color = BALL_COLORS[j % len(BALL_COLORS)]
            name = chr(ord('A') + j)
            new_balls.append(Ball(environment, x, environment.floor_y, BALL_RADIUS, color, name))
        return new_balls

    # Initialize balls and start the first throw
    balls = create_balls()
    balls[0].throw(velocity=THROW_VELOCITY, angle=ANGLE, distance=HAND_DISTANCE, max_height=MAX_HEIGHT)

    clock = pygame.time.Clock()

    # Main game loop
    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Handle clicks for the reset button
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                button_x, button_y, button_width, button_height, _ = draw_reset_button(screen, environment, mouse_x,
                                                                                       mouse_y)
                if (button_x <= mouse_x <= button_x + button_width) and (
                        button_y <= mouse_y <= button_y + button_height):
                    balls = create_balls()  # Recreate the balls
                    balls[0].throw(velocity=THROW_VELOCITY, angle=ANGLE, distance=HAND_DISTANCE, max_height=MAX_HEIGHT)

        # Cap the frame rate
        clock.tick(FPS)

        # Calculate delta time
        dt = clock.get_time() / 1000

        # Check if a throw is needed
        for i, ball in enumerate(balls):
            if ball.detect_apex():
                next_ball = balls[(i + 1) % len(balls)]
                next_ball.throw(velocity=THROW_VELOCITY, angle=ANGLE, distance=HAND_DISTANCE, max_height=MAX_HEIGHT)

        # Update ball positions
        for ball in balls:
            ball.update(dt)

        # Draw full scene
        draw_background(screen, environment, 30)
        for ball in balls:
            ball.draw(screen)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        draw_reset_button(screen, environment, mouse_x, mouse_y)

        # Update the screen
        pygame.display.flip()


if __name__ == "__main__":
    main()
