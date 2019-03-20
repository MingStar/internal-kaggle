from flask import Flask
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from app.config.sql_alchemy import db
from app.config.celery import make_celery
from app.config import view_filters
from app.env import SERVER_NAME

app = Flask("internal_kaggle",
            template_folder="app/templates",
            static_url_path="")
if SERVER_NAME:
  app.config['SERVER_NAME'] = SERVER_NAME

db.init_app(app)
migrate = Migrate(app, db)
Bootstrap(app)
celery = make_celery(app)
view_filters.init_app(app)
