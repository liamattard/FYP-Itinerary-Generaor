import numpy as np
import random

from Entities.Enums.budget import Budget
from Entities.place import Place
from Entities.Enums.category import Category


class Trip:
    '''
    From this trip object a user will be able to generate itineraries
    that are applicable to his constraints. Constraints include:
    budget, moderation, characteristics, travel date and accomodation.
    '''

    def __init__(
            self, budget: Budget, moderation, characteristics, date,
            accomodation: Place):
        super().__init__()

        self.budget = budget
        self.moderation = moderation
        self.characteristics = characteristics
        self.date = date
        self.accomodation = accomodation

    def generate_random_day(self):

        day = []
        night = []
        day_values = []
        night_values = []

        i = 1
        while i < 11:
            category = Category(i)

            if i < 8:

                day.append(category)
                day_values.append(
                    self.characteristics[0].get_value_by_category(category))
            else:
                night.append(category)
                night_values.append(
                    self.characteristics[0].get_value_by_category(category))

            i = i + 1

        day_norm = [float(i)/sum(day_values) for i in day_values]
        day_generated = select_random(day, day_norm, self.moderation, True)

        night_norm = [float(i)/sum(night_values) for i in night_values]
        night_generated = select_random(
            night, night_norm, self.moderation, False)
        
        for i in day_generated+night_generated:
            print(random.choice(Place.of_category(i)).name)
        # return day_generated + night_generated

    def generate_itineraries(self):

        all_places, max_ratings = Place.get_places(self.characteristics[0])
        print(self.generate_random_day())

        # timetable = Timetable([dateStart, dateFinal], accomodation)
        # timetable.add_place(all_places[0], 1)


def select_random(categories, normalised_values, moderation, day):
    generated_places = []
    food_added = False
    number_of_activities = random.randint(moderation - 1, moderation + 1)

    if not day:
        generated_places.append(Category.restaurant)

    if sum(normalised_values) != 0:

        for i in range(number_of_activities):

            random_choice = np.random.choice(categories, 1,
                                             p=normalised_values)

            while(random_choice == Category.cafe or
                  random_choice == Category.restaurant):

                random_choice = np.random.choice(categories, 1,
                                                 p=normalised_values)
            generated_places.append(random_choice[0])

            if day and not food_added:
                food_added = bool(random.getrandbits(1))
                if food_added:
                    generated_places.append(Category.cafe)

    if day and not food_added:
        generated_places.append(Category.cafe)

    return generated_places
