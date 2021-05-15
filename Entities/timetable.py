import numpy as np
import random
import collections

from Entities.place import Place
from Entities.Enums.category import Category


class Timetable:
    def __init__(self, random_timetable=None, moderation=None, array=None):

        if array is None:
            self.moderation = moderation

            timetable = np.zeros(
                (len(random_timetable), 2 + (2 * (moderation + 2))), dtype=int
            )

            for i, day in enumerate(random_timetable):

                timetable[i][1: len(day[0]) + 1] = day[0]
                timetable[i][-(len(day[1]) + 1): -1] = day[1]

            self.timetable = timetable

        else:
            self.timetable = array

    def __str__(self):
        string = ""
        for i, day in enumerate(self.timetable):

            string = string + "Day " + str(i + 1) + "\n"
            string = string + "---------\n"

            new_duration = 0

            for i, place in enumerate(day[:-1]):

                current_place = Place.get_place_by_id(place)
                string = string + current_place.name
                string = string + ", "
                string = string + str(current_place.category.value)
                if current_place.place_name is not None:
                    string = string + ", " + str(current_place.place_name)
                string = string + " -> \n"

                new_duration = (
                    new_duration
                    + current_place.time_to(Place.get_place_by_id(day[i + 1]))[0]
                )

            string = string + Place.get_place_by_id(day[-1]).name
            string = string + "\n Travel time:  " + str(new_duration) + " \n"
            string = string + "\n --------- \n"

        return string

    def update_timetable(self, new_timetable):
        self.timetable = new_timetable

    @staticmethod
    def calculate_score(timetable):

        y = list(
            map(lambda x: get_day_score(
                x, timetable.moderation), timetable.timetable)
        )
        avg = sum(y)

        return avg

    @staticmethod
    def generate_random_day(trip, day, night, day_norm, night_norm):

        temp_select_random_categories(
            day, day_norm, trip.moderation, True)

        temp_select_random_categories(
            night, night_norm, trip.moderation, False)

        # night_generated = select_random_categories(
        # night, night_norm, trip.moderation, False
        # )
        # print("day_generated", day_generated)
        # print("night_generatel", night_generated)

        # day_ids = []

        # for i in day_generated:

        # day_ids.append(select_random_place(i, max_ratings[i]).id)

        # night_ids = []

        # for i in night_generated:

        # night_ids.append(select_random_place(i, max_ratings[i]).id)

        # return [day_ids, night_ids]

    @staticmethod
    def generate_random_timetable(trip):

        day = []
        night = []
        day_values = []
        night_values = []

        for category in Category.get_categories_time():
            if category[1] == 0:
                day.append(category[0])
                day_values.append(
                    trip.characteristics[0].get_value_by_category(category[0])
                )
            else:
                night.append(category[0])
                night_values.append(
                    trip.characteristics[0].get_value_by_category(category[0])
                )

        day_values = [float(i) / sum(day_values) for i in day_values]
        night_values = [float(i) / sum(night_values) for i in night_values]

        random_timetable = []

        number_of_days = (trip.date[1] - trip.date[0]).days

        for _ in range(number_of_days):

            random_timetable.append(
                Timetable.generate_random_day(
                    trip, day, night, day_values, night_values
                )
            )

        # return Timetable(random_timetable, trip.moderation)


def get_day_score(day, moderation):

    # Total number of unique events
    total_events = set(day)
    total_events_score = len(total_events) / (len(day) - 3)

    total_ratings = []
    category_list = []
    durations_list = []

    for i, place_id in enumerate(day[:-1]):

        place = Place.get_place_by_id(place_id)
        next_place = Place.get_place_by_id(day[i + 1])

        category_list.append(place.category)
        durations_list.append(place.time_to(next_place)[0])

        if place.rating is not None:
            total_ratings.append(place.rating)
        else:
            total_ratings.append(0.0)

    avg_rating = 0
    if total_ratings != []:
        avg_rating = (sum(total_ratings) / (len(total_ratings) - 2)) / 5.0

    total_durations = sum(durations_list)

    if total_durations == 0:
        return 0

    duration_score = 10 / sum(durations_list)

    total_score = total_events_score + duration_score + avg_rating

    counter = collections.Counter(category_list)

    for i in counter:

        if counter[i] > 3 and i != Category.accomodation:
            total_score = 0

    if counter[Category.restaurant] > 1 or counter[Category.cafe] > 1:
        total_score = 0

    return total_score


def get_normalised_values(day_values, night_values):

    values = day_values + night_values

    norm_values = [float(i) / sum(values) for i in values]

    day_norm = norm_values[: len(day_values)]
    night_norm = norm_values[-len(night_values):]
    day_norm.append(1 - sum(day_norm))
    night_norm.append(1 - sum(night_norm))

    return day_norm, night_norm


def select_random_place(category, max_ratings):
    places = Place.of_category(category)
    places_values = []

    for i in places:
        places_values.append(
            (i.no_of_ratings / max_ratings) + (i.rating / 5.0))

    norm_values = [float(i) / sum(places_values) for i in places_values]

    random_choice = np.random.choice(places, 1, p=norm_values)

    return random.choice(random_choice)


def temp_select_random_categories(categories, normalised_values,
                                  moderation, day):

    generated_day = []
    generated_night = []

    if day:
        random_choice = np.random.choice(categories, 1, p=normalised_values)
        generated_day.append(random_choice)
        generated_day.append(Category.cafe)

        for _ in range(moderation):
            random_choice = np.random.choice(
                categories, 1, p=normalised_values)
            generated_day.append(random_choice)
        print(generated_day)
    else:
        generated_night.append(Category.restaurant)
        random_choice = np.random.choice(categories, 1, p=normalised_values)
        generated_night.append(random_choice)

        print(generated_night)


def select_random_categories(categories, normalised_values, moderation, day):
    generated_places = []
    food_added = False
    number_of_activities = random.randint(moderation, moderation + 2)

    if not day:
        generated_places.append(Category.restaurant)

    if sum(normalised_values) != 0:

        for i in range(number_of_activities)[1:]:

            random_choice = np.random.choice(
                categories, 1, p=normalised_values)

            while (
                random_choice == Category.cafe or random_choice == Category.restaurant
            ):

                random_choice = np.random.choice(
                    categories, 1, p=normalised_values)
            if random_choice[0] is not None:
                generated_places.append(random_choice[0])

            if day and not food_added:
                food_added = bool(random.getrandbits(1))
                if food_added:
                    generated_places.append(Category.cafe)

    if day and not food_added:
        generated_places.append(Category.cafe)

    return generated_places
