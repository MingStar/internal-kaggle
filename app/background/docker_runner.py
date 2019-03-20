import docker
import logging
import time
import socket

import contextlib
from docker.errors import ImageNotFound

from app.env import DOCKER_REGISTRY

logger = logging.getLogger(__name__)

class DockerRunner:

  def __init__(self, image_name, image_tag):
    self.image_name = image_name
    self.image_tag = image_tag
    self.client = docker.from_env()

  def _get_image(self):
    image_name = "%s%s:%s" % (DOCKER_REGISTRY, self.image_name, self.image_tag)
    try:
      logger.info("Getting image %s", image_name)
      img = self.client.images.get(image_name)
      logger.info("Got image %s, id: %s", image_name, img.short_id)
    except ImageNotFound:
      logger.info("Image not found: pulling image %s", image_name)
      img = self.client.images.pull(image_name)
    return img

  def run_container(self,
                    command,
                    volume_mounts=None,
                    container_complete_callback=None,
                    container_failed_callback=None
                    ):
    try:
      image = self._get_image()
      mounts = volume_mounts
      self._log_container_run_info(command, mounts)

      start = time.time()
      with self._auto_close(
          self.client.containers.run(
            image,
            mounts=mounts,
            command=command,
            detach=True,
            remove=False,  # need to get the container status after it finishes
          )
      ) as container:
        logger.info("Container name: %s", container.name)
        self._container_running(container)
        status = container.wait()
        end = time.time()
        total_run_time = end - start
        logger.info("Total runtime: %d seconds" % int(total_run_time))
        if status['StatusCode'] != 0:
          logger.info(status['Error'])
          raise Exception(
            "Non-Zero Status Code returned: %d\n" % status['StatusCode'] +
            "Detail logs: \n" +
            "\n".join(self.logs)
          )
        if container_complete_callback:
          container_complete_callback(status, total_run_time)
        return {
          'container_run_time': total_run_time,
          'docker_image_size': image.attrs['Size'],
          'docker_image_id': image.short_id
        }
    except Exception as e:
      logger.exception('Error running container')
      if container_failed_callback:
        container_failed_callback(e)
      raise

  def _log_container_run_info(self, command, mounts):
    logger.info("Running container:")
    # Log host
    logger.info("on host: %s", socket.gethostname())
    # Log command
    command_str = ' '.join(command)
    logger.info("with command: %s", command_str)
    # Log volume mounts
    if mounts:
      logger.info("With mounts:")
      for mount in mounts:
        logger.info(mount)
    else:
      logger.info("With NO mounts.")

  def _container_running(self, container):
    self.logs = []
    for line in container.attach(stdout=True, stderr=True, stream=True):
      line = line.decode()
      self.logs.append(line)
      logger.info(line)

  @contextlib.contextmanager
  def _auto_close(self, container):
    try:
      yield container
    finally:
      container.stop()
      container.remove()
      logger.info("Auto-closing container")
