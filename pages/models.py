from django.db import models
from django.contrib.auth.models import User , Group
from django.utils import timezone

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
    #id = models.IntegerField(unique=True, blank=False , null=True) 
   
    def __str__(self):
        return self.address.capitalize() 

class Totem(models.Model):
    identity_code = models.IntegerField(unique=True ,null=True,blank=False) # if this should be required
    secret_token  = models.CharField(max_length=64, null= True ,unique=True, blank=False)  # Unique token for each totem
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
        return self.user.username.capitalize()


class controler (models.Model):
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING, blank=False, null=True)
    badge_number = models.CharField(max_length=64, blank=False, null=True)
    group = models.ForeignKey(Group, on_delete=models.DO_NOTHING, blank=False, null=False)

    def __str__(self):
        return self.user.username.capitalize()


class Car(models.Model):
    plate_number = models.CharField(max_length=64, unique=True,blank=False, null=True)
    user = models.ForeignKey(User_developed,on_delete=models.DO_NOTHING, blank=True, null=True)
    def __str__(self):
        return self.plate_number.capitalize()  
    
class Ticket(models.Model):
    
    start_time = models.DateTimeField(auto_now_add=True,null=True)
    stop_time = models.DateTimeField(null=True)

    def is_active(self):
        now = timezone.now()
        return self.start_time and self.stop_time and self.start_time <= now < self.stop_time

    #totem = models.ForeignKey(Totem ,on_delete=models.DO_NOTHING, blank=False , null=True)
    car = models.ForeignKey(Car,on_delete=models.DO_NOTHING, blank=False, null=True)
    Parking = models.ForeignKey(Parking ,on_delete=models.DO_NOTHING, blank=False , null=True)
    #duration = models.IntegerField(blank=False, null=True)
    price = models.FloatField(blank=False, null=True)
    card_number = models.CharField(max_length=64, blank=False, null=True)
    id = models.AutoField(primary_key=True, null=False)  # Auto-incrementing primary key

    def __str__(self): 
        return f"Ticket #{self.id} - {str(self.Parking)} - {self.car} (start time : {self.start_time} - stop time : {self.stop_time})" 

class Chalk(models.Model):
   
    #maybe the car doesn't have user
    car = models.ForeignKey(Car,on_delete=models.DO_NOTHING, blank=False, null=True)
    issued_time = models.DateTimeField(auto_now_add=True,null=True)
    def __str__(self):
        return f"Chalk for {self.car} issued at {self.issued_time}"

class Fine(models.Model):
 
   #maybe the car doesn't have user (which obligatory should have codice fischale to apply the fine)
   car = models.ForeignKey(Car,on_delete=models.DO_NOTHING, blank=False, null=True)
   issued_time = models.DateTimeField(auto_now_add=True,null=True)
   def __str__(self):
         return f"Fine for {self.car} issued at {self.issued_time}"
class Card(models.Model):
    card_number = models.CharField(max_length=64, unique=True, blank=False , null=True)
    def __str__(self):
        return self.card_number.capitalize()