from django.db import models
from django.contrib.auth.models import User



class Parking(models.Model):
    name = models.CharField(max_length=64, unique=True, blank=False)
    location_address = models.CharField(max_length=64, unique=True, blank=False)

   #   def __str__(self):
   #   return self.name.capitalize()


class Totem(models.Model):
    parking = models.ForeignKey(Parking, on_delete=models.DO_NOTHING, blank=False, null=True)
    durations = models.CharField(max_length=255, blank=False)
    prices = models.CharField(max_length=255, blank=False)
    

    def get_durations(self):
        return [int(x) for x in self.durations.split(",")] if self.durations else []
    
    def get_prices(self):
        print(self.prices.split(","))
        return [int(x) for x in self.prices.split(",")] if self.prices else []
    
    def __str__(self):
        return f"Totem [{self.id}] {self.parking}"


class User_developed (models.Model):
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING, blank=False, null=True)
    codice_fiscale = models.CharField(max_length=64)
   
    def __str__(self):
        return f"User extension with Codice Fiscale: {self.codice_fiscale}" 

    
class Car(models.Model):
    plate_number = models.CharField(max_length=64, unique=True,blank=False, null=True)
    user = models.ForeignKey(User_developed,on_delete=models.DO_NOTHING, blank=True, null=True)

class Ticket(models.Model):
    start_time = models.DateTimeField(auto_now_add=True)
    totem = models.ForeignKey(Totem, on_delete=models.DO_NOTHING, blank=False, null=True)
    car = models.ForeignKey(Car,on_delete=models.DO_NOTHING, blank=False, null=True)
    
    duration = models.IntegerField(blank=False, null=True)
    price = models.IntegerField(blank=False, null=True)


class Fine(models.Model):
    car = models.ForeignKey(Car,on_delete=models.DO_NOTHING, blank=False, null=True)
    issued_time = models.DateTimeField(auto_now_add=True)

class Chalk(models.Model):
    car = models.ForeignKey(Car,on_delete=models.DO_NOTHING, blank=False, null=True)
    issued_time = models.DateTimeField(auto_now_add=True)
    parking = models.ForeignKey(Parking, on_delete=models.DO_NOTHING, blank=False, null=True)
