from app import celery
from app.background.evaluation_runner import EvaluationRunner

@celery.task(bind=True, name='tasks.submit')
def submit(self, data):
  runner = EvaluationRunner()
  return runner.run(data, self.request.id)
