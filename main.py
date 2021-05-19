import datetime

from Entities.location import Location
from Entities.Enums.category import Category
from Entities.place import Place
from Entities.trip import Trip
from Entities.characteristics import Characteristic
from Entities.timetable import Timetable


accomodation = Place(
    name="Hotel",
    category=Category.accomodation,
    location=Location(35.8988, 14.5124),
    type=0,
)


characteristics = Characteristic(
    beach=1, museums=4, nature=1, clubbing=7, bar=2, shopping=8,
)

dateStart = datetime.datetime(2021, 5, 17)
dateFinal = datetime.datetime(2021, 5, 18)

trip = Trip(
    budget=3,
    moderation=3,
    characteristics=[characteristics],
    date=[dateStart, dateFinal],
    accomodation=accomodation,
)

trip.generate_itineraries()
