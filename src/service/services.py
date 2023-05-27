import random
from service import models


class TruckService:
    __tuuck_model = models.Truck
    __location_model = models.Location

    @classmethod
    def set_random_location(cls, self):
        all_locations = cls.__location_model.objects.filter(is_deleted=False)
        random_location = random.choice(all_locations)
        self.curr_location = random_location
