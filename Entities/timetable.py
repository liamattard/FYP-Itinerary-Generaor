import numpy as np
import random
import collections

from Entities.place import Place
from Entities.Enums.category import Category


class Timetable:
    def __init__(self, timetable=None, moderation=1, array=None):

        if array == None:
            self.days = []

            for day in timetable:
                morning = np.zeros((2 + moderation), dtype=np.int32)
                evening = np.zeros(2, dtype=np.int32)

                for i, place in enumerate(day[0]):
                    morning[i] = place.id

                for i, place in enumerate(day[1]):
                    evening[i] = place.id

                self.days.append([morning, evening])
        else:
            self.days = []
            self.days.append(array)

    def __str__(self):
        string = ""
        for i, day in enumerate(self.days):

            string = string + "Day " + str(i + 1) + "\n"
            string = string + "---------\n"

            string = string + "...morning... \n"

            new_duration = 0

            for j, place in enumerate(day[0][:-1]):

                if j == 0:
                    next_place = Place.cafe_places_by_id[day[0][j + 1]]
                else:
                    next_place = Place.day_places_by_id[day[0][j + 1]]

                if j == 1:
                    current_place = Place.cafe_places_by_id[place]
                else:
                    current_place = Place.day_places_by_id[place]

                string = string + current_place.name
                string = string + ", "
                string = string + str(current_place.category.value)
                # if current_place.place_name is not None:
                # string = string + ", " + str(current_place.place_name)
                string = string + " -> \n"

                new_duration = new_duration + current_place.time_to(next_place)[0]

            string = string + Place.day_places_by_id[day[0][-1]].name
            string = string + "\n Travel time:  " + str(new_duration) + " \n"
            string = string + "\n --------- \n"

            string = string + "...evening... \n"

            # Evening

            new_duration = 0

            current_place = Place.restaurant_places_by_id[day[1][0]]
            string = string + current_place.name
            string = string + ", "
            string = string + str(current_place.category.value)
            string = string + " -> \n"

            new_duration = (
                new_duration
                + current_place.time_to(Place.night_places_by_id[day[1][1]])[0]
            )

            string = string + Place.night_places_by_id[day[1][1]].name
            string = string + "\n Travel time:  " + str(new_duration) + " \n"
            string = string + "\n --------- \n"

        return string

    def update_timetable(self, new_timetable):
        self.days[0][0] = new_timetable

    @staticmethod
    def calculate_score(timetable, is_Day):

        # y = list(
        # map(lambda x: get_day_score(x, timetable.moderation), timetable.timetable)
        # )
        # avg = sum(y)

        if is_Day:
            avg = get_day_score(timetable.days[0][0], is_Day)
        else:
            avg = get_day_score(timetable.days[0][1], is_Day)

        return avg

    @staticmethod
    def generate_random_day(trip, day, night, day_norm, night_norm):

        day_categories, day_norm = generate_random_night_day(
            day, day_norm, trip.moderation, True
        )

        night_categories, night_norm = generate_random_night_day(
            night, night_norm, trip.moderation, False
        )

        return [day_categories, night_categories], day_norm, night_norm

    def remove_days_from_list(self):
        for day in self.days:
            for i, place_id in enumerate(day[0]):
                if i == 1:
                    place = Place.cafe_places_by_id[place_id]
                    Place.delete_place(place.category, place)
                else:
                    place = Place.day_places_by_id[place_id]
                    Place.delete_place(place.category, place)
            for i, place_id in enumerate(day[1]):
                if i == 0:
                    place = Place.restaurant_places_by_id[place_id]
                    Place.delete_place(place.category, place)
                else:
                    place = Place.night_places_by_id[place_id]
                    Place.delete_place(place.category, place)

    @staticmethod
    def generate_random_timetable(trip):

        # Splitting categories into day and night and calculating their
        # probabilities based on the user's characteristics

        day_result = []
        night_result = []
        day_values = []
        night_values = []

        for category in Category.get_categories_time():
            if category[1] == 0:
                day_result.append(category[0])
                day_values.append(
                    trip.characteristics[0].get_value_by_category(category[0])
                )
            else:
                night_result.append(category[0])
                night_values.append(
                    trip.characteristics[0].get_value_by_category(category[0])
                )

        # Normalising the probabilities

        day_values = [float(i) / sum(day_values) for i in day_values]
        night_values = [float(i) / sum(night_values) for i in night_values]

        random_timetable = []

        number_of_days = (trip.date[1] - trip.date[0]).days

        # Generating the timetable

        for _ in range(number_of_days):

            result, day_values, night_values = Timetable.generate_random_day(
                trip, day_result, night_result, day_values, night_values
            )
            random_timetable.append(result)

        # Re-Adding the places to the places's list

        for day_result in result[0]:
            Place.readd_place(day_result)

        for night_result in result[1]:
            Place.readd_place(night_result)

        return Timetable(random_timetable, moderation=trip.moderation)


