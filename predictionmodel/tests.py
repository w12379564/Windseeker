from django.test import TestCase
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Windseeker.settings")
django.setup()

from frontend.models import number
from predictionmodel.dataPreprocess import db2dataset
from predictionmodel.prediction import train,predict,check
import matplotlib.pyplot as plt
from math import sqrt
from sklearn.externals import joblib
from datetime import datetime,timedelta
import predictionmodel.getData
from predictionmodel.task import predictTask
# Create your tests here.

predictTask()