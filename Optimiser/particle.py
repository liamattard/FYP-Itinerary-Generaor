import numpy as np

from Entities.timetable import Timetable


class Particle:
    def __init__(self, timetable, is_Day):
        super().__init__()
        self.timetable = timetable
        if is_Day:
            self.position = timetable.days[0][0]
        else:
            self.position = timetable.days[0][1]

        self.personal_best_score = self.get_score(is_Day)
        self.personal_best_position = self.position
        self.velocity = np.zeros((self.position.shape), dtype=int)

    def get_score(self, is_Day):
        return Timetable.calculate_score(self.timetable, is_Day)

    def update_timetable(self, new_timetable):
        self.timetable.update_timetable(new_timetable)
        self.position = new_timetable
