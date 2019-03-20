import logging
import json
import requests
import traceback
from app.env import SLACK_WEB_HOOK_URL

logger = logging.getLogger(__file__)

class SlackNotifier:
  def notify_result(self, *args):
    if not SLACK_WEB_HOOK_URL:
      logger.error("environment variable SLACK_WEB_HOOK_URL not set, no notifications sent.")
      return
    msg = self._format(*args)
    return self._send(msg)

  def _format(self, *args):
    if len(args) == 2:
      return self._format_error(*args)
    else:
      return self._format_result(*args)

  def _format_error(self, *args):
    options, exception = args
    preview = "\n".join([
      f"Evaluation failed for Team `{options['team']}`:"
    ])
    msg = '\n'.join(traceback.format_exception(etype=type(exception), value=exception, tb=exception.__traceback__))
    return {
      "attachments": [{
          "color": "danger",
          "fallback": preview,
          "pretext": preview,
          "fields": [
            {
              "title": f"Competition: {options['competition']}",
              "value": msg
            }
          ]
      }]
    }

  def _format_result(self, *args):
    eval = args[0]
    preview = "\n".join([
      f"Evaluation results for Team `{eval.team_name}`:"
    ])
    return {
      "attachments": [{
        "color": "good",
        "fallback": preview,
        "pretext": preview,
        "title": f"Competition: {eval.competition.name} ({eval.competition.code})",
        "title_link": eval.competition.url,
        "fields": [
          {
            "title": "Score",
            "value": "`%.4f`" % eval.final_score,
            "short": True
          },
          {
            "title": "Duration",
            "value": f"{eval.duration:.1f} seconds",
            "short": True
          },
          {
            "title": "Docker Image",
            "value": f"{eval.docker_image_name}:{eval.docker_image_tag} ({eval.docker_image_hash})",
            "short": False
          },
          {
            "title": "Task Details",
            "value": f"<{eval.task_url}|Link>",
            "short": False
          }
        ]
      }]
    }

  def _send(self, msg):
    r = requests.post(SLACK_WEB_HOOK_URL, data=json.dumps(msg))
    logger.info("Slack notification result: %d %s", r.status_code, r.reason)
    return r.status_code
