import numpy as np

from app.ai.ml.preprocessing.normalize_landmarks import normalize_sample


class Preprocessor:
    """
    Handles preprocessing before prediction.
    """

    @staticmethod
    def preprocess(features):
        """
        Validate and normalize landmark features.

        Args:
            features: List or NumPy array containing 63 values.

        Returns:
            NumPy array of normalized features.
        """

        if features is None:
            raise ValueError("Features cannot be None.")

        features = np.array(features, dtype=float)

        if features.size != 63:
            raise ValueError(
                f"Expected 63 features, but got {features.size}."
            )

        normalized = normalize_sample(features)

        return np.array(normalized).reshape(1, -1)