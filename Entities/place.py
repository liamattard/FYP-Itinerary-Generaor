import json

from Entities.hours import Hours
from Entities.Enums.transport import Transport
from Entities.rating import Rating
from Entities.location import Location
from Entities.Enums.category import Category
from Entities.category_constant import Category_Constant
from Entities.Enums.price import Price
from os import listdir
from os.path import isfile, join


class Place:

    def __init__(self, name: str = None, hours: Hours = None,
                 price: Price = None, rating: Rating = None,
                 no_of_ratings: int = None, location: Location = None,
                 category: Category = None):

        super().__init__()
        self.name = name
        self.hours = hours
        self.price = price
        self.rating = rating
        self.no_of_ratings = no_of_ratings
        self.location = location
        self.category = category

    def get_time(self, trip):

        # number_of_ratings = self.no_of_ratings/max_ratings[self.category]

        userPref = trip.get_value_by_category(self.category)/100
        rating = (self.rating*20)/100

        time = userPref * rating * Category_Constant[self.category]
        time = 0.5 * round(float(time)/0.5)

        return time

    @staticmethod
    def get_places():

        all_places = []
        path = 'NearbySearch/POIs/'
        all_places = create_place(path, all_places, Category.point_of_interest)

        path = 'NearbySearch/beach/'
        all_places = create_place(path, all_places, Category.beach)

        path = 'NearbySearch/museums/'
        all_places = create_place(path, all_places,  Category.museums)

        path = 'NearbySearch/nature/'
        all_places = create_place(path, all_places, Category.nature)

        path = 'NearbySearch/night_clubs/'
        all_places = create_place(path, all_places, Category.club)

        path = 'NearbySearch/bars/'
        all_places = create_place(path, all_places, Category.bar)

        path = 'NearbySearch/restaurants/'
        all_places = create_place(path, all_places, Category.restaurant)

        path = 'NearbySearch/amusementParks/'
        all_places = create_place(path, all_places,  Category.amusement_park)

        path = 'NearbySearch/shopping/'
        all_places = create_place(path, all_places, Category.shopping)

        return all_places, max_ratings

    @staticmethod
    def get_distance(placeOne, placeTwo):
        return 1.0, Transport.car


max_ratings = {}
for i in Category:
    max_ratings[i] = 0


def create_place(path, all_places, category):

    results = [f for f in listdir(path) if isfile(join(path, f))]

    for i in results:

        f = open(path+i,)
        x = json.load(f)

        for i in x['results']:

            if 'rating' in i:

                name = i['name']
                rating = i['rating']
                no_of_ratings = i['user_ratings_total']
                price_level = None

                if 'price_level' in i:
                    price_level = i['price_level']

                all_places.append(Place(name=name,  price=price_level,
                                        rating=rating,
                                        no_of_ratings=no_of_ratings,
                                        category=category))

                if max_ratings[category] < no_of_ratings:
                    max_ratings[category] = no_of_ratings

    return all_places
