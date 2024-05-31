from vpython import mag


def calculate_kinetic_energy(atom_list_):
    total_ke = 0
    m = 1.66053906660e-27
    for atom in atom_list_:
        speed_squared = mag(atom.velocity) ** 2
        total_ke += 0.5 * atom.weight * m * speed_squared
    return total_ke


def calculate_pressure(ke_total, volume):
    return (2 / 3) * (ke_total / volume)


def calculate_average_speed(atom_list_):
    total_speed = 0
    for atom in atom_list_:
        total_speed += atom.get_speed()
    return total_speed/len(atom_list_)


def calculate_micro_pressure(atom_list, dt, xmax, ymax, zmax):
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
