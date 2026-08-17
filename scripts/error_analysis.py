import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix

# Load datasets
train_df = pd.read_csv("train.csv")
test_df = pd.read_csv("test.csv")

X_train = train_df.drop("label", axis=1)
y_train = train_df["label"]

X_test = test_df.drop("label", axis=1)
y_test = test_df["label"]

# Train best model
model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)

model.fit(X_train, y_train)

predictions = model.predict(X_test)

# Generate confusion matrix
labels = sorted(y_test.unique())

cm = confusion_matrix(
    y_test,
    predictions,
    labels=labels
)

plt.figure(figsize=(12,10))

sns.heatmap(
    cm,
    cmap="Blues",
    xticklabels=labels,
    yticklabels=labels
)

plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")

plt.tight_layout()

plt.savefig("confusion_matrix.png")

print("Confusion Matrix saved as confusion_matrix.png")

# Find top confused gestures
confusions = []

for i in range(len(labels)):
    for j in range(len(labels)):
        if i != j and cm[i][j] > 0:
            confusions.append(
                (
                    labels[i],
                    labels[j],
                    cm[i][j]
                )
            )

confusions.sort(
    key=lambda x: x[2],
    reverse=True
)

top5 = confusions[:5]

with open("error_analysis.md", "w") as f:

    f.write("# Error Analysis\n\n")

    f.write("## Top 5 Most Confused Gestures\n\n")

    if len(top5) == 0:
        f.write("No significant confusions found.\n\n")
    else:
        for actual, predicted, count in top5:
            f.write(
                f"- {actual} predicted as {predicted} ({count} times)\n"
            )

    f.write("\n## Possible Reasons\n\n")

    f.write("- Similar finger positions\n")
    f.write("- Poor dataset quality\n")
    f.write("- Occlusion\n")
    f.write("- Incorrect labels\n")
    f.write("- Background noise\n")

print("error_analysis.md generated successfully!")