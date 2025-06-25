import cv2
import mediapipe as mp

################################################################

class HandTracker:
    def __init__(self) -> None:
        self.mp_hands = mp.solutions.hands # type: ignore
        self.hands = self.mp_hands.Hands(static_image_mode=False,
                            max_num_hands=2,
                            min_detection_confidence=0.7,
                            min_tracking_confidence=0.7)
        self.mp_drawing = mp.solutions.drawing_utils # type: ignore

    def _get_hand_landmarks(self, results, img_shape):
        hands_data = []

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                hand_data = {}
                for i, lm in enumerate(hand_landmarks.landmark):
                    h, w, _ = img_shape
                    hand_data[f"landmark_{i}"] = {
                        "x": lm.x * w,
                        "y": lm.y * h,
                        "z": lm.z * w
                    }
                hands_data.append(hand_data)
        return hands_data

    def process_frame(self, frame):
        results = self.hands.process(frame)

        hand_landmarks_data = self._get_hand_landmarks(results, frame.shape)
        if hand_landmarks_data:
            for hand in hand_landmarks_data:
                print(hand)

        return results

    def annotate_frame(self, frame, results):
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS
                )
        return frame