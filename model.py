import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import pickle

data = pd.read_csv("student-mat.csv", sep=';')

X = data[['studytime', 'failures', 'absences']]
y = data['G3']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = RandomForestRegressor()
model.fit(X_train, y_train)

pickle.dump(model, open("model.pkl", "wb"))

print("Model Ready 🚀")