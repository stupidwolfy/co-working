from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Member(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    money = models.FloatField(max_length=20)

class Zone(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    price = models.FloatField(max_length=10)

class SeatBooking(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE)
    time_in = models.DateTimeField(auto_now_add=True)
    time_out = models.DateTimeField(auto_now=True)
    total_price = models.FloatField(max_length=10)
    create_date = models.DateField(auto_now_add=True)
    create_by = models.ForeignKey(User, on_delete=models.CASCADE)

class TopupLog(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    amount = models.FloatField(max_length=10)
    topup_date = models.DateField(auto_now=True)
    topup_by = models.ForeignKey(User, on_delete=models.CASCADE)