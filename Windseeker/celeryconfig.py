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
    'writedb-every-30-second': {
        'task': 'predictionmodel.tasks.writedbtest',
        'schedule': timedelta(seconds=30)
    },
    'get-data-every-3:00-am':{
        'task': 'predictionmodel.tasks.getDataTask',
        'schedule': crontab(hour=19)
    },
    'train-every-7-days':{
        'task': 'predictionmodel.tasks.trainTask',
        'schedule': timedelta(days=7)
    },
    'predict-every-4:00-am':{
        'task': 'predictionmodel.tasks.predictTask',
        'schedule': crontab(hour=8,minute=5)
    }
}
