from django.db import models
from django.contrib.auth.models import User

class Service_provider (models.Model):  #Admin define => totem can get variables by totem
    name = models.CharField(max_length=64, unique=True, blank=False)
    
    def __str__(self):
      return self.name.capitalize()

class City (models.Model):              #Service provider define => totem can get variables by totem
    name = models.CharField(max_length=64, blank=False)
    service_provider = models.ForeignKey(Service_provider ,on_delete=models.DO_NOTHING, blank=False , null=True) 

    durations = models.CharField(max_length=255, blank=False)
    prices = models.CharField(max_length=255, blank=False)
    
    def __str__(self):
      return self.name.capitalize()


    def get_durations(self):
        return [int(x) for x in self.durations.split(",")] if self.durations else []
    
    def get_prices(self):
        print(self.prices.split(","))
        return [int(x) for x in self.prices.split(",")] if self.prices else []



class Totem(models.Model):
   
    location_address = models.CharField(max_length=64, unique=True, blank=False , null=True)
    city = models.ForeignKey(City ,on_delete=models.DO_NOTHING, blank=False , null=True)
    service_provider = models.ForeignKey(Service_provider ,on_delete=models.DO_NOTHING, blank=False , null=True) 
    def __str__(self):
      return self.location_address.capitalize()

#-------------------------------------------------------------------------------------------------------------------

class User_developed (models.Model):
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING, blank=False, null=True)
    codice_fiscale = models.CharField(max_length=64)
   
    def __str__(self):
        return self.codice_fiscale.capitalize() 

    
class Car(models.Model):
    plate_number = models.CharField(max_length=64, unique=True,blank=False, null=True)
    user = models.ForeignKey(User_developed,on_delete=models.DO_NOTHING, blank=True, null=True)
    def __str__(self):
        return self.plate_number.capitalize()  
    
class Ticket(models.Model):
    start_time = models.DateTimeField(auto_now_add=True)
 
    location_address = models.CharField(max_length=64, unique=True, blank=False , null=True)
    city =  models.CharField(max_length=64, unique=True, blank=False , null=True)
    service_provider =  models.CharField(max_length=64, unique=True, blank=False , null=True) 

    car = models.ForeignKey(Car,on_delete=models.DO_NOTHING, blank=False, null=True)
    
    duration = models.IntegerField(blank=False, null=True)
    price = models.IntegerField(blank=False, null=True)


class Fine(models.Model):
    plate_number = models.CharField(max_length=64, unique=True,blank=False, null=True)
    issued_time = models.DateTimeField(auto_now_add=True)

class Chalk(models.Model):
    plate_number = models.CharField(max_length=64, unique=True,blank=False, null=True)
    issued_time = models.DateTimeField(auto_now_add=True)
