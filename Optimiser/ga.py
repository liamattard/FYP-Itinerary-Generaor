import numpy as np
import random

from geneticalgorithm2 import geneticalgorithm2 as ga
from Entities.place import Place
from Entities.timetable import Timetable
from Optimiser.particle import Particle


def initialise_particles(trip, population_size, is_Day):

    # Getting all places
    particles = []

    for _ in range(population_size):

        timetable = Timetable.generate_random_timetable(trip)

        # current_particle = Particle(timetable, is_Day, trip)
        particles.append(np.array(timetable.days[0][0]))

    return np.array(particles)


def getScore(timetable):

    global trip
    global is_Day
    global places_bound
    global cafe_bound

    new_timetable = Timetable()
    new_timetable.add_a_new_day([timetable, [0, 0]])
    return -Timetable.calculate_score(new_timetable, is_Day, trip)


def Optimise(trip):

    new_timetable = Timetable()

    for i in range(trip.number_of_days):

        x = Optimise_day(trip)
        new_timetable.add_a_new_day([x, [0, 0]])

        new_timetable.remove_days_from_list(i)

    # new_timetable.add_a_new_day([[19, 15, 37], [0, 0]])
    new_timetable.days = []
    print(new_timetable)
    return new_timetable


trip = None
is_Day = True
places_bound = 0
cafe_bound = 0


def Optimise_day(trip_recieved):

    global trip
    global places_bound
    global cafe_bound

    popsize = 50
    places_bound = len(Place.day_places_by_id) - 1
    cafe_bound = len(Place.cafe_places_by_id) - 1
    print(places_bound)
    print(cafe_bound)

    trip = trip_recieved

    particles = initialise_particles(trip, popsize, True)

    x = [[0, places_bound], [0, cafe_bound]] + [[0, places_bound]] * trip.moderation
    print(x)
    varBound = np.array(x)
    vartype = np.array(["int", "int"] + ["int"] * trip.moderation)

    algorithm_param = {
        "max_num_iteration": 15,
        "population_size": popsize,
        "mutation_probability": 0.1,
        "elit_ratio": 0.01,
        "crossover_probability": 0.5,
        "parents_portion": 0.3,
        # "crossover_type": "uniform",
        # "mutation_type": "uniform_by_center",
        # "selection_type": "roulette",
        "max_iteration_without_improv": None,
    }

    model = ga(
        function=getScore,
        dimension=trip.moderation + 2,
        variable_type="int",
        variable_boundaries=varBound,
        algorithm_parameters=algorithm_param,
    )

    # model.run(start_generation={"variables": particles, "scores": None})
    model.run(
        no_plot=True,
        disable_progress_bar=True,
        disable_printing=True,
        start_generation={"variables": particles, "scores": None},
    )

    max = 0
    for i in particles:
        score = getScore(i)
        if score > max:
            max = score

    print("Initial Score:", score)
    print("Best Score:", model.output_dict["function"])
    return model.output_dict["variable"]
    # for i in particles:
    # print(getScore(i))
