import math

from vpython import vector, color, sphere, mag, norm
from random import randrange, gauss, random, uniform


class Atom:

    def __init__(self, range_, temperature):
        self.symbol = "He"
        self.position = vector(uniform(-range_, range_), uniform(-range_, range_), uniform(-range_, range_))
        self.radius = 1.4
        self.color = color.blue
        self.velocity = self.set_velocity(temperature)
        self.weight = 4
        self.atom = sphere(pos=self.position, radius=self.radius, color=self.color)
        self.is_molecule = False
        self.is_bonded = False  # if bonded do not update the position

    def update(self):
        self.atom.pos = self.position
        self.atom.radius = self.radius
        self.atom.color = self.color

    def update_position(self, dt):
        if not self.is_molecule:
            self.position += self.velocity * dt
            self.atom.pos = self.position  # Update the visual position

        elif not self.is_bonded:  # To ensure only one time position is updated
            self.update_position(dt)

    def detect_collision(self, other):
        distance = mag(self.position - other.position)
        return distance < (self.radius + other.radius)

    def handle_collision(self, other, activation_energy):
        if self.detect_collision(other):
            # Calculate the relative kinetic energy
            kinetic_energy = 0.5 * (self.weight * mag(self.velocity) ** 2 + other.weight * mag(other.velocity) ** 2)

            # If the kinetic energy exceeds the activation energy, form a molecule
            if kinetic_energy > activation_energy:
                if not self.is_molecule and not other.is_molecule:
                    if self.symbol == "H" and other.symbol == "Cl":
                        self.form_molecule(other)
                        return True

            # Otherwise, handle the collision normally
            collision_normal = norm(self.position - other.position)
            relative_velocity = self.velocity - other.velocity
            velocity_along_normal = relative_velocity.dot(collision_normal)

            # Only handle the collision if the atoms are moving towards each other
            if velocity_along_normal > 0:
                return False

            # Calculate the impulse scalar
            impulse_magnitude = (2 * velocity_along_normal) / (self.weight + other.weight)

            # Apply the impulse to the velocities
            self.velocity -= impulse_magnitude * other.weight * collision_normal
            other.velocity += impulse_magnitude * self.weight * collision_normal

        return False

    def form_molecule(self, other):
        self.is_molecule = True
        other.is_molecule = True
        self.is_bonded = True
        other.is_bonded = True


    def maxwell_boltzmann_speed(self, temperature):
        """Generate a speed based on the Maxwell-Boltzmann distribution."""
        # Constants
        k_B = 1.380649e-23  # Boltzmann constant in J/K
        m = 1.66053906660e-27  # Mass of particle in kg (example value)

        # Calculate the scale factor for the Maxwell-Boltzmann distribution
        scale_factor = math.sqrt(k_B * temperature / m)

        # Box-Muller transform to generate normally distributed values
        u1 = random()
        u2 = random()
        z = scale_factor * math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * u2)

        return abs(z)

    def set_velocity(self, temperature):
        speed = self.maxwell_boltzmann_speed(temperature)

        # Random direction with the given speed
        theta = uniform(0, 2 * math.pi)
        phi = uniform(0, math.pi)

        vx = speed * math.sin(phi) * math.cos(theta)
        vy = speed * math.sin(phi) * math.sin(theta)
        vz = speed * math.cos(phi)

        return vector(vx, vy, vz)

    def get_speed(self):
        return mag(self.velocity)
