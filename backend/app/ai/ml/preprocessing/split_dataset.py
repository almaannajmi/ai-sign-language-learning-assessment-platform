import pandas as pd
from sklearn.model_selection import train_test_split
from pathlib import Path

# Locate project root
CURRENT_FILE = Path(__file__).resolve()
PROJECT_ROOT = CURRENT_FILE.parents[5]

INPUT_CSV = PROJECT_ROOT / "normalized_landmarks.csv"

TRAIN_CSV = PROJECT_ROOT / "train.csv"
VALIDATION_CSV = PROJECT_ROOT / "validation.csv"
TEST_CSV = PROJECT_ROOT / "test.csv"


def main():
    print("Reading normalized_landmarks.csv...")

    df = pd.read_csv(INPUT_CSV)

    X = df.iloc[:, :-1]
    y = df.iloc[:, -1]

    # 70% Train | 30% Temporary
    X_train, X_temp, y_train, y_temp = train_test_split(
        X,
        y,
        test_size=0.30,
        stratify=y,
        random_state=42
    )

    # Split remaining 30% into Validation (15%) and Test (15%)
    X_val, X_test, y_val, y_test = train_test_split(
        X_temp,
        y_temp,
        test_size=0.50,
        stratify=y_temp,
        random_state=42
    )

    train_df = pd.concat([X_train, y_train], axis=1)
    val_df = pd.concat([X_val, y_val], axis=1)
    test_df = pd.concat([X_test, y_test], axis=1)

    train_df.to_csv(TRAIN_CSV, index=False)
    val_df.to_csv(VALIDATION_CSV, index=False)
    test_df.to_csv(TEST_CSV, index=False)

    print("\nDataset split completed successfully!\n")

    print(f"Training samples   : {len(train_df)}")
    print(f"Validation samples : {len(val_df)}")
    print(f"Test samples       : {len(test_df)}")

    print("\nClass distribution:\n")

    print("Training:")
    print(y_train.value_counts().sort_index())

    print("\nValidation:")
    print(y_val.value_counts().sort_index())

    print("\nTest:")
    print(y_test.value_counts().sort_index())


if __name__ == "__main__":
    main()