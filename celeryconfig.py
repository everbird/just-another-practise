from datetime import timedelta


BROKER_URL = 'redis://localhost:6379/1'
CELERY_RESULT_BACKEND = 'redis'
CELERYBEAT_SCHEDULE = {
    'check-merge': {
        'task': 'tasks.scheduler',
        'schedule': timedelta(seconds=15),
    },
    'check-complete': {
        'task': 'tasks.complete_selector',
        'schedule': timedelta(seconds=15),
    }
}
CELERY_IMPORTS = (
    'dispatcher',
    'to_export',
)
