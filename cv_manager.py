# File Name: cv_manager.py
# This module contains the backend logic using only MediaPipe.
# No external model files are needed.

import cv2
import mediapipe as mp
from datetime import datetime
import os

class MediaPipeProcessor:
    """
    Encapsulates all MediaPipe-related initializations and processing logic.
    """
    def __init__(self):
        """Initializes MediaPipe solutions for hand and face detection."""
        self.mp_hands = mp.solutions.hands
        self.mp_face_detection = mp.solutions.face_detection
        self.mp_drawing = mp.solutions.drawing_utils

        # Initialize with specific confidence levels for better accuracy
        self.hands = self.mp_hands.Hands(
            max_num_hands=2,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        self.face_detector = self.mp_face_detection.FaceDetection(
            min_detection_confidence=0.7
        )

    def _count_fingers(self, hand_landmarks, handedness):
        """
        Private helper method to count the number of fingers up for one hand.
        It uses handedness (Left/Right) to correctly detect the thumb.
        """
        tip_ids = [4, 8, 12, 16, 20] # Landmark indices for all 5 finger tips
        count = 0
        
        # Simple check for thumb based on hand orientation
        hand_label = handedness.classification[0].label.lower()
        
        if hand_label == 'right':
            # For a right hand, the thumb is up if its x-coordinate is to the left of the next landmark
            if hand_landmarks.landmark[tip_ids[0]].x > hand_landmarks.landmark[tip_ids[0] - 1].x:
                count += 1
        else: # Left hand
            # For a left hand, the thumb is up if its x-coordinate is to the right of the next landmark
            if hand_landmarks.landmark[tip_ids[0]].x < hand_landmarks.landmark[tip_ids[0] - 1].x:
                count += 1

        # Check for the other four fingers
        for i in range(1, 5):
            # A finger is up if its tip's y-coordinate is above its pip's y-coordinate
            if hand_landmarks.landmark[tip_ids[i]].y < hand_landmarks.landmark[tip_ids[i] - 2].y:
                count += 1
                
        return count

    def process_frame(self, frame):
        """
        Processes a single camera frame to detect and draw hand and face landmarks.
        Returns the processed frame with annotations.
        """
        # Flip the frame horizontally for a selfie-view display
        frame = cv2.flip(frame, 1)
        # Convert the BGR image to RGB for MediaPipe processing
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process for hand landmarks and handedness
        hand_results = self.hands.process(rgb_frame)
        if hand_results.multi_hand_landmarks and hand_results.multi_handedness:
            # Iterate over both landmarks and handedness results
            for hand_landmarks, handedness in zip(hand_results.multi_hand_landmarks, hand_results.multi_handedness):
                # Draw hand landmarks on the frame
                self.mp_drawing.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                
                # Get the hand label (Left or Right) and count fingers
                hand_label = handedness.classification[0].label
                finger_count = self._count_fingers(hand_landmarks, handedness)
                
                # Display the label and finger count on the frame
                h, w, _ = frame.shape
                cx = int(hand_landmarks.landmark[0].x * w)
                cy = int(hand_landmarks.landmark[0].y * h)
                cv2.putText(frame, f"{hand_label}: {finger_count} Fingers", (cx - 70, cy - 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        # Process for face detection
        face_results = self.face_detector.process(rgb_frame)
        if face_results.detections:
            for detection in face_results.detections:
                self.mp_drawing.draw_detection(frame, detection)
        
        return frame

    def save_photo(self, frame, output_dir="outputs"):
        """Saves a single BGR frame as a JPG image."""
        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(output_dir, f"photo_{timestamp}.jpg")
        cv2.imwrite(output_path, frame)
        return f"Photo saved to: {output_path}"

    def save_video(self, frames, output_dir="outputs"):
        """Saves a list of frames as an MP4 video."""
        if not frames:
            return "No frames to save."
        
        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(output_dir, f"recording_{timestamp}.mp4")

        # Get frame dimensions from the first frame
        height, width, _ = frames[0].shape
        fourcc = cv2.VideoWriter_fourcc(*'mp4v') # Use 'mp4v' for .mp4 files
        
        video_writer = cv2.VideoWriter(output_path, fourcc, 20.0, (width, height)) # 20 FPS is a reasonable default

        for frame in frames:
            # MediaPipe processes RGB, but VideoWriter needs BGR
            bgr_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            video_writer.write(bgr_frame)

        video_writer.release()
        return f"Video saved successfully to: {output_path}"
