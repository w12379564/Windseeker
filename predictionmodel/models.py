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

class Config(models.Model):
    id = models.IntegerField(primary_key=True)
    configname = models.CharField(max_length=20)

class RealTime_read(models.Model):
    config = models.OneToOneField(Config,on_delete=models.CASCADE)
    id = models.IntegerField(primary_key=True)
    value = models.FloatField()

class HistoryData(models.Model):
    time = models.DateTimeField()
    no = models.IntegerField()
    windspeed = models.FloatField()
    power = models.FloatField()
    class Meta:
        unique_together = ("time","no")


