# import cv2
# import numpy as np
# import mediapipe as mp
# from mediapipe.tasks import python
# from mediapipe.tasks.python import vision
# from mediapipe.framework.formats import landmark_pb2

# # Setup the model
# model_path = 'video/hand_landmarker.task'
# BaseOptions = python.BaseOptions
# HandLandmarker = vision.HandLandmarker
# HandLandmarkerOptions = vision.HandLandmarkerOptions
# VisionRunningMode = vision.RunningMode

# # Gesture Logic
# def is_finger_extended(tip, pip, landmarks):
#     return landmarks[tip].y < landmarks[pip].y

# def is_finger_bent(tip, pip, landmarks):
#     return landmarks[tip].y > landmarks[pip].y

# def detect_ram_horn(landmarks):
#     return (
#         is_finger_extended(8, 6, landmarks) and    # Index
#         is_finger_extended(20, 18, landmarks) and  # Pinky
#         is_finger_bent(12, 10, landmarks) and      # Middle
#         is_finger_bent(16, 14, landmarks)          # Ring
#     )

# # Initialize hand landmarker
# options = HandLandmarkerOptions(
#     base_options=BaseOptions(model_asset_path=model_path),
#     running_mode=VisionRunningMode.VIDEO,
#     num_hands=2
# )

# detector = HandLandmarker.create_from_options(options)

# # Callback for async detection
# results_container = {'results': None}

# def callback(result, output_image, timestamp):
#     results_container['results'] = result

# # Open webcam
# cap = cv2.VideoCapture(0)
# if not cap.isOpened():
#     raise IOError("Cannot open webcam")

# while True:
#     ret, frame = cap.read()
#     if not ret:
#         continue

#     image = cv2.flip(frame, 1)
#     mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
#     timestamp = int(cv2.getTickCount() / cv2.getTickFrequency() * 1000)

#     detector.detect_async(mp_image, timestamp)
#     result = results_container['results']

#     if result and result.hand_landmarks:
#         if result is not None and result.hand_landmarks:
#             assert result is not None and result.hand_landmarks is not None
#             for hand_landmarks in result.hand_landmarks: # type: ignore
#                 # Draw landmarks
#                 for lm in hand_landmarks:
#                     h, w, _ = image.shape
#                     cx, cy = int(lm.x * w), int(lm.y * h)
#                     cv2.circle(image, (cx, cy), 4, (0, 255, 0), -1)

#                 if detect_ram_horn(hand_landmarks):
#                     cv2.putText(image, 'Ram Horn Fingers Detected!', (30, 60),
#                                 cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)

#     cv2.imshow('Ram Horn Fingers Detector', image)
#     if cv2.waitKey(5) & 0xFF == 27:  # ESC key to quit
#         break

# cap.release()
# cv2.destroyAllWindows()
