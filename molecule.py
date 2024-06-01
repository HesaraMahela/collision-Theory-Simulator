from vpython import cylinder, mag, norm

from atoms import Atom


class Molecule(Atom):

    def __init__(self, atom1, atom2):
        self.atoms = []
        self.atom1 = atom1
        self.atom2 = atom2
        self.atom1.is_bonded = True
        self.atom2.is_bonded = True
        axis = self.atom2.position - self.atom1.position
        # self.bond = cylinder(pos=self.atom1.position, axis=axis)
        self.position = self.set_position()
        self.relative_position1 = self.position - self.atom1.position
        self.relative_position2 = self.atom2.position - self.position
        self.radius = (self.atom2.radius + self.atom1.radius)
        self.velocity = self.set_velocity()

        self.weight = self.atom1.weight + self.atom2.weight
        self.is_molecule = False  # this molecule act as a atom
        self.symbol = self.set_symbol()

    def set_position(self):
        # keep two atom spheres together
        return (self.atom2.position * self.atom2.weight + self.atom1.position * self.atom1.weight) / \
               (self.atom2.weight + self.atom1.weight)

    def set_velocity(self):
        velocity = (self.atom2.velocity * self.atom2.weight + self.atom1.velocity * self.atom1.weight) / \
                   (self.atom2.weight + self.atom1.weight)
        self.atom2.velocity = velocity
        self.atom1.velocity = velocity

        if mag(self.atom2.position) > 20:
            print(self.position, self.velocity, self.atom1.velocity, self.atom2.velocity)

        return velocity

    def update_position(self, dt):
        self.position += self.velocity * dt
        self.atom1.position = self.position + self.relative_position1
        self.atom2.position = self.position + self.relative_position2
        self.atom1.atom.pos = self.atom1.position  # Update the visual position
        self.atom2.atom.pos = self.atom2.position  # Update the visual position

    def set_symbol(self):
        return self.atom1.symbol + self.atom2.symbol
