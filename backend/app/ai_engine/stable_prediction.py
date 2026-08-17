from collections import deque
from collections import Counter


class StablePrediction:
    """
    Accepts a prediction only if it stays the same
    for several consecutive frames.
    """

    def __init__(self, required_frames=5):
        self.required_frames = required_frames
        self.history = deque(maxlen=required_frames)

    def update(self, prediction):
        self.history.append(prediction)

        if len(self.history) < self.required_frames:
            return None

        most_common = Counter(self.history).most_common(1)[0]

        if most_common[1] == self.required_frames:
            return most_common[0]

        return None

    def clear(self):
        self.history.clear()