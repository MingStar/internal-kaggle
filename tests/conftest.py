import os
import tempfile

import pytest

from app.app import flask_app
from app.db_manager import db

@pytest.fixture
def client():
  db_fd, flask_app.config['DATABASE'] = tempfile.mkstemp()
  flask_app.config['TESTING'] = True
  client = flask_app.test_client()

  with flask_app.app_context():
    db.init_app(flask_app)

  yield client

  os.close(db_fd)
  os.unlink(flask_app.config['DATABASE'])