def get_day_score(day, is_Day):

    if is_Day:

        # Total number of unique events
        total_events = set(day)
        if len(total_events) != len(day):
            return 0

        total_ratings = []
        durations_list = []

        for i, place_id in enumerate(day):

            if i != (len(day) - 1):

                if i == 1:
                    place = Place.cafe_places_by_id[place_id]
                else:
                    place = Place.day_places_by_id[place_id]
                if i == 0:
                    next_place = Place.cafe_places_by_id[day[i + 1]]
                else:
                    next_place = Place.day_places_by_id[day[i + 1]]

                durations_list.append(place.time_to(next_place)[0])

            if place.rating is not None:
                total_ratings.append(place.rating)
            else:
                total_ratings.append(0.0)
        avg_rating = 0
        if total_ratings != []:
            avg_rating = (sum(total_ratings) / len(total_ratings)) / 10.0

        total_durations = sum(durations_list)

        if total_durations == 0:
            return 0
        duration_score = 10 / total_durations

    else:
        place_one = Place.restaurant_places_by_id[day[0]]
        place_two = Place.night_places_by_id[day[1]]
        duration_score = 1 / (place_one.time_to(place_two)[0])
        avg_rating = (place_one.rating + place_two.rating) / 5

    total_score = duration_score + avg_rating

    return total_score


def get_normalised_values(day_values, night_values):

    values = day_values + night_values

    norm_values = [float(i) / sum(values) for i in values]

    day_norm = norm_values[: len(day_values)]
    night_norm = norm_values[-len(night_values) :]
    day_norm.append(1 - sum(day_norm))
    night_norm.append(1 - sum(night_norm))

    return day_norm, night_norm


def select_random_place(category):
    places = Place.of_category(category)
    places_values = []

    if places != []:
        max_ratings = max([i.no_of_ratings for i in places])

        for place in places:
            places_values.append(
                (place.no_of_ratings / max_ratings) + (place.rating / 5.0)
            )

        norm_values = [float(i) / sum(places_values) for i in places_values]

        random_choice = np.random.choice(places, 1, p=norm_values)
        Place.remove_place(category, random_choice)

        return random_choice[0]
    else:
        return None


def get_a_place(categories, normalised_values):

    if categories == []:
        print("ERROR, EMPTY CATEGORIES")
    normalised_values = [float(i) / sum(normalised_values) for i in normalised_values]

    random_place = None
    while random_place == None:
        random_choice = np.random.choice(categories, 1, p=normalised_values)
        random_place = select_random_place(random_choice[0])

        if random_place == None:
            normalised_values = np.delete(
                normalised_values, categories.index(random_choice[0])
            )
            categories.remove(random_choice[0])
            normalised_values = [
                float(i) / sum(normalised_values) for i in normalised_values
            ]

    return random_place, normalised_values


def generate_random_night_day(categories, normalised_values, moderation, day):

    generated_places = []

    if day:
        place, normalised_values = get_a_place(categories, normalised_values)
        generated_places.append(place)
        generated_places.append(select_random_place(Category.cafe))

        for _ in range(moderation):
            place, normalised_values = get_a_place(categories, normalised_values)
            generated_places.append(place)
    else:
        generated_places.append(select_random_place(Category.restaurant))
        place, normalised_values = get_a_place(categories, normalised_values)
        generated_places.append(place)

    return generated_places, normalised_values


def select_random_categories(categories, normalised_values, moderation, day):
    generated_places = []
    food_added = False
    number_of_activities = random.randint(moderation, moderation + 2)

    if not day:
        generated_places.append(Category.restaurant)

    if sum(normalised_values) != 0:

        for _ in range(number_of_activities)[1:]:

            random_choice = np.random.choice(categories, 1, p=normalised_values)

            while (
                random_choice == Category.cafe or random_choice == Category.restaurant
            ):

                random_choice = np.random.choice(categories, 1, p=normalised_values)
            if random_choice[0] is not None:
                generated_places.append(random_choice[0])

            if day and not food_added:
                food_added = bool(random.getrandbits(1))
                if food_added:
                    generated_places.append(Category.cafe)

    if day and not food_added:
        generated_places.append(Category.cafe)

    return generated_places
