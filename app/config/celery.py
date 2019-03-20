from app.env import CELERY_BROKER_URL, CELERY_RESULT_BACKEND

from celery import Celery
from celery.task import Task

def make_celery(app):
    class ContextTask(Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery = Celery(
        app.import_name,
        backend=CELERY_RESULT_BACKEND,
        broker=CELERY_BROKER_URL,
        task_cls=ContextTask
    )
    celery.Task = ContextTask
    celery.conf.update(app.config)
    return celery
