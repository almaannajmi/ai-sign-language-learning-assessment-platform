import cv2
import mediapipe as mp


class LandmarkExtractor:
    """
    Extracts 21 hand landmarks from an input image using MediaPipe.
    """

    def __init__(self):
        self.mp_hands = mp.solutions.hands

        self.hands = self.mp_hands.Hands(
            static_image_mode=True,
            max_num_hands=2,
            min_detection_confidence=0.5
        )

    def extract(self, image):
        """
        Extract 63 landmark values from an image.

        Args:
            image: OpenCV image (BGR format)

        Returns:
            List of 63 values if one valid hand is detected.
            Otherwise returns a status string.
        """

        # Convert BGR image to RGB for MediaPipe
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Detect hands
        results = self.hands.process(rgb_image)

        # No hand detected
        if not results.multi_hand_landmarks:
            return "NO_HAND"

        # More than one hand detected
        if len(results.multi_hand_landmarks) > 1:
            return "MULTIPLE_HANDS"

        # Get the single detected hand
        hand_landmarks = results.multi_hand_landmarks[0]

        # Check if hand is too close to image boundary
       

        # Extract x, y, z coordinates
        features = []

        for landmark in hand_landmarks.landmark:
            features.extend([
                landmark.x,
                landmark.y,
                landmark.z
            ])

        # 21 landmarks × 3 values = 63 features
        return features