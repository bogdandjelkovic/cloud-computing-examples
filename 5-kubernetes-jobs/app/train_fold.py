import os
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import numpy as np
from sklearn.model_selection import KFold
import warnings

warnings.filterwarnings("ignore")

dataset_file = os.environ.get('DATASET_FILE', '/app/data.csv')
target_column = os.environ.get('TARGET_COLUMN', 'MEDV')
k = int(os.environ.get('K', '10'))
current_fold = int(os.environ.get('JOB_COMPLETION_INDEX', '0'))

print(f"Running fold {current_fold} of {k}")

df = pd.read_csv(dataset_file)
df = df.fillna(df.mean())

X = df.drop(columns=[target_column])
y = df[target_column]

kf = KFold(n_splits=k, shuffle=True, random_state=42)
folds = list(kf.split(X))

train_idx, test_idx = folds[current_fold]

X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]

model = LinearRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

print(f"Fold {current_fold} RMSE: {rmse}")

os.makedirs("/results", exist_ok=True)
with open(f"/results/rmse_fold_{current_fold}.txt", "w") as f:
    f.write(f"{rmse}\n")
