from datetime import datetime,timedelta
from celery.schedules import crontab

# Broker and Backend
BROKER_URL = 'redis://127.0.0.1:6379'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'


# Timezone
CELERY_TIMEZONE='Asia/Shanghai'

# import
CELERY_IMPORTS = (
    'predictionmodel.tasks',
)

# schedules
CELERYBEAT_SCHEDULE = {
    'add-every-30-seconds': {
         'task': 'predictionmodel.tasks.add',
         'schedule': crontab(hour=15, minute=31),
         'args': (5, 8)
    },
}
