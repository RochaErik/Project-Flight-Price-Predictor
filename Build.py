import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from catboost import CatBoostRegressor # Model selected for having the best performance
import pickle

df = pd.read_csv('df_deployed')

df = df.drop('Unnamed: 0', axis=1)

X = df.drop('Price', axis=1)
y = df['Price']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

cat_model = CatBoostRegressor()
cat_model.fit(X_train, y_train)

cat_model_predict = cat_model.predict(X_test)

pickle.dump(cat_model, open('model.pkl', 'wb'))