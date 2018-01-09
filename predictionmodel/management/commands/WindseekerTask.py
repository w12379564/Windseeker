from django.core.management.base import BaseCommand,CommandError
from predictionmodel.tasks import WindseekerTasks
import os

class Command(BaseCommand):
    def handle(self, *args, **options):
        os.chdir('/home/chongming/project/Windseeker')
        WindseekerTasks()