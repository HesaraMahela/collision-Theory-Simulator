from vpython import rate, label, vector, color, box
from atoms import Atom
from calculations import *
# Simulation parameters
from molecule import Molecule

temperature = 300  # Temperature in Kelvin
atom_count = 6  # Number of atoms
activation_energy = 1e-10 # activation energy for forming a molecule
xmax = 20
ymax = 20
zmax = 10
volume = (2 * xmax) * (2 * ymax) * (2 * zmax)  # Volume of the box

# Create atoms with velocities based on temperature
atom_list = []
molecule_list =[]

# Change or add atoms
for _ in range(10):
    special_atom = Atom(10, temperature)
    # special_atom.velocity = vector(0, 0, 0)
    special_atom.symbol ="H"
    special_atom.weight = 1
    special_atom.radius = 1.2
    special_atom.color = color.cyan
    special_atom.update()
    atom_list.append(special_atom)

for _ in range(5):

    special_atom = Atom(5, temperature)
    special_atom.symbol = "Cl"
    special_atom.velocity = vector(0, 0, 0)
    special_atom.weight = 35.5
    special_atom.radius = 1.7
    special_atom.color = color.purple
    special_atom.update()
    atom_list.append(special_atom)



# Create the box
container = box(pos=vector(0, 0, 0), size=vector(2 * xmax, 2 * ymax, 2 * zmax), color=color.white, opacity=0.1)

# Display labels
average_speed_label = label(pos=vector(0, -1, 0), text='Average speed : ', box=False, height=10)
kinetic_energy_label = label(pos=vector(0, 1, 0), text='Kinetic Energy: ', box=False, height=10)
pressure_label = label(pos=vector(0, 4, 0), text='Pressure: ', box=False, height=10)



# Simulation loop
dt = 0.0001
while True:
    rate(100)  # Run 100 iterations per second

    for i, atom in enumerate(atom_list):
        if not atom.is_molecule:
            atom.update_position(dt)
        else:
            for molecule in molecule_list:
                molecule.update_position(dt)

        # Handle collisions with walls
        if abs(atom.position.x) > xmax - atom.radius:
            atom.velocity.x = -atom.velocity.x
        if abs(atom.position.y) > ymax - atom.radius:
            atom.velocity.y = -atom.velocity.y
        if abs(atom.position.z) > zmax - atom.radius:
            atom.velocity.z = -atom.velocity.z

        # Handle collisions with other atoms
        for j in range(i + 1, len(atom_list)):
            if not atom_list[j].is_molecule:
                if atom.handle_collision(atom_list[j], activation_energy):
                    molecule_list.append(Molecule(atom, atom_list[j]))  # Add the new molecule to the list


        # Calculate total kinetic energy
    total_kinetic_energy = calculate_kinetic_energy(atom_list)
    kinetic_energy_label.text = f'Total Kinetic Energy: {total_kinetic_energy} J'

    # Calculate pressure
    pressure = calculate_pressure(total_kinetic_energy, volume)
    pressure_label.text = f'Pressure: {pressure:} Pa'

    # Calculate average speed
    avg_speed = calculate_average_speed(atom_list)
    average_speed_label.text = f'Average speed : {avg_speed} ms-1'