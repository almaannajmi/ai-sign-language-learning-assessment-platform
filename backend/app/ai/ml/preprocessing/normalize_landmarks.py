import pandas as pd
import numpy as np
from pathlib import Path

# Locate project root and files
CURRENT_FILE = Path(__file__).resolve()
PROJECT_ROOT = CURRENT_FILE.parents[5]

INPUT_CSV = PROJECT_ROOT / "landmarks.csv"
OUTPUT_CSV = PROJECT_ROOT / "normalized_landmarks.csv"


def normalize_sample(features):
    """
    Normalize one hand sample.
    Strategy:
    1. Make all landmarks wrist-relative.
    2. Scale using the maximum distance from the wrist.
    """

    landmarks = np.array(features, dtype=float).reshape(21, 3)

    # Wrist landmark (landmark 0)
    wrist = landmarks[0]

    # Wrist-relative coordinates
    landmarks = landmarks - wrist

    # Compute maximum distance from wrist
    distances = np.linalg.norm(landmarks, axis=1)
    max_distance = np.max(distances)

    if max_distance > 0:
        landmarks = landmarks / max_distance

    return landmarks.flatten()


def main():
    print("Reading landmarks.csv...")

    df = pd.read_csv(INPUT_CSV)

    feature_columns = df.columns[:-1]
    label_column = df.columns[-1]

    normalized_data = []

    for _, row in df.iterrows():
        features = row[feature_columns].values
        label = row[label_column]

        normalized_features = normalize_sample(features)

        normalized_data.append(
            list(normalized_features) + [label]
        )

    normalized_df = pd.DataFrame(
        normalized_data,
        columns=list(feature_columns) + [label_column]
    )

    normalized_df.to_csv(OUTPUT_CSV, index=False)

    print(f"\nNormalization completed successfully!")
    print(f"Output saved to:\n{OUTPUT_CSV}")


if __name__ == "__main__":
    main()