import os

def str2bool(v):
    if v is None:
        return False
    return v.lower() in ("yes", "true", "t", "1")

def get_db_uri():
  return 'postgres://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}'.format(**os.environ)

CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL'),
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND')
FLOWER_BASE_URL = os.getenv('FLOWER_BASE_URL')
SLACK_WEB_HOOK_URL = os.getenv('SLACK_WEB_HOOK_URL')
SERVER_NAME = os.getenv('SERVER_NAME')

DOCKER_REGISTRY = os.getenv('DOCKER_REGISTRY', '')
HOST_WORKSPACE_PATH = os.getenv('HOST_WORKSPACE_PATH', '/data')

WORKSPACE_PATH = '/workspace'
