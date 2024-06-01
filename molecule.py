
from vpython import cylinder, mag, norm


class Molecule:

    def __init__(self, atom1, atom2):

        self.atoms = []
        self.atom1 = atom1
        self.atom2 = atom2
        self.atom1.is_bonded = True
        self.atom2.is_bonded = True
        axis = self.atom2.position - self.atom1.position
        # self.bond = cylinder(pos=self.atom1.position, axis=axis)
        self.position = self.set_position()
        self.relative_position1 = self.position-self.atom1.position
        self.relative_position2 = self.atom2.position - self.position
        self.radius = (self.atom2.radius + self.atom1.radius) * 2
        self.velocity = self.set_velocity()

        self.weight = self.atom1.weight + self.atom2.weight

    def set_position(self):
        return (self.atom2.position * self.atom2.weight + self.atom1.position * self.atom1.weight) / \
               (self.atom2.weight + self.atom1.weight)

    def set_velocity(self):
        velocity = (self.atom2.velocity * self.atom2.weight + self.atom1.velocity * self.atom1.weight) / \
        (self.atom2.weight + self.atom1.weight)
        self.atom2.velocity = velocity
        self.atom1.velocity = velocity
        return velocity

    def update_position(self, dt):
        self.position += self.velocity * dt
        self.atom1.position = self.position+self.relative_position1
        self.atom2.position = self.position+self.relative_position2
        self.atom1.atom.pos = self.atom1.position  # Update the visual position
        self.atom2.atom.pos = self.atom2.position  # Update the visual position

    def detect_collision(self, other):
        distance = mag(self.position - other.position)
        return distance < (self.radius + other.radius)

    def handle_collision(self, other):
        if self.detect_collision(other):
            # Calculate the normal and tangential components of the velocities
            collision_normal = norm(self.position - other.position)
            relative_velocity = self.velocity - other.velocity

            # Project the relative velocity onto the normal direction
            velocity_along_normal = relative_velocity.dot(collision_normal)

            # Only handle the collision if the atoms are moving towards each other
            if velocity_along_normal > 0:
                return False

            # Calculate the impulse scalar
            impulse_magnitude = (2 * velocity_along_normal) / (self.weight + other.weight)

            # Apply the impulse to the velocities
            self.velocity -= impulse_magnitude * other.weight * collision_normal
            other.velocity += impulse_magnitude * self.weight * collision_normal

            return True