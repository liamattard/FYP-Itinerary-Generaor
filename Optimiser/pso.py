import numpy as np
import random

from Entities.place import Place
from Entities.timetable import Timetable
from Optimiser.particle import Particle


def initialise_particles(trip, population_size, is_Day):

    # Getting all places
    particles = []
    global_best = None

    for _ in range(population_size):

        timetable = Timetable.generate_random_timetable(trip)

        current_particle = Particle(timetable, is_Day)
        particles.append(current_particle)

        if global_best is None:
            global_best = current_particle

        if current_particle.get_score(is_Day) > global_best.get_score(is_Day):
            global_best = current_particle

    return particles, global_best


def switch_random(original_matrix, switch_matrix):
    col = random.randint(0, (original_matrix.shape[0] - 1))
    row = random.randint(1, (original_matrix.shape[1] - 2))

    original_matrix[col, row] = switch_matrix[col, row]

    return original_matrix


def Optimse(trip):
    x = Optimise_day(trip, 10, 50, 5, 2, 2, True)
    y = Optimise_day(trip, 3, 20, 1, 2, 2, False)
    new_timetable = Timetable(array=[x.days[0][0], y.days[0][1]])
    new_timetable.remove_days_from_list()


def Optimise_day(
    trip,
    iterations,
    population_size,
    inertia,
    personal_acceleration,
    global_acceleration,
    is_Day,
):

    particles, global_best = initialise_particles(trip, population_size, is_Day)

    global_best_score = global_best.get_score(is_Day)
    global_best_position = global_best.position
    global_best_timetable = global_best.timetable

    print("Initial best score ", global_best_score)

    for _ in range(iterations):

        for particle in particles:

            if inertia > 0:
                inertia_velocity = np.random.randint(
                    -inertia, inertia, size=particle.velocity.shape
                )

            else:
                inertia_velocity = None

            personal_acceleration_matrix = np.random.randint(
                personal_acceleration, size=particle.velocity.shape
            )

            personal_best_velocity = np.multiply(
                personal_acceleration_matrix,
                np.subtract(particle.personal_best_position, particle.position),
            )

            global_acceleration_matrix = np.random.randint(
                global_acceleration, size=particle.velocity.shape
            )

            global_best_velocity = np.multiply(
                global_acceleration_matrix,
                np.subtract(global_best_position, particle.position),
            )

            if inertia_velocity is not None:
                new_velocity = np.add(inertia_velocity, personal_best_velocity)
            else:
                new_velocity = personal_best_velocity
            new_velocity = np.add(new_velocity, global_best_velocity)

            new_position = np.add(particle.position, new_velocity)
            clip(new_position, is_Day)

            particle.velocity = new_velocity
            particle.update_timetable(new_position)

            new_score = particle.get_score(is_Day)
            # print(global_best)
            if new_score > particle.personal_best_score:

                particle.personal_best_score = new_score
                particle.personal_best_position = particle.position

                if new_score > global_best_score:

                    global_best_score = new_score
                    global_best_position = particle.position
                    global_best_timetable = particle.timetable

        # print("Current Best Score ", global_best_score)
        inertia = inertia - 1

    print("Final best score ", global_best_score)
    # global_best = Timetable(array=global_best_position)
    return global_best_timetable
    # print(global_best)


def clip(new_position, is_Day):

    if is_Day:
        for i, place_id in enumerate(new_position):

            if place_id < 0:
                new_position[i] = 0
            else:
                if i == 1:
                    if place_id >= len(Place.cafe_places_by_id):
                        new_position[i] = len(Place.cafe_places_by_id) - 1
                else:
                    if place_id >= len(Place.day_places_by_id):
                        new_position[i] = len(Place.day_places_by_id) - 1
    else:

        new_position = np.array(
            [0 if i < 0 else i for i in new_position], dtype=np.int32
        )

        if new_position[0] >= len(Place.restaurant_places_by_id):
            new_position[0] = len(Place.restaurant_places_by_id) - 1

        if new_position[1] >= len(Place.night_places_by_id):
            new_position[1] = len(Place.night_places_by_id) - 1
