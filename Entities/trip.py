from Entities.Enums.category import Category


class Category_value:
    def __init__(self, value: int, category: Category):
        self.category = category
        self.value = value


class Characteristic:
    def __init__(
        self,
        point_of_interests=None,
        beach=None,
        museums=None,
        nature=None,
        clubbing=None,
        bar=None,
        food=None,
        amusement_parks=None,
        shopping=None,
    ):

        super().__init__()

        self.point_of_interests = Category_value(
            point_of_interests, Category.point_of_interest
        )
        self.beach = Category_value(beach, Category.beach)
        self.museums = Category_value(museums, Category.museums)
        self.nature = Category_value(nature, Category.nature)
        self.clubbing = Category_value(clubbing, Category.club)
        self.bar = Category_value(bar, Category.bar)
        self.food = Category_value(food, Category.restaurant)
        self.amusement_parks = Category_value(amusement_parks,
                                              Category.amusement_park)
        self.shopping = Category_value(shopping, Category.shopping)

    def get_attributes(self):
        return [
            self.point_of_interests,
            self.beach,
            self.museums,
            self.nature,
            self.clubbing,
            self.bar,
            self.food,
            self.amusement_parks,
            self.shopping,
        ]


class Trip:
    def __init__(self, budget, moderation, characteristics, date):
        super().__init__()

        self.budget = budget
        self.moderation = moderation
        self.characteristics = characteristics
        self.date = date

    def get_value_by_category(self, category):
        for i in self.characteristics[0].get_attributes():
            if i.category == category:
                return i.value
