import datetime

from Entities.location import Location
from Entities.Enums.category import Category
from Entities.place import Place
from Entities.trip import Trip
from Entities.characteristics import Characteristic


accomodation = Place(
    name="Sample Hotel", category=Category.accomodation,
    location=Location(35.9543, 14.4184))


characteristics = Characteristic(point_of_interests=70,
                                 beach=90,
                                 museums=40,
                                 nature=60,
                                 clubbing=80,
                                 bar=60,
                                 food=100,
                                 amusement_parks=40,
                                 shopping=90)

dateStart = datetime.datetime(2021, 5, 17)
dateFinal = datetime.datetime(2021, 5, 27)

trip_one = Trip(3, 3, [characteristics], [dateStart, dateFinal], accomodation)

trip_one.generate_itineraries()
