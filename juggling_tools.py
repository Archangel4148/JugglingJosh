import math
from dataclasses import dataclass

import pygame


@dataclass
class JugglingEnvironment:
    width_pix: int
    height_pix: int
    gravity: float
    floor_y: float
    ceiling_y: float
    scaling_factor: float
    left_hand_x: int | None
    right_hand_x: int | None
    use_distance_and_max_height: bool

    def get_gravity_scaled(self) -> float:
        return self.gravity * self.scaling_factor


class Ball:
    def __init__(self, environment: JugglingEnvironment, x: float, y: float, radius: float, color: tuple[int, int, int],
                 name: str = "Unnamed Ball"):
        self.environment = environment
        self.initial_x = x
        self.initial_y = y
        self.radius = radius
        self.color = color  # Using RGB colors
        self.name = name
        self.x = self.initial_x
        self.y = self.initial_y

        # Ball is initially at rest
        self.velocity_x = 0
        self.velocity_y = 0
        self.previous_velocity_y = 0
        self.is_airborne = False

    def update(self, dt: float):
        # Update previous velocity
        self.previous_velocity_y = self.velocity_y

        # Apply gravity (scaled for pixel world)
        self.velocity_y += self.environment.get_gravity_scaled() * dt
        # Update position
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt

        # Check if the ball has hit the ground (starting y-value)
        if self.y >= self.environment.floor_y:
            self.y = self.environment.floor_y
            # "Catch" the ball
            self.velocity_y = 0
            self.velocity_x = 0
            self.is_airborne = False
        else:
            self.is_airborne = True

    def draw(self, main_screen: pygame.Surface):
        pygame.draw.circle(main_screen, self.color, (int(self.x), int(self.y)),
                           self.radius * self.environment.scaling_factor)

    def throw(self, velocity: float, angle: float):
        if self.is_airborne:
            print("Attempted to throw a ball that is already airborne.")
            return

        # Convert velocity to pixels per second
        velocity *= self.environment.scaling_factor

        # Check which hand the ball is in
        if self.x > self.environment.width_pix / 2:
            velocity_x = -velocity * math.cos(math.radians(angle))
            velocity_y = -velocity * math.sin(math.radians(angle))
        else:
            velocity_x = velocity * math.cos(math.radians(angle))
            velocity_y = -velocity * math.sin(math.radians(angle))

        # Throw the ball
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y

    def is_in_hand(self, hand: str):
        if self.is_airborne:
            return
        center = self.environment.width_pix / 2
        if hand.casefold() == "left":
            return self.x < center
        elif hand.casefold() == "right":
            return self.x > center
        else:
            raise ValueError(f"Invalid hand: {hand}")

    def reset(self):
        self.x = self.initial_x
        self.y = self.initial_y
        self.velocity_x = 0
        self.velocity_y = 0
        self.is_airborne = False
