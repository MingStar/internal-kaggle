# importing *, so that Flask can register the entities
from app.tasks import *
from app.models import *
from app.controllers import *

from app import app
from app import celery
