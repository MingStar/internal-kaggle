from app.models import *
from app import repository
from flask import url_for
from app.env import FLOWER_BASE_URL

IMAGE_NOT_FOUND = 'https://user-images.githubusercontent.com/24848110/33519396-7e56363c-d79d-11e7-969b-09782f5ccbab.png'

class ViewModel:
  def __init__(self, model):
    self.model = model

  def __getattr__(self, attr_name):
    return getattr(self.model, attr_name)

class CompetitionViewModel(ViewModel):
  def __init__(self, model:Competition):
    super(CompetitionViewModel, self).__init__(model)

  @property
  def description(self):
    return self.model.description.trim()

  @property
  def image_url(self):
    return self.model.image_url or IMAGE_NOT_FOUND

  @property
  def url(self):
    return url_for('competition', id=self.id)

  @property
  def short_description(self, length=150):
    if len(self.model.description) <= length:
      return self.model.description
    # else
    return self.model.description[:150] + " ..."

  @property
  def leaderboard(self):
    return [ EvaluationViewModel(item) for item in repository.get_leaderboard(self.model) ]


class EvaluationViewModel(ViewModel):
  def __init__(self, model:Evaluation):
    super(EvaluationViewModel, self).__init__(model)
    self.competition = CompetitionViewModel(self.model.competition)

  @property
  def final_score_str(self):
    return "%.2f" % self.model.final_score

  @property
  def task_url(self):
    return FLOWER_BASE_URL + "/task/" + self.model.task_id
