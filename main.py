import datetime

from Entities.location import Location
from Entities.Enums.category import Category
from Entities.place import Place
from Entities.trip import Trip
from Entities.characteristics import Characteristic
from Entities.timetable import Timetable


def generateItineries(
    moderation,
    number_of_days,
    is_personalised,
    beach=None,
    clubbing=None,
    bars=None,
    nature=None,
    shopping=None,
    museums=None,
):

    accomodation = Place(
        name="Hotel",
        category=Category.accomodation,
        location=Location(35.8988, 14.5124),
        type=0,
    )

    characteristics = None

    if is_personalised:

        characteristics = Characteristic(
            beach=beach,
            museums=museums,
            nature=nature,
            clubbing=clubbing,
            bar=bars,
            shopping=shopping,
        )

    else:

        characteristics = Characteristic(
            beach=1, museums=1, nature=1, clubbing=1, bar=1, shopping=1,
        )

    trip = Trip(
        budget=3,
        moderation=moderation,
        characteristics=[characteristics],
        number_of_days=number_of_days,
        accomodation=accomodation,
        is_personalised=is_personalised,
    )

    Place.set_places(trip.characteristics[0])
    return trip.generate_itineraries()


# generateItineries(
# 3, 1, True, beach=9, clubbing=8, bars=8, nature=0, shopping=1, museums=0,
# )

generateItineries(1, 1, False)
