from django.core.management.base import BaseCommand,CommandError
from datetime import datetime
import os

class Command(BaseCommand):
    def handle(self, *args, **options):
        os.chdir('/home/donghai/project/Windseeker')
        now = datetime.today()
        s = str(now)
        print(s)
        with open('predictionmodel/management/commands/fts', 'a') as f:
            f.write(s + ':' + 'EL PSY CONGROO\n')
