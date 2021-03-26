from enum import Enum


class Timetable():
    def __init__(self, date, accomodation):
        super().__init__()
        # TODO: include months
        number_of_days = date[1].day - date[0].day
        days = [day] * number_of_days
        print(days)

    def add_place(self, place, day):
        print("Yo")


class day():
    def __init__(self):
        super().__init__()
        # Set Max 24 hrs
        #  Add Accomodation time
        self.slots = []


class slot():
    def __init__(self, slot_type, place):
        super().__init__()


class slot_type(Enum):
    accomodation = 0
    place = 1
    travel_time = 2
