import catboost
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

model = catboost.CatBoostRegressor(
  bagging_temperature=0.01, 
  depth=10, 
  learning_rate=0.05, 
  iterations=1000, 
  l2_leaf_reg=1, 
  leaf_estimation_method='Gradient', 
  verbose=False
)

df = pd.read_csv('./dataset-without_bt.csv')

X_train, X_test, y_train, y_test = train_test_split(df.drop('predict', axis=1), df['predict'], test_size=0.3)

model.fit(X_train, y_train);

pred = model.predict(X_test)
print("mae:", mean_absolute_error(y_test, pred))

model.save_model('./model.cbm')