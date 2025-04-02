from django.db import models



class Parking(models.Model):
    name = models.CharField(max_length=64, unique=True, blank=False)
    location_address = models.CharField(max_length=64, unique=True, blank=True)

    def __str__(self):
        return self.name.capitalize()


class Totem(models.Model):
    parking = models.ForeignKey(Parking, on_delete=models.DO_NOTHING, blank=False, null=True)
    durations = models.CharField(max_length=255, blank=True)
    prices = models.CharField(max_length=255, blank=True)
    

    def get_durations(self):
        return [int(x) for x in self.durations.split(",")] if self.durations else []
    
    def get_prices(self):
        print(self.prices.split(","))
        return [int(x) for x in self.prices.split(",")] if self.prices else []
    
    def __str__(self):
        return f"Totem [{self.id}] {self.parking}"
    