import time
from datetime import datetime

from app.ai_engine.input_validator import InputValidator
from app.ai_engine.landmark_extractor import LandmarkExtractor
from app.ai_engine.preprocessor import Preprocessor
from app.ai_engine.model_loader import ModelLoader
from app.ai_engine.prediction_result import PredictionResult
from app.ai_engine.frame_buffer import FrameBuffer
from app.ai_engine.sequence_builder import SequenceBuilder
from app.services.practice_service import PracticeService
from app.services.progress_service import ProgressService
from app.services.report_service import ReportService

from app.feedback.landmark_comparator import LandmarkComparator
from app.feedback.rule_engine import RuleEngine
from app.feedback.feedback_generator import FeedbackGenerator

from app.services.review_service import ReviewService
from app.services.motion_metrics_service import MotionMetricsService

from app.ai.models.assessment_record import AssessmentRecord

from app.services.error_analysis_service import ErrorAnalysisService
from app.services.personalized_feedback_service import PersonalizedFeedbackService
from app.services.learner_profile_service import LearnerProfileService
from app.services.recommendation_service import RecommendationService
from app.services.adaptive_learning_service import AdaptiveLearningService
from app.ai_engine.stable_prediction import StablePrediction
from app.ai_engine.logger import logger

class Predictor:
    """
    Complete AI prediction pipeline.
    """

    def __init__(self):
        self.extractor = LandmarkExtractor()
        self.preprocessor = Preprocessor()
        self.loader = ModelLoader()
        self.validator = InputValidator()

        self.model = self.loader.load_model()
        self.practice = PracticeService()
        self.progress = ProgressService()
        self.profile = LearnerProfileService()
        self.recommendation = RecommendationService()
        self.adaptive = AdaptiveLearningService()
        print(self.progress)
        print(self.progress.__dict__)
        self.report = ReportService(self.progress)
        self.frame_buffer = FrameBuffer(max_frames=20)
        self.sequence_builder = SequenceBuilder()
        self.stable_prediction = StablePrediction(required_frames=1)
        self.comparator = LandmarkComparator()
        self.rule_engine = RuleEngine()
        self.feedback_generator = FeedbackGenerator()
        self.review = ReviewService(self.progress)
        self.error_analysis = ErrorAnalysisService(self.progress)
        self.personalized_feedback = PersonalizedFeedbackService(
            self.progress,
            self.error_analysis
        )
        self.motion = MotionMetricsService()

    def predict(self, image):
        """
        Predict the sign language gesture from an image.
        """

        start_time = time.time()
        valid, message = self.validator.validate(image)

        if not valid:
            logger.warning(f"Prediction validation failed: {message}")
            return {
                "status": "invalid_input",
                "message": message
            }
        self.motion.start_gesture()

        features = self.extractor.extract(image)
        print("DEBUG FEATURES:", features)
        if features == "NO_HAND":
            logger.warning("Prediction failed: no hand detected.")
            self.motion.add_invalid_frame()
            return None

        if features == "MULTIPLE_HANDS":
            logger.warning("Prediction failed: multiple hands detected.")
            self.motion.add_invalid_frame()
            return None

        if features == "PARTIAL_HAND":
            logger.warning("Prediction failed: partial hand detected.")
            self.motion.add_invalid_frame()
            return None

        if features == "NO_PERSON":
            print("No person detected.")
            self.motion.add_invalid_frame()
            return None

        if features == "PARTIAL_BODY":
            print("Partial body detected.")
            self.motion.add_invalid_frame()
            return None

        if features is None:
            logger.warning("Prediction failed: landmark extraction returned None.")
            self.motion.add_invalid_frame()
            return None
        self.motion.add_landmarks(features)

        processed = self.preprocessor.preprocess(features)

        self.frame_buffer.add_frame(processed.flatten())

        if self.frame_buffer.is_full():
            sequence = self.sequence_builder.build(
                self.frame_buffer.get_sequence()
            )

            # Reserved for future LSTM/GRU model

        prediction = self.model.predict(processed)[0]
        stable_prediction = self.stable_prediction.update(prediction)
        print("DEBUG STABLE PREDICTION:", stable_prediction)

        if stable_prediction is None:
            return None

        prediction = stable_prediction
        landmark_features = self.comparator.compare(features)

        rules = self.rule_engine.evaluate(
            expected=self.practice.current_letter(),
            predicted=prediction,
            features=landmark_features
        )

        feedback = self.feedback_generator.generate(rules)

        confidence = max(
            self.model.predict_proba(processed)[0]
        )

        self.motion.add_confidence(float(confidence))

        inference_time = time.time() - start_time

        expected = self.practice.current_letter()

        is_correct = prediction.startswith(expected)

        self.practice.record_attempt(is_correct)

        if is_correct:
            self.practice.next_letter()

        self.progress.add_attempt(
            expected=expected,
            predicted=prediction,
            correct=is_correct,
            confidence=float(confidence),
            inference_time=inference_time
        )

        self.profile.update(
            expected=expected,
            correct=is_correct,
            confidence=float(confidence)
        )

        print("\n========== SESSION DASHBOARD ==========")

        print(f"Expected Letter : {expected}")
        print(f"Predicted Letter: {prediction}")
        print(f"Correct         : {is_correct}")

        print("---------------------------------------")

        print(f"Total Attempts  : {self.progress.total_attempts()}")
        print(f"Accuracy        : {self.progress.accuracy():.2f}%")
        print(f"Average Confidence : {self.progress.average_confidence():.2f}")

        print(f"Strongest Letter: {self.progress.strongest_alphabet()}")
        print(f"Weakest Letter  : {self.progress.weakest_alphabet()}")
        print(f"Most Mistaken   : {self.progress.most_mistaken()}")

        print("Recent History:")

        for item in self.progress.recent_history():
            print(
                f"{item['expected']} -> {item['predicted']} | "
                f"{'✓' if item['correct'] else '✗'} | "
                f"{item['confidence']:.2f}"
            )

        print("=======================================\n")

        print("\nFeedback:")

        for message in feedback["messages"]:
            print(f"- {message}")
        self.report.export_json()

        review = self.review.generate_review()

        print("\n========== PRACTICE REVIEW ==========")

        print(f"Overall Score      : {review['overall_score']}%")
        print(f"Correct Gestures   : {review['correct']}")
        print(f"Incorrect Gestures : {review['incorrect']}")
        print(f"Average Confidence : {review['average_confidence']}")
        print(f"Strongest Gesture  : {review['strongest_gesture']}")
        print(f"Weakest Gesture    : {review['weakest_gesture']}")
        print(f"Most Common Mistake: {review['most_common_mistake']}")

        print("=====================================\n")
        print(f"Gesture Time      : {self.motion.gesture_time():.2f} sec")
        print(f"Invalid Frames    : {self.motion.invalid_frames}")
        print(f"Gesture Confidence: {self.motion.average_confidence():.2f}")
        print(f"Gesture Stability : {self.motion.stability_score():.2f}")

        overall_score = self.motion.overall_sign_score(
            hand_shape_accuracy=confidence * 100
)

        print(f"Overall Sign Score: {overall_score:.2f}")

        analysis = self.error_analysis.generate_analysis()

        feedback = self.personalized_feedback.generate()

        print("\n===== PERSONALIZED FEEDBACK =====")

        for message in feedback:
            print("-", message)

        print("=================================\n")

        print("\n========== ERROR ANALYSIS ==========")
        print(analysis)
        print("====================================")

        assessment = AssessmentRecord(
            expected=expected,
            predicted=prediction,
            correct=is_correct,
            confidence=float(confidence),
            overall_accuracy=self.progress.accuracy(),
            attempt_number=self.progress.total_attempts(),
            inference_time=inference_time,
            session_accuracy=self.progress.accuracy(),
            timestamp=datetime.now(),
            gesture_time=self.motion.gesture_time(),
            invalid_frames=self.motion.invalid_frames,
            gesture_stability=self.motion.stability_score(),
            overall_score=overall_score
        )

        print("\nAssessment Record:")
        print(assessment)

        print("\n===== LEARNER PROFILE =====")
        print(self.profile.profile())
        print("===========================\n")

        profile = self.profile.profile()

        recommendations = self.recommendation.recommend(profile)

        print("\n===== RECOMMENDATIONS =====")

        for item in recommendations:
            print(f"{item['alphabet']} : {item['reason']}")

        print("===========================\n")

        plan = self.adaptive.generate_plan(profile)

        print("\n===== ADAPTIVE LEARNING PLAN =====")
        print("Practice Now :", plan["practice_now"])
        print("Review Later :", plan["review_later"])
        print("Mastered     :", plan["mastered"])
        print("==================================\n")

        return PredictionResult(
            label=prediction,
            confidence=float(confidence),
            model_version=self.loader.model_version,
            inference_time=inference_time,
            feedback=feedback,
            expected=expected,
            correct=is_correct,
            accuracy=self.progress.accuracy()
        )