from pathlib import Path
import joblib


class ModelLoader:
    """
    Loads and provides access to the trained ML model.
    """

    def __init__(self):
        self.model = None
        self.model_version = "v1.0"

    def load_model(self):
        """
        Load the trained Random Forest model.
        """
        if self.model is None:
            model_path = (
                Path(__file__).resolve().parents[2]
                / "random_forest_model.pkl"
            )

            self.model = joblib.load(model_path)

        return self.model