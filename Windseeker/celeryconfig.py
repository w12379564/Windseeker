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
    'predict_15min': {
        'task': 'predictionmodel.tasks.Predict',
        'schedule': crontab(minute='*/15')
    },
    'get_data_15min': {
        'task': 'predictionmodel.tasks.GetData',
        'schedule': crontab(minute='*/15')
    },
    'Calc_Expect_value_15min': {
        'task': 'predictionmodel.tasks.CalcExpectValue',
        'schedule': crontab(minute='*/15')
    },
    'Write_WindTower_value_15min': {
        'task': 'predictionmodel.tasks.WriteWindTowerInfo',
        'schedule': crontab(minute='*/15')
    }
}
