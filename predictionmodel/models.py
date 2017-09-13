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
    y_predict = models.FloatField()