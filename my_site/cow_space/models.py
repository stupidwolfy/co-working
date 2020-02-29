from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Member(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    money = models.FloatField(max_length=20)

class Zone(models.Model):
    zone_type = (
        ('GR', 'Green Zone'),
        ('GO', 'Gold Zone'),
        ('PR', 'Private Zone')
    )

    title = models.CharField(max_length=50, choices=zone_type)
    description = models.CharField(max_length=200)
    price = models.FloatField(max_length=10)

class SeatBooking(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE)
    time_in = models.DateTimeField(auto_now_add=True)
    #time_out = models.DateTimeField(auto_now=True)
    time_out = models.DateTimeField(null = True)
    total_price = models.FloatField(max_length=10, null = True)
    create_date = models.DateField(auto_now_add=True)
    create_by = models.ForeignKey(User, on_delete=models.CASCADE)

class TopupLog(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    amount = models.FloatField(max_length=10)
    topup_date = models.DateTimeField(auto_now=True)
    topup_by = models.ForeignKey(User, on_delete=models.CASCADE)