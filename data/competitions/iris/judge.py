import csv
import logging

logger = logging.getLogger(__file__)

def _get_results(filename):
  with open(filename) as csvfile:
    reader = csv.reader(csvfile)
    return [row for row in reader]

def _get_result_file(base_path, is_training):
  if is_training:
    return f"{base_path}/results/training_labels.csv"
  else:
    return f"{base_path}/results/test_labels.csv"

def judge(is_traning, base_path, output_path):
  results = _get_results(_get_result_file(base_path, is_traning))
  output = _get_results(output_path + "/output.csv")

  score = 0
  for expected, actual in zip(results, output):
    logger.info(f"Expected: `{expected[0]}`, got: `{actual[0]}`")
    if expected[0] == actual[0]:
      score += 1
  return score / len(results)
