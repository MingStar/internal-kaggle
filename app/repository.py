from sqlalchemy import desc
from app.config.sql_alchemy import db
from app.models import *

def get_competition_by(code):
  return db.session.query(Competition).filter_by(code=code).first()

def get_competition(id):
  return db.session.query(Competition).get(id)

def get_active_competitions():
  return db.session.query(Competition).filter_by(is_active=True)

def get_recent_evaluations(num:int):
  return db.session.query(Evaluation)\
    .order_by(desc(Evaluation.created_at))\
    .limit(num).all()

def get_leaderboard(competition, num:int=10):
  return competition.evaluations.order_by(desc(Evaluation.final_score)).limit(num)
