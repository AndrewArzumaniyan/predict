import argparse
import catboost
from get_coverage_metric import get_coverage_metric

model = catboost.CatBoostRegressor()
model.load_model('./model.cbm')

def parse_args():
  parser = argparse.ArgumentParser(description='Run CatBoost Regression Model')
  parser.add_argument('params', nargs='+', type=float, help='Input parameters for prediction')
  parser.add_argument('-covfile', '--filepath', type=str, required=True, help='Path to the file containing data')
  args = parser.parse_args()
  
  params = args.params
  filepath = args.filepath
  
  return params, filepath

def predict(params, coverage_file_path):
  coverage_metric = get_coverage_metric(coverage_file_path)
  input_data = params
  input_data.append(coverage_metric)
  return model.predict(input_data)

def main():
  params, filepath = parse_args()
  prediction = predict(params, filepath)
  print(f'Prediction: {prediction}')

if __name__ == '__main__':
  main()