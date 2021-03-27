import numpy as np
import random

from Entities.Enums.budget import Budget
from Entities.timetable import Timetable
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

    def generate_random_day(self, max_ratings):

        # TODO: Shuffle days + remove max_ratings
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

        day.append(None)
        night.append(None)
        day_norm, night_norm = get_normalised_values(day_values, night_values)

        day_generated = select_random_categories(
            day, day_norm, self.moderation, True)

        night_generated = select_random_categories(
            night, night_norm, self.moderation, False)

        day_ids = []

        for i in day_generated:

            day_ids.append(select_random_place(
                i, max_ratings[i]).id)

        night_ids = []

        for i in night_generated:

            night_ids.append(select_random_place(
                i, max_ratings[i]).id)

        return [day_ids, night_ids]

    def generate_itineraries(self):

        # Getting all places
        all_places, max_ratings = Place.get_places(self.characteristics[0])

        # Generating a random timetable
        number_of_days = (self.date[1] - self.date[0]).days
        random_timetable = []

        for i in range(number_of_days):
            random_timetable.append(self.generate_random_day(max_ratings))

        timetable = Timetable(random_timetable, self.moderation)
        print(timetable)


def get_normalised_values(day_values, night_values):

    values = day_values + night_values

    norm_values = [float(i)/sum(values) for i in values]

    day_norm = norm_values[:len(day_values)]
    night_norm = norm_values[-len(night_values):]
    day_norm.append(1-sum(day_norm))
    night_norm.append(1-sum(night_norm))

    return day_norm, night_norm


def select_random_place(category, max_ratings):
    places = Place.of_category(category)
    places_values = []

    for i in places:
        places_values.append(
            (i.no_of_ratings / max_ratings) + (i.rating / 5.0))

    norm_values = [float(i)/sum(places_values) for i in places_values]

    random_choice = np.random.choice(places, 1,
                                     p=norm_values)

    return random.choice(random_choice)


def select_random_categories(categories, normalised_values, moderation, day):
    generated_places = []
    food_added = False
    number_of_activities = random.randint(moderation, moderation + 2)

    if not day:
        generated_places.append(Category.restaurant)

    if sum(normalised_values) != 0:

        for i in range(number_of_activities)[1:]:

            random_choice = np.random.choice(categories, 1,
                                             p=normalised_values)

            while(random_choice == Category.cafe or
                  random_choice == Category.restaurant):

                random_choice = np.random.choice(categories, 1,
                                                 p=normalised_values)
            if random_choice[0] is not None:
                generated_places.append(random_choice[0])

            if day and not food_added:
                food_added = bool(random.getrandbits(1))
                if food_added:
                    generated_places.append(Category.cafe)

    if day and not food_added:
        generated_places.append(Category.cafe)

    return generated_places
