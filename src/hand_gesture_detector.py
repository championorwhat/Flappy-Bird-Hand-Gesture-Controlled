"""
Hand Gesture Detection Module
Uses MediaPipe to detect hand gestures for game control
"""

import cv2
import mediapipe as mp
import numpy as np
from config import *

class HandGestureDetector:
    def __init__(self):
        """Initialize MediaPipe hand detection"""
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=MIN_DETECTION_CONFIDENCE,
            min_tracking_confidence=MIN_TRACKING_CONFIDENCE
        )
        self.mp_draw = mp.solutions.drawing_utils

    def count_fingers(self, landmarks):
        """
        Count the number of raised fingers
        Returns: int - number of fingers up (0-5)
        """
        if len(landmarks) < 21:
            return 0

        fingers_up = 0

        # Thumb (compare x coordinates for left/right)
        if landmarks[FINGER_TIPS[0]][0] > landmarks[FINGER_PIPS[0]][0]:
            fingers_up += 1

        # Other fingers (compare y coordinates)
        for i in range(1, 5):
            if landmarks[FINGER_TIPS[i]][1] < landmarks[FINGER_PIPS[i]][1]:
                fingers_up += 1

        return fingers_up

    def get_hand_center(self, landmarks):
        """
        Get the center position of the hand
        Returns: tuple (x, y) - center coordinates
        """
        if len(landmarks) < 21:
            return None

        # Use wrist and middle finger tip to calculate center
        wrist = landmarks[HAND_LANDMARKS['WRIST']]
        middle_tip = landmarks[HAND_LANDMARKS['MIDDLE_TIP']]

        center_x = (wrist[0] + middle_tip[0]) // 2
        center_y = (wrist[1] + middle_tip[1]) // 2

        return (center_x, center_y)

    def detect_peace_sign(self, landmarks):
        """
        Detect peace sign (index and middle finger up, others down)
        Returns: bool - True if peace sign detected
        """
        if len(landmarks) < 21:
            return False

        # Check if index and middle fingers are up
        index_up = landmarks[FINGER_TIPS[1]][1] < landmarks[FINGER_PIPS[1]][1]
        middle_up = landmarks[FINGER_TIPS[2]][1] < landmarks[FINGER_PIPS[2]][1]

        # Check if ring and pinky are down
        ring_down = landmarks[FINGER_TIPS[3]][1] > landmarks[FINGER_PIPS[3]][1]
        pinky_down = landmarks[FINGER_TIPS[4]][1] > landmarks[FINGER_PIPS[4]][1]

        return index_up and middle_up and ring_down and pinky_down

    def detect_thumbs_up(self, landmarks):
        """
        Detect thumbs up gesture
        Returns: bool - True if thumbs up detected
        """
        if len(landmarks) < 21:
            return False

        # Thumb should be up (x coordinate comparison)
        thumb_up = landmarks[FINGER_TIPS[0]][0] > landmarks[FINGER_PIPS[0]][0]

        # Other fingers should be down
        fingers_down = all(
            landmarks[FINGER_TIPS[i]][1] > landmarks[FINGER_PIPS[i]][1]
            for i in range(1, 5)
        )

        return thumb_up and fingers_down

    def detect_fist(self, landmarks):
        """
        Detect closed fist
        Returns: bool - True if fist detected
        """
        if len(landmarks) < 21:
            return False

        # All fingers should be down
        fingers_down = all(
            landmarks[FINGER_TIPS[i]][1] > landmarks[FINGER_PIPS[i]][1]
            for i in range(1, 5)
        )

        # Thumb should be down too
        thumb_down = landmarks[FINGER_TIPS[0]][0] < landmarks[FINGER_PIPS[0]][0]

        return fingers_down and thumb_down

    def process_frame(self, frame):
        """
        Process camera frame and detect hand gestures

        Args:
            frame: OpenCV frame from camera

        Returns:
            dict: {
                'should_flap': bool,
                'hand_position': tuple or None,
                'fingers_count': int,
                'gesture': str,
                'frame': processed frame with landmarks
            }
        """
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(frame_rgb)

        # Default return values
        should_flap = False
        hand_position = None
        fingers_count = 0
        gesture = "none"

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw landmarks on frame
                self.mp_draw.draw_landmarks(
                    frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS
                )

                # Extract landmark coordinates
                landmarks = []
                h, w, c = frame.shape
                for lm in hand_landmarks.landmark:
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    landmarks.append([cx, cy])

                if len(landmarks) >= 21:
                    # Count fingers
                    fingers_count = self.count_fingers(landmarks)

                    # Get hand position
                    hand_position = self.get_hand_center(landmarks)

                    # Detect specific gestures
                    if self.detect_peace_sign(landmarks):
                        gesture = "peace"
                        should_flap = True
                    elif self.detect_thumbs_up(landmarks):
                        gesture = "thumbs_up"
                        should_flap = True
                    elif self.detect_fist(landmarks):
                        gesture = "fist"
                    elif fingers_count >= MIN_FINGERS_FOR_FLAP:
                        gesture = f"{fingers_count}_fingers"
                        should_flap = True

                    # Draw gesture info on frame
                    if hand_position:
                        cv2.putText(
                            frame, 
                            f"Fingers: {fingers_count}", 
                            (10, 30), 
                            cv2.FONT_HERSHEY_SIMPLEX, 
                            1, 
                            (0, 255, 0), 
                            2
                        )
                        cv2.putText(
                            frame, 
                            f"Gesture: {gesture}", 
                            (10, 70), 
                            cv2.FONT_HERSHEY_SIMPLEX, 
                            1, 
                            (255, 0, 0), 
                            2
                        )

                        # Draw hand center
                        cv2.circle(frame, hand_position, 10, (255, 255, 0), -1)

        return {
            'should_flap': should_flap,
            'hand_position': hand_position,
            'fingers_count': fingers_count,
            'gesture': gesture,
            'frame': frame
        }