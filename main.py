import datetime

from Entities.timetable import Timetable
from Entities.Enums.category import Category
from Entities.place import Place
from Entities.trip import Trip
from Entities.trip import Characteristic

# Getting all places
all_places, max_ratings = Place.get_places()


# Defining a new trip

accomodation = Place(name="Sample Hotel", category=Category.accomodation)

character_one = Characteristic(point_of_interests=80,
                               beach=80,
                               museums=100,
                               nature=40,
                               clubbing=10,
                               bar=60,
                               food=50,
                               amusement_parks=100,
                               shopping=30)

dateStart = datetime.datetime(2021, 5, 17)
dateFinal = datetime.datetime(2021, 5, 27)
tripOne = Trip(3, 3, [character_one], [dateStart, dateFinal])


# Calculate the time spent at each event
for i in all_places:

    time = i.get_time(tripOne)
    print(time, "hrs at ", i.name)

# Calculate distance between two places
distance, transport = Place.get_distance(all_places[0], all_places[1])
print("Distance between", all_places[0].name, "and",
      all_places[1].name, " is: ", distance, "hr by ", transport.name)


# Creating a new itinerary
timetable = Timetable([dateStart, dateFinal], accomodation)
