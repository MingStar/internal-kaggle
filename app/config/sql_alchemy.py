from datetime import datetime

from sqlalchemy import Column, DateTime, Integer
import flask_sqlalchemy
import sqlalchemy_jsonfield

from app.env import get_db_uri

class AnnaSQLAlchemy(flask_sqlalchemy.SQLAlchemy):
  def apply_driver_hacks(self, app, info, options):
      options.update({
          # Needed because Azure kills idle connections
          'pool_pre_ping': True
      })
      super(AnnaSQLAlchemy, self).apply_driver_hacks(app, info, options)

  def init_app(self, app):
    app.config['SQLALCHEMY_DATABASE_URI'] = get_db_uri()
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    super(AnnaSQLAlchemy, self).init_app(app)

db = AnnaSQLAlchemy()

def get_current_time():
  time_format = "%Y-%m-%d %H:%M:%S"
  time_now = datetime.now()
  return time_now.strftime(time_format)

class BaseModel(db.Model):
  __abstract__ = True
  id = Column(Integer, primary_key=True, autoincrement=True)
  created_at = Column(DateTime, nullable=False, default=db.func.now())
  updated_at = Column(DateTime, nullable=False, default=db.func.now(), onupdate=db.func.now())


JsonField = sqlalchemy_jsonfield.JSONField()
