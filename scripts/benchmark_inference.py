import os
import time
import tracemalloc
import pickle

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


# -------------------------
# Load dataset
# -------------------------

train_df = pd.read_csv("train.csv")
test_df = pd.read_csv("test.csv")

X_train = train_df.drop("label", axis=1)
y_train = train_df["label"]

X_test = test_df.drop("label", axis=1)
y_test = test_df["label"]


# -------------------------
# Train model
# -------------------------

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)

model.fit(X_train, y_train)


# -------------------------
# Accuracy Evaluation
# -------------------------

predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions) * 100


# -------------------------
# Save model
# -------------------------

with open("random_forest_model.pkl", "wb") as f:
    pickle.dump(model, f)

model_size = os.path.getsize("random_forest_model.pkl") / 1024


# -------------------------
# Benchmark Inference
# -------------------------

sample = X_test.iloc[[0]]

tracemalloc.start()

start = time.perf_counter()

runs = 1000

for _ in range(runs):
    model.predict(sample)

end = time.perf_counter()

current, peak = tracemalloc.get_traced_memory()

tracemalloc.stop()


# -------------------------
# Calculate Metrics
# -------------------------

avg_time = ((end - start) / runs) * 1000

throughput = runs / (end - start)

peak_memory = peak / 1024


# -------------------------
# Print Results
# -------------------------

print("\n========== MODEL EVALUATION ==========")

print(f"Accuracy               : {accuracy:.2f}%")

print(f"Average inference time : {avg_time:.4f} ms")

print(f"Peak memory            : {peak_memory:.2f} KB")

print(f"Model size             : {model_size:.2f} KB")

print(f"Throughput             : {throughput:.2f} predictions/sec")

print("======================================")