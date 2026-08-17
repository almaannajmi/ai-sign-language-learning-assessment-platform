import time
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score

# Load datasets
train_df = pd.read_csv("train.csv")
test_df = pd.read_csv("test.csv")

# Split features and labels
X_train = train_df.drop("label", axis=1)
y_train = train_df["label"]

X_test = test_df.drop("label", axis=1)
y_test = test_df["label"]

results = []

# Test different numbers of trees
for trees in [50, 100, 200]:

    model = RandomForestClassifier(
        n_estimators=trees,
        random_state=42
    )

    start = time.time()

    model.fit(X_train, y_train)

    training_time = time.time() - start

    predictions = model.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)

    f1 = f1_score(
        y_test,
        predictions,
        average="weighted"
    )

    results.append({
        "Trees": trees,
        "Training Time": round(training_time, 4),
        "Accuracy": round(accuracy, 4),
        "F1 Score": round(f1, 4)
    })

results_df = pd.DataFrame(results)

results_df.to_csv(
    "hyperparameter_study.csv",
    index=False
)

print(results_df)