class DayNight:

    def __init__(self, image: str):
        self.image: str = self.check_day_night(image)

    @classmethod
    def check_day_night(cls, img: str):
        if 'd' in img:
            return "День"
        return "Ночь"


