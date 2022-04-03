from django.db import models
import datetime


# Create your models here.

class User(models.Model):
    first_name = models.CharField(max_length=55, default="")
    last_name = models.CharField(max_length=55, default="")
    email = models.EmailField(max_length=100, default="")
    phone = models.CharField(max_length=15, default="")
    password = models.CharField(max_length=15, default="")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def isExists(self):
        if User.objects.filter(email=self.email):
            return True
        return False

    @staticmethod
    def get_customer_by_email(email):
        try:
            return User.objects.get(email=email)
        except:
            return False


# Bus Table
class Bus(models.Model):
    bus_Name = models.CharField(max_length=50)
    source = models.CharField(max_length=75)
    destination = models.CharField(max_length=75)
    Nos = models.IntegerField()
    rem = models.IntegerField()
    price = models.IntegerField()
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return self.bus_Name


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Bus_Name = models.CharField(max_length=50)
    No_Seats = models.IntegerField()
    Contact = models.CharField(max_length=15)
    From = models.CharField(max_length=50)
    To = models.CharField(max_length=50)
    Price_Per_Ticket = models.IntegerField()
    Cost = models.IntegerField()
    T_date = models.CharField(max_length=15)
    T_time = models.CharField(max_length=15)
    booking_Date = models.DateTimeField(default=datetime.datetime.today)

    def __str__(self):
        return str(self.user)

    @staticmethod
    def get_orders_by_customer(customer_id):
        return Booking.objects.filter(user=customer_id).order_by('-booking_Date')
