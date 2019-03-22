import os
import docker
import logging
from app.background.docker_runner import DockerRunner
from app.background.enum import EvaluationMode
from app.env import HOST_WORKSPACE_PATH, WORKSPACE_PATH

logger = logging.getLogger(__file__)

def ensure_path(path):
  logger.info("Creating path: %s", path)
  os.makedirs(path, exist_ok=True)
  logger.info("Created path: %s", path)

class KaggleDockerRunner:
  def __init__(self, options, task_id):
    self.options = options
    self.competition_code = options['competition']
    self.task_id = task_id
    self.output_path = self._get_output_path()

  def run(self, mode):
    ensure_path(self.output_path)
    docker_runner = DockerRunner(self.options["docker_image_name"],
                                 self.options["docker_image_tag"]
                                 )
    result = docker_runner.run_container(
      command=["./entrypoint.sh", self.competition_code, "/input", "/output"],
      volume_mounts=self._get_mounts(mode)
    )
    result['output_path'] = self.output_path
    return result

  def _get_output_path(self, base_path=WORKSPACE_PATH):
    return f"{base_path}/run/{self.task_id}"

  def get_competition_base_path(self):
    return f"{HOST_WORKSPACE_PATH}/competitions/{self.competition_code}"

  def _get_mounts(self, mode):
    if mode == EvaluationMode.test:
      input_path = 'test'
    else:
      input_path = 'training'
    input = docker.types.Mount(
      '/input',
      self.get_competition_base_path() + "/input/" + input_path,
      type='bind',
      read_only=True
    )
    output = docker.types.Mount(
      '/output',
      self._get_output_path(HOST_WORKSPACE_PATH), # <- need host path for mounting
      type='bind'
    )
    return [ input, output ]
