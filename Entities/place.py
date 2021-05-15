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

day_id = 0
night_id = 0

day_places_by_id = {}
night_places_by_id = {}
places_of_category = {}

for i in Category:
    places_of_category[i] = []

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
        is_Day=None,
        is_accomodation=False,
    ):

        super().__init__()
        global day_id
        global night_id

        self.is_Day = is_Day
        self.name = name
        self.hours = hours
        self.price = price
        self.rating = rating
        self.no_of_ratings = no_of_ratings
        self.location = location
        self.category = category
        self.place_name = place_name

        if not is_accomodation:
            if is_Day:
                self.id = day_id
                day_places_by_id[id] = self
                day_id += 1
            else:
                self.id = night_id
                night_places_by_id[id] = self
                night_id += 1

        if time is not None:
            self.time = time

    def time_to(self, place_two):

        url = "http://127.0.0.1:5000/table/v1/driving/"
        url = url + str(self.location.y) + "," + str(self.location.x) + ";"
        url = url + str(place_two.location.y) + "," + str(place_two.location.x)
        duration = requests.get(url).json()
        if duration["durations"][0][1] is None:
            duration_time = 0
        else:
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
    def get_night_places(characteristics):

        all_places = []

        path = "NearbySearch/night_clubs/"
        all_places = create_place(
            path, all_places, Category.club, characteristics, is_Day=False
        )

        path = "NearbySearch/bars/"
        all_places = create_place(
            path, all_places, Category.bar, characteristics, is_Day=False
        )

    @staticmethod
    def get_day_places(characteristics):

        all_places = []

        path = "NearbySearch/beach/"
        all_places = create_place(
            path, all_places, Category.beach, characteristics, is_Day=True
        )

        path = "NearbySearch/museums/"
        all_places = create_place(
            path, all_places, Category.museums, characteristics, is_Day=True
        )

        path = "NearbySearch/nature/"
        all_places = create_place(
            path, all_places, Category.nature, characteristics, is_Day=True
        )

        path = "NearbySearch/shopping/"
        all_places = create_place(
            path, all_places, Category.shopping, characteristics, is_Day=True
        )

        return all_places

    @staticmethod
    def get_place_by_id(id):
        return day_places_by_id[id]

    @staticmethod
    def of_category(category):
        return places_of_category[category]


def create_place(path, all_places, category, characteristics: Characteristic, is_Day):

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
                else:
                    vicinity = ""

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
                    is_Day=is_Day,
                )

                all_places.append(new_place)
                places_of_category[category].append(new_place)

    return all_places


def calculate_time(characteristics, rating, category):
    userPref = characteristics.get_value_by_category(category)
    if userPref == None:
        userPref = 1
    else:
        userPref = userPref / 100

    rating = (rating * 20) / 100

    time = (userPref + rating) * Category_Constant[category]
    time = 0.5 * round(float(time) / 0.5)
    return time
