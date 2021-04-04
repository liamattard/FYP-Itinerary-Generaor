import numpy as np

from Entities.timetable import Timetable


class Particle():
    def __init__(self, timetable):
        super().__init__()
        self.timetable = timetable
        self.position = timetable.timetable
        self.personal_best_score = self.get_score()
        self.personal_best_position = self.position
        self.velocity = np.zeros((self.position.shape), dtype=int)

    def get_score(self):
        return Timetable.calculate_score(self.timetable)

    def update_timetable(self, new_timetable):
        self.timetable.update_timetable(new_timetable)
        self.position = new_timetable
