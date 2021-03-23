from enum import Enum


class Timetable():
    def __init__(self, date, accomodation):
        super().__init__()

    def add_place(self, place):
        print("Yo")


class day():
    def __init__(self):
        super().__init__()
        self.slots = []


class slot():
    def __init__(self, slot_type, place):
        super().__init__()


class slot_type(Enum):
    accomodation = 0
    place = 1
    travel_time = 2
