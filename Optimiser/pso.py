import numpy as np

from Entities.place import Place
from Entities.timetable import Timetable
from Optimiser.particle import Particle


def initialise_particles(trip, population_size):

    # Getting all places
    particles = []
    all_places, max_ratings = Place.get_places(trip.characteristics[0])
    upperBound = len(all_places)
    number_of_days = (trip.date[1] - trip.date[0]).days
    global_best = 0

    for i in range(population_size):

        timetable = Timetable.generate_random_timetable(
            trip, max_ratings, number_of_days)

        current_particle = Particle(timetable)
        particles.append(current_particle)
        if current_particle.score > global_best:
            global_best = current_particle.score
            global_position = current_particle.position

    return particles, global_best, global_position, upperBound


def Optimise(trip):

    iterations = 30
    population_size = 50
    inertia = 5
    personal_acceleration = 2
    global_acceleration = 2

    particles, global_best, global_position, upperBound = initialise_particles(
        trip, population_size)

    for i in range(iterations):
        for particle in particles:

            inertia_velocity = (np.multiply(inertia, particle.velocity))

            personal_acceleration_matrix = np.random.randint(
                personal_acceleration, size=particle.velocity.shape)

            personal_best_velocity = (np.multiply(
                personal_acceleration_matrix,
                np.subtract(
                    particle.personal_best_position, particle.position)))

            global_acceleration_matrix = np.random.randint(
                global_acceleration, size=particle.velocity.shape)

            global_best_velocity = (np.multiply(
                global_acceleration_matrix,
                np.subtract(
                    global_position, particle.position)))

            new_velocity = np.add(inertia_velocity, personal_best_velocity)
            new_velocity = np.add(new_velocity, global_best_velocity)

            new_position = np.add(particle.position, new_velocity)
            np.clip(new_position, 0, upperBound, out=new_position)

            particle.velocity = new_velocity
            particle.update_timetable(
                new_position)

            new_score = Timetable.calculate_score(particle.timetable)
            # print(global_best)
            if new_score > particle.personal_best:

                particle.personal_best = new_score
                particle.personal_best_position = particle.position

                if new_score > global_best:
                    global_best = new_score
                    global_position = particle.position

            inertia = inertia - 1

    print(particle.timetable)
