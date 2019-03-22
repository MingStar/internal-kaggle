import importlib
import logging

from app.background.kaggle_docker_runner import KaggleDockerRunner
from app.background.slack_notifier import SlackNotifier
from app.background.enum import EvaluationMode
from app.models import Evaluation
from app.config.sql_alchemy import db
from app.repository import get_competition_by
from app.env import WORKSPACE_PATH
from app.view_models import EvaluationViewModel

logger = logging.getLogger(__file__)

def _load_judge_file(filename):
  spec = importlib.util.spec_from_file_location("judge", filename)
  module = importlib.util.module_from_spec(spec)
  spec.loader.exec_module(module)
  return module

class EvaluationRunner:
  def __init__(self, mode=EvaluationMode.training):
    self.mode = mode

  def run(self, options, task_id, is_training = True):
    try:
      return self._run(options, task_id, is_training)
    except Exception as e:
      self._notify(options, e)
      raise

  def _run(self, options, task_id, is_training):
    self.competition_code = options['competition']
    competition = get_competition_by(self.competition_code)
    run_stats = self._run_docker(options, task_id)
    judge_result = self._judge(run_stats["output_path"], is_training)
    evaluation = self._save(options, competition, run_stats, judge_result, task_id)
    self._notify(EvaluationViewModel(evaluation))
    return judge_result

  def _run_docker(self, options, task_id):
    docker = KaggleDockerRunner(options, task_id)
    return docker.run(self.mode)

  def _get_competition_path(self):
    return f"{WORKSPACE_PATH}/competitions/{self.competition_code}"

  def _judge(self, output_path, is_training):
    base_path = self._get_competition_path()
    judge_filename = base_path + "/judge.py"
    judge = _load_judge_file(judge_filename).judge
    result = judge(is_training, base_path, output_path)
    logger.info("Judge result:")
    logger.info(result)
    return result

  def _notify(self, *args):
    SlackNotifier().notify_result(*args)

  def _save(self, options, competition, run_stats, judge_result, task_id):
    new = Evaluation(
      competition_id=competition.id,
      team_name=options['team'],
      task_id=task_id,
      docker_image_name=options['docker_image_name'],
      docker_image_tag=options['docker_image_tag'],
      docker_image_hash=run_stats['docker_image_id'],
      docker_image_size=run_stats['docker_image_size'],
      duration=run_stats['container_run_time'],
      test_scores=judge_result,
      final_score=judge_result
    )
    db.session.add(new)
    db.session.commit()
    return new

