import numpy as np
import random

from Entities.place import Place
from Entities.timetable import Timetable
from Optimiser.particle import Particle


def initialise_particles(trip, population_size):

    # Getting all places
    particles = []
    all_places, max_ratings = Place.get_day_places(trip.characteristics[0])
    upperBound = len(all_places)
    number_of_days = (trip.date[1] - trip.date[0]).days
    global_best = None

    for _ in range(population_size):

        timetable = Timetable.generate_random_timetable(
            trip, max_ratings, number_of_days
        )

        current_particle = Particle(timetable)
        particles.append(current_particle)

        if global_best is None:
            global_best = current_particle

        if current_particle.get_score() > global_best.get_score():
            global_best = current_particle

    return particles, global_best, upperBound


def Optimise(trip):

    iterations = 35
    population_size = 100
    inertia = 5
    personal_acceleration = 7
    global_acceleration = 8

    particles, global_best, upperBound = initialise_particles(
        trip, population_size)

    print("Initial best global score ", global_best.get_score())

    for i in range(iterations):
        for particle in particles:

            for j in range(inertia):
                col = random.randint(0, (particle.position.shape[0] - 1))
                row = random.randint(1, ((particle.position.shape[1] - 2)))
                inc = random.randint(1, 3)

                particle.position[col, row] = particle.position[col, row] + inc
            np.clip(particle.position, 0, upperBound, out=particle.position)

            for k in range(personal_acceleration):

                particle.position = switch_random(
                    particle.position, particle.personal_best_position
                )

            for z in range(global_acceleration):

                particle.position = switch_random(
                    particle.position, global_best.position
                )

            particle.update_timetable(particle.position)

            new_score = particle.get_score()
            if new_score > particle.personal_best.get_score():

                particle.personal_best = particle

                if new_score > global_best.get_score():
                    global_best = particle

        print("Current Best Score", global_best.get_score())
        inertia = inertia - 1

    print("Final best score", global_best.get_score())
    print(global_best.timetable)


def switch_random(original_matrix, switch_matrix):
    col = random.randint(0, (original_matrix.shape[0] - 1))
    row = random.randint(1, (original_matrix.shape[1] - 2))

    original_matrix[col, row] = switch_matrix[col, row]

    return original_matrix


def Optimise_classic(trip):

    iterations = 10
    population_size = 100
    inertia = 5
    personal_acceleration = 2
    global_acceleration = 2
    x = False

    particles, global_best, upperBound = initialise_particles(
        trip, population_size)

    if x:

        global_best_score = global_best.get_score()
        global_best_position = global_best.position

        print("Initial best score ", global_best_score)

        for i in range(iterations):

            for particle in particles:

                if inertia > 0:
                    inertia_velocity = np.random.randint(
                        -inertia, inertia, size=particle.velocity.shape
                    )
                    for col in range(len(inertia_velocity)):
                        inertia_velocity[col][0] = 0
                        inertia_velocity[col][-1] = 0

                else:
                    inertia_velocity = None

                personal_acceleration_matrix = np.random.randint(
                    personal_acceleration, size=particle.velocity.shape
                )

                personal_best_velocity = np.multiply(
                    personal_acceleration_matrix,
                    np.subtract(particle.personal_best_position,
                                particle.position),
                )

                global_acceleration_matrix = np.random.randint(
                    global_acceleration, size=particle.velocity.shape
                )

                global_best_velocity = np.multiply(
                    global_acceleration_matrix,
                    np.subtract(global_best_position, particle.position),
                )

                if inertia_velocity is not None:
                    new_velocity = np.add(
                        inertia_velocity, personal_best_velocity)
                else:
                    new_velocity = personal_best_velocity
                new_velocity = np.add(new_velocity, global_best_velocity)

                new_position = np.add(particle.position, new_velocity)
                np.clip(new_position, 0, upperBound, out=new_position)

                particle.velocity = new_velocity
                particle.update_timetable(new_position)

                new_score = particle.get_score()
                # print(global_best)
                if new_score > particle.personal_best_score:

                    particle.personal_best_score = new_score
                    particle.personal_best_position = particle.position

                    if new_score > global_best_score:
                        global_best_score = new_score
                        global_best_position = particle.position

            print("Current Best Score ", global_best_score)
            inertia = inertia - 1

        print("Final best score ", global_best_score)
        global_best = Timetable(array=global_best_position)
        print(global_best)
