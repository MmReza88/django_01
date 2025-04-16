from django.db import models
from django.contrib.auth.models import User

class Service_provider (models.Model):  #Admin define => totem can get variables by totem
    name = models.CharField(max_length=64, unique=True, blank=False)
    
    def __str__(self):
      return self.name.capitalize()

class City (models.Model):              #Service provider define => totem can get variables by totem
    name = models.CharField( unique=True ,max_length=64, blank=False)
    def __str__(self):
      return self.name.capitalize()

class Zone (models.Model):
    
    name = models.CharField (unique=True ,max_length=64, blank=False)
   
    city = models.ForeignKey(City ,on_delete=models.DO_NOTHING, blank=False , null=True)
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


class Parking (models.Model):
    
    address= models.CharField(max_length=64, unique=True, blank=False)
    zone = models.ForeignKey(Zone ,on_delete=models.DO_NOTHING, blank=False , null=True)
    
    def __str__(self):
        return self.address.capitalize() 

class Totem(models.Model):
    identity_code = models.IntegerField(unique=True ,null=True,blank=False) # if this should be required
    parking = models.ForeignKey(
        Parking, 
        on_delete=models.PROTECT,  # Better than DO_NOTHING
        blank=False,
        null=True  # Don't allow null if every totem must belong to a parking
    )
    
    def __str__(self):
        return f"Totem {self.identity_code}"


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
    
    start_time = models.DateTimeField(auto_now_add=True,null=True)
    
    totem = models.ForeignKey(Totem ,on_delete=models.DO_NOTHING, blank=False , null=True)
    
    car = models.ForeignKey(Car,on_delete=models.DO_NOTHING, blank=False, null=True)
 
    duration = models.IntegerField(blank=False, null=True)
    price = models.IntegerField(blank=False, null=True)
    payment_done = models.BooleanField(default=False)
    def __str__(self): 
        return f"Ticket #{str(self.totem.identity_code)} - {self.car} (Duration: {self.duration} mins)" 

class Chalk(models.Model):
   
    #user is controler
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING, blank=False, null=True)
    #maybe the car doesn't have user
    car = models.ForeignKey(Car,on_delete=models.DO_NOTHING, blank=False, null=True)
    issued_time = models.DateTimeField(auto_now_add=True,null=True)


class Fine(models.Model):
 
   #user is controler
   user = models.ForeignKey(User,on_delete=models.DO_NOTHING, blank=False, null=True)
   #maybe the car doesn't have user (which obligatory should have codice fischale to apply the fine)
   car = models.ForeignKey(Car,on_delete=models.DO_NOTHING, blank=False, null=True)
   issued_time = models.DateTimeField(auto_now_add=True,null=True)
