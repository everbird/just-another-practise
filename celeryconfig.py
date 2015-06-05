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
    },
    'merge': {
        'task': 'tasks.start_merge_workers',
        'schedule': timedelta(seconds=60),
    },
    'export': {
        'task': 'tasks.start_export_workers',
        'schedule': timedelta(seconds=60),
    },
}
CELERY_IMPORTS = (
    'tasks',
    'tasks.dispatcher',
    'tasks.complete_selector',
    'tasks.merge',
    'tasks.export',
)
