import sys
from sklearn.metrics import mean_squared_error
import math
import pandas as pd
from sklearn.linear_model import LinearRegression

train_file = sys.argv[1]
test_file = sys.argv[2]
target_column = sys.argv[3]

train_df = pd.read_csv(train_file)
test_df = pd.read_csv(test_file)

X_train = train_df.drop(columns=[target_column])
y_train = train_df[target_column]

X_test = test_df.drop(columns=[target_column])
y_test = test_df[target_column]

model = LinearRegression()
model.fit(X_train, y_train)
preds = model.predict(X_test)

rmse = math.sqrt(mean_squared_error(y_test, preds))

with open("rmse.txt", "w") as f:
    f.write(f"{rmse}\n")
