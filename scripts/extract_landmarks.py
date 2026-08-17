import cv2
import mediapipe as mp

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands

hands = mp_hands.Hands(
    static_image_mode=True,
    max_num_hands=1,
    min_detection_confidence=0.5
)


def extract_landmarks(image_path):
    """
    Extract 21 hand landmarks (63 values) from an image.

    Args:
        image_path (str): Path to an image.

    Returns:
        list:
            63 landmark values if a hand is detected.
        None:
            If the image cannot be read or no hand is detected.
    """

    image = cv2.imread(image_path)

    if image is None:
        return None

    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb)

    if not results.multi_hand_landmarks:
        return None

    landmarks = []

    for landmark in results.multi_hand_landmarks[0].landmark:
        landmarks.extend([
            landmark.x,
            landmark.y,
            landmark.z
        ])

    return landmarks


if __name__ == "__main__":

    # Change this to any image from your dataset
    image_path = "datasets/ASL Alphabet Dataset/dataset/A-samples/0.jpg"
    features = extract_landmarks(image_path)

    if features:
        print("Landmarks extracted successfully!")
        print("Total values:", len(features))
    else:
        print("No hand detected.")
