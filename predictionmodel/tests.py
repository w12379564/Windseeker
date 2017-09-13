from django.test import TestCase
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Windseeker.settings")
django.setup()

from frontend.models import number
from predictionmodel.dataPreprocess import db2dataset
# Create your tests here.
data = db2dataset(48,1)


print(data)