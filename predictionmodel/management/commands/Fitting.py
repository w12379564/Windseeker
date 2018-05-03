from django.core.management.base import BaseCommand,CommandError
from predictionmodel.prediction import FittingCurve
import os

class Command(BaseCommand):
    def handle(self, *args, **options):
        os.chdir('/home/nanhui/project/Windseeker')
        FittingCurve()
