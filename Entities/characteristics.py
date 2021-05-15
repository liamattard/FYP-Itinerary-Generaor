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

        categories = [beach, museums, nature, clubbing, bar, shopping]
        normalised_categories = []
        for i in categories:
            normalised_categories.append((i/sum(categories)) * 100)

        self.beach = Category_value(normalised_categories[0], Category.beach)
        self.museums = Category_value(
            normalised_categories[1], Category.museums)
        self.nature = Category_value(normalised_categories[2], Category.nature)
        self.clubbing = Category_value(normalised_categories[3], Category.club)
        self.bar = Category_value(normalised_categories[4], Category.bar)
        self.shopping = Category_value(
            normalised_categories[5], Category.shopping)

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
            print_str +=  ": "
            print_str += str(i.value)
            print_str += ("\n")

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
