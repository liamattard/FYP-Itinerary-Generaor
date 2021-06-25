class Rating:
    def __init__(self, rating):
        super().__init__()

        if rating >= 5.0 and rating <= 0.0:
            print("ERROR Rating must be between 0 and 5")
        else:
            self.rating = rating
