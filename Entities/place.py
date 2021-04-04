import json
import requests
import requests_cache

from Entities.hours import Hours
from Entities.characteristics import Characteristic
from Entities.location import Location
from Entities.Enums.transport import Transport
from Entities.rating import Rating
from Entities.Enums.category import Category
from Entities.category_constant import Category_Constant
from Entities.Enums.price import Price
from os import listdir
from os.path import isfile, join

id = 0

place_by_id = {}


requests_cache.install_cache("demo_cache")


class Place:
    def __init__(
        self,
        name: str = None,
        hours: Hours = None,
        price: Price = None,
        rating: Rating = None,
        no_of_ratings: int = None,
        location: Location = None,
        category: Category = None,
        place_name=None,
        time=None,
    ):

        super().__init__()
        global id

        self.name = name
        self.hours = hours
        self.price = price
        self.rating = rating
        self.no_of_ratings = no_of_ratings
        self.location = location
        self.category = category
        self.id = id
        self.place_name = place_name
        place_by_id[id] = self
        id = id + 1

        if time is not None:
            self.time = time

    def time_to(self, place_two):

        url = "http://127.0.0.1:5000/table/v1/driving/"
        url = url + str(self.location.y) + "," + str(self.location.x) + ";"
        url = url + str(place_two.location.y) + "," + str(place_two.location.x)
        duration = requests.get(url).json()
        duration_time = (duration["durations"][0][1]) / 60

        # distance = geopy.distance.geodesic(
        #     place_one_location, place_two_location).m
        # avg_speed = 13.8889

        # time = distance / avg_speed
        # if time != 0:
        #     time = time + 1000

        # time = datetime.timedelta(seconds=time)

        return duration_time, Transport.car

    @staticmethod
    def get_places(characteristics):

        all_places = []
        path = "NearbySearch/POIs/"
        all_places = create_place(
            path, all_places, Category.point_of_interest, characteristics
        )

        path = "NearbySearch/beach/"
        all_places = create_place(path, all_places, Category.beach, characteristics)

        path = "NearbySearch/museums/"
        all_places = create_place(path, all_places, Category.museums, characteristics)

        path = "NearbySearch/nature/"
        all_places = create_place(path, all_places, Category.nature, characteristics)

        path = "NearbySearch/night_clubs/"
        all_places = create_place(path, all_places, Category.club, characteristics)

        path = "NearbySearch/bars/"
        all_places = create_place(path, all_places, Category.bar, characteristics)

        path = "NearbySearch/restaurants/"
        all_places = create_place(
            path, all_places, Category.restaurant, characteristics
        )

        path = "NearbySearch/amusementParks/"
        all_places = create_place(
            path, all_places, Category.amusement_park, characteristics
        )

        path = "NearbySearch/shopping/"
        all_places = create_place(path, all_places, Category.shopping, characteristics)

        path = "NearbySearch/cafeterias/"
        all_places = create_place(path, all_places, Category.cafe, characteristics)

        return all_places, max_ratings

    @staticmethod
    def get_place_by_id(id):
        return place_by_id[id]

    @staticmethod
    def of_category(category):
        return places_of_category[category]


max_ratings = {}
for i in Category:
    max_ratings[i] = 0

places_of_category = {}
for i in Category:
    places_of_category[i] = []


def create_place(path, all_places, category, characteristics: Characteristic):

    results = [f for f in listdir(path) if isfile(join(path, f))]

    for i in results:

        f = open(path + i,)
        x = json.load(f)

        for i in x["results"]:

            if "rating" in i:

                name = i["name"]
                rating = i["rating"]
                no_of_ratings = i["user_ratings_total"]
                longitude = i["geometry"]["location"]["lng"]
                latitude = i["geometry"]["location"]["lat"]
                location = Location(latitude, longitude)
                price_level = None

                if "price_level" in i:
                    price_level = i["price_level"]

                if "vicinity" in i:
                    vicinity = i["vicinity"].split(",")[-1]

                time = calculate_time(characteristics, rating, category)

                new_place = Place(
                    name=name,
                    price=price_level,
                    rating=rating,
                    no_of_ratings=no_of_ratings,
                    category=category,
                    location=location,
                    time=time,
                    place_name=vicinity,
                )

                all_places.append(new_place)
                places_of_category[category].append(new_place)

                if max_ratings[category] < no_of_ratings:
                    max_ratings[category] = no_of_ratings

    return all_places


def calculate_time(characteristics, rating, category):
    userPref = characteristics.get_value_by_category(category) / 100
    rating = (rating * 20) / 100

    time = userPref * rating * Category_Constant[category]
    time = 0.5 * round(float(time) / 0.5)
    return time
