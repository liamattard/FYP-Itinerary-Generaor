
import numpy as np

from Entities.place import Place


class Timetable():

    def __init__(self, random_timetable, moderation):

        timetable = np.zeros(
            (len(random_timetable), 2+(2 * (moderation + 2))), dtype=int)

        for i, day in enumerate(random_timetable):

            timetable[i][1:len(day[0])+1] = day[0]
            timetable[i][-(len(day[1])+1):-1] = day[1]

        self.timetable = timetable

    def __str__(self):
        string = ""
        for i, day in enumerate(self.timetable):
            string = string + "Day " + str(i + 1) + "\n"
            string = string + "---------\n"

            for place in day[:-1]:
                string = string + Place.get_place_by_id(place).name
                string = string + " -> "
            string = string + Place.get_place_by_id(day[-1]).name
            string = string + "\n --------- \n"

        return string
