import Optimiser.pso as pso

from Entities.Enums.budget import Budget
from Entities.place import Place


class Trip:
    """
    From this trip object a user will be able to generate itineraries
    that are applicable to his constraints. Constraints include:
    budget, moderation, characteristics, travel date and accomodation.
    """

    def __init__(
        self, budget: Budget, moderation, characteristics, date, accomodation: Place
    ):
        super().__init__()

        self.budget = budget
        self.moderation = moderation
        self.characteristics = characteristics
        self.date = date
        self.accomodation = accomodation

    def generate_itineraries(self):

        # pso.Optimise(self)
        pso.Optimise_classic(self)

        # return timetables
