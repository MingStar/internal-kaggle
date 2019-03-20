from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import String, Integer, DECIMAL, Boolean

from app.config.sql_alchemy import BaseModel, JsonField

class Competition(BaseModel):
  name = Column(String, nullable=False)
  code = Column(String(20), nullable=False)
  image_url = Column(String)
  description = Column(String)
  training_data_url = Column(String, nullable=False)
  validation_data_url = Column(String)
  validation_script_url = Column(String)
  is_active = Column(Boolean, default=True, nullable=False)
  evaluations = relationship("Evaluation", backref="competition", lazy='dynamic')

class Evaluation(BaseModel):
  competition_id = Column(Integer, ForeignKey("competition.id"), nullable=False)
  team_name = Column(String(128), nullable=False)
  task_id = Column(String(128), nullable=False)
  docker_image_name = Column(String)
  docker_image_tag = Column(String)
  docker_image_hash = Column(String)
  docker_image_size = Column(Integer)
  test_scores = Column(JsonField)
  final_score = Column(DECIMAL)
  duration = Column(DECIMAL)
