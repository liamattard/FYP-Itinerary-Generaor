from Entities.Enums.category import Category


class Category_value:
    def __init__(self, value: int, category: Category):
        self.category = category
        self.value = value


class Characteristic:
    def __init__(
        self,
        beach=None,
        museums=None,
        nature=None,
        clubbing=None,
        bar=None,
        shopping=None,
    ):

        super().__init__()

        day_categories = [beach, museums, nature, shopping]
        night_categories = [clubbing, bar]

        normalised_day = []
        normalised_night = []

        for i in day_categories:
            normalised_day.append((i / sum(day_categories)) * 100)

        for i in night_categories:
            normalised_night.append((i / sum(night_categories)) * 100)

        self.beach = Category_value(normalised_day[0], Category.beach)
        self.museums = Category_value(normalised_day[1], Category.museums)
        self.nature = Category_value(normalised_day[2], Category.nature)
        self.shopping = Category_value(normalised_day[3], Category.shopping)

        self.clubbing = Category_value(normalised_night[0], Category.club)
        self.bar = Category_value(normalised_night[1], Category.bar)

    def get_value_by_category(self, category):
        """
        Returns the characteristic value from a category.

        Parameters
        ----------
        category (Category)

        Returns
        -------
        value (int): Representing the value characteristic value of a
        user.

        """
        for i in self.get_attributes():
            if i.category == category:
                return i.value

    def __str__(self):
        print_str = ""
        for i in self.get_attributes():
            print_str += str(i.category)
            print_str += ": "
            print_str += str(i.value)
            print_str += "\n"

        return print_str

    def get_attributes(self):
        """
        Returns a list of all characteristics.
        Returns
        -------
        list of categories.
        """
        return [
            self.beach,
            self.museums,
            self.nature,
            self.shopping,
            self.clubbing,
            self.bar,
        ]
