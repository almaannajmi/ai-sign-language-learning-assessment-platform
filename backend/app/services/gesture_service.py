from app.schemas.prediction import PredictionResponse
from app.ai_engine.predictor import Predictor


class GestureService:

    def _init_(self):
        self.predictor = Predictor()

    def predict(self, image) -> PredictionResponse:

        result = self.predictor.predict(image)

        if result is None:
            return PredictionResponse(
                predicted_label="UNKNOWN",
                confidence=0.0,
                processing_time=0.0
            )

        if isinstance(result, dict):
            return PredictionResponse(
                predicted_label="INVALID",
                confidence=0.0,
                processing_time=0.0
            )

        return PredictionResponse(
            predicted_label=result.label,
            confidence=result.confidence,
            processing_time=result.inference_time
        )