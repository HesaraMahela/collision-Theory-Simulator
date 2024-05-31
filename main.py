from vpython import rate, label, vector, mag, color, box
from atoms import Atom

# Simulation parameters
temperature = 30  # Temperature in Kelvin
atom_count = 4  # Number of atoms
xmax = 10
ymax = 10
zmax = 10
volume = (2 * xmax) * (2 * ymax) * (2 * zmax)  # Volume of the box

# Create atoms with velocities based on temperature
atom_list = [Atom(5, temperature) for _ in range(atom_count)]

# Change or add atoms
special_atom = atom_list[0]
special_atom.velocity = vector(0,0,0)
special_atom.weight = 131
special_atom.radius = 2.16
special_atom.color = color.cyan
special_atom.update()
atom_list.append(special_atom)

# Create the box
container = box(pos=vector(0,0,0), size=vector(2*xmax, 2*ymax, 2*zmax), color=color.white, opacity=0.1)

# Display labels
kinetic_energy_label = label(pos=vector(0, 1, 0), text='Kinetic Energy: ', box=False, height=10)
pressure_label = label(pos=vector(0, 4, 0), text='Pressure: ', box=False, height=10)


def calculate_kinetic_energy():
    total_ke = 0
    for atom in atom_list:
        speed_squared = mag(atom.velocity) ** 2
        total_ke += 0.5 * atom.weight * speed_squared
    return total_ke


def calculate_pressure(ke_total, volume):
    return (2 / 3) * (ke_total / volume)


def calculate_micro_pressure(atom_list, dt):
    momentum_change = 0
    for atom in atom_list:
        # Calculate momentum change for wall collisions
        if abs(atom.position.x) > xmax - atom.radius:
            momentum_change += 2 * atom.weight * abs(atom.velocity.x)
        if abs(atom.position.y) > ymax - atom.radius:
            momentum_change += 2 * atom.weight * abs(atom.velocity.y)
        if abs(atom.position.z) > zmax - atom.radius:
            momentum_change += 2 * atom.weight * abs(atom.velocity.z)

    # Average force over the time step
    force = momentum_change / dt
    # Pressure is force divided by the area of the walls
    surface_area = 2 * (2 * xmax * 2 * ymax + 2 * xmax * 2 * zmax + 2 * ymax * 2 * zmax)
    pressure = force / surface_area
    return pressure

# Simulation loop
dt = 0.001
while True:
    rate(50)  # Run 100 iterations per second

    for i, atom in enumerate(atom_list):
        atom.update_position(dt)

        # Handle collisions with walls
        if abs(atom.position.x) > xmax - atom.radius:
            atom.velocity.x = -atom.velocity.x
        if abs(atom.position.y) > ymax - atom.radius:
            atom.velocity.y = -atom.velocity.y
        if abs(atom.position.z) > zmax - atom.radius:
            atom.velocity.z = -atom.velocity.z

        # Handle collisions with other atoms
        for j in range(i + 1, len(atom_list)):
            atom.handle_collision(atom_list[j])

        # Calculate total kinetic energy
    total_kinetic_energy = calculate_kinetic_energy()
    kinetic_energy_label.text = f'Total Kinetic Energy: {total_kinetic_energy} J'

    # Calculate pressure
    pressure = calculate_pressure(total_kinetic_energy, volume)
    pressure_label.text = f'Pressure: {pressure:} Pa'
