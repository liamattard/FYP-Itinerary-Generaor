
import numpy as np
import datetime
import random

from Entities.place import Place
from Entities.Enums.category import Category


class Timetable():

    def __init__(self, random_timetable, moderation):

        self.moderation = moderation

        timetable = np.zeros(
            (len(random_timetable), 2+(2 * (moderation + 2))), dtype=int)

        for i, day in enumerate(random_timetable):

            timetable[i][1:len(day[0])+1] = day[0]
            timetable[i][-(len(day[1])+1):-1] = day[1]

        self.timetable = timetable

    def __str__(self):
        string = ""
        for i, day in enumerate(self.timetable):

            string = string + "Day " + str(i + 1) + "\n"
            string = string + "---------\n"

            duration = datetime.timedelta()

            for i, place in enumerate(day[:-1]):

                current_place = Place.get_place_by_id(place)
                string = string + current_place.name
                string = string + ", "
                string = string + str(current_place.category)
                string = string + " -> "

                new_duration = current_place.time_to(
                    Place.get_place_by_id(day[i+1]))[0]

                duration = duration + new_duration

            string = string + Place.get_place_by_id(day[-1]).name
            string = string + "\n Travel time:  " + str(duration) + " \n"
            string = string + "\n --------- \n"

        return string

    def update_timetable(self, new_timetable):
        self.timetable = new_timetable

    @staticmethod
    def calculate_score(timetable):

        y = list(map(lambda x: get_day_score(
            x, timetable.moderation), timetable.timetable))
        avg = sum(y)/len(y)

        return avg

    @staticmethod
    def generate_random_day(trip, max_ratings):
        # TODO: maybe shuffle days + remove max_ratings
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
                    trip.characteristics[0].get_value_by_category(category))
            else:
                night.append(category)
                night_values.append(
                    trip.characteristics[0].get_value_by_category(category))

            i = i + 1

        day.append(None)
        night.append(None)
        day_norm, night_norm = get_normalised_values(day_values, night_values)

        day_generated = select_random_categories(
            day, day_norm, trip.moderation, True)

        night_generated = select_random_categories(
            night, night_norm, trip.moderation, False)

        day_ids = []

        for i in day_generated:

            day_ids.append(select_random_place(
                i, max_ratings[i]).id)

        night_ids = []

        for i in night_generated:

            night_ids.append(select_random_place(
                i, max_ratings[i]).id)

        return [day_ids, night_ids]

    @staticmethod
    def generate_random_timetable(trip, max_ratings, number_of_days):

        random_timetable = []

        for i in range(number_of_days):

            random_timetable.append(
                Timetable.generate_random_day(trip, max_ratings))

        return Timetable(random_timetable, trip.moderation)


def get_day_score(day, moderation):

    total_duration = datetime.timedelta()
    total_events = set()
    total_ratings = []

    for i, place_id in enumerate(day[:-1]):
        place = Place.get_place_by_id(place_id)
        total_events.add(place.name)
        next_place = Place.get_place_by_id(day[i+1])
        total_duration = total_duration + place.time_to(next_place)[0]
        if place.rating is not None:
            total_ratings.append(place.rating)

    avg_rating = 0
    if total_ratings != []:
        avg_rating = (sum(total_ratings)/len(total_ratings))/5.0

    total_events_score = len(total_events) / ((2 * moderation) + 2)
    total_duration_score = 0
    if total_duration.seconds != 0:
        total_duration_score = (5400/total_duration.seconds)

    total_score = total_events_score + total_duration_score + avg_rating

    return total_score


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
