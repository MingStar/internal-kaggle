import logging
from flask import request, render_template, redirect
import celery.states as states

from app import celery
from app.env import SITE_NAME, GET_STARTED_URL
from app.view_models import *
from app import app, repository

logger = logging.getLogger(__name__)

@app.route('/')
def index():
    evals = [EvaluationViewModel(item) for item in repository.get_recent_evaluations(10)]
    return render_template('index.html', recent_evals=evals, site_name=SITE_NAME)

@app.route('/competitions')
def competitions():
    competitions = [
        CompetitionViewModel(item) for item in repository.get_active_competitions()]
    return render_template('competitions/index.html', model=competitions)

@app.route('/competitions/<int:id>')
def competition(id):
    competition = CompetitionViewModel(repository.get_competition(id))
    return render_template('competitions/show.html', comp=competition)

@app.route('/get_started')
def get_started():
    if GET_STARTED_URL:
        return redirect(GET_STARTED_URL, code=302)
    else:
        return render_template('get_started.html')


def validate_options(options):
  #TODO: for invalid options, throw exceptions
  pass

# {
#     "competition": "iris",
#     "team": "test",
#     "docker_image_name": "user/image",
#     "docker_image_tag": "latest"
# }
@app.route('/submit', methods=["POST"])
def submit():
    data = request.get_json()
    validate_options(data)
    task = celery.send_task('tasks.submit', args=[data])
    return get_response(task)

def get_response(task):
    return f"<a href='{url_for('check_task', task_id=task.id, external=True)}'>check status of {task.id} </a>"

@app.route('/tasks/<string:task_id>')
def check_task(task_id: str) -> str:
    res = celery.AsyncResult(task_id)
    if res.state == states.PENDING:
        return res.state
    else:
        return str(res.result)
