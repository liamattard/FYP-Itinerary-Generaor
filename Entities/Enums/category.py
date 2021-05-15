from enum import Enum


class Category(Enum):

    accomodation = 0
    beach = 2
    museums = 3
    nature = 4
    shopping = 6
    cafe = 7
    club = 8
    bar = 9
    restaurant = 10

    @staticmethod
    def get_categories_time():
        x = [[Category.beach, 0]]
        x.append([Category.museums, 0])
        x.append([Category.nature, 0])
        x.append([Category.shopping, 0])
        x.append([Category.club, 1])
        x.append([Category.bar, 1])
        return x
