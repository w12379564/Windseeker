from django.db import models

# Create your models here.
class weathertest(models.Model):
    time = models.DateTimeField(primary_key=True)
    temp = models.FloatField()
    hum = models.FloatField()
    press = models.FloatField()
    dir = models.CharField(max_length=50)
    windspeed = models.FloatField()
    condition = models.CharField(max_length=50)

class resulttest(models.Model):
    time = models.DateTimeField(primary_key=True)
    windspeed = models.FloatField()

class celerytest(models.Model):
    time = models.DateTimeField()

class HistoryDataTest(models.Model):
    time = models.DateTimeField(primary_key=True)
    no=models.IntegerField()
    power=models.FloatField()
    windspeed = models.FloatField()
    windspeed_30s = models.FloatField()
    windspeed_10m = models.FloatField()
    degree = models.FloatField()