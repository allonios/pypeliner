from math import atan2, degrees
from typing import List

from mediapipe.framework.formats.landmark_pb2 import NormalizedLandmarkList
from numpy import ndarray

from examples.hand_operations.utils import Orientation


class HandState:
    def __init__(
        self, id: int, landmarks: NormalizedLandmarkList, hand_type: str
    ) -> None:
        self.id = id
        self.landmarks = landmarks
        self.rotated_landmarks = None
        self.hand_type = hand_type
        self.thumb_orientation = Orientation.UNIDENTIFIED
        self.orientation = Orientation.UNIDENTIFIED
        self.raised_fingers = []

    def clear_raised_fingers(self) -> None:
        self.raised_fingers.clear()

    def add_raised_finger(self, finger: int) -> None:
        self.raised_fingers.append(finger)

    def add_raised_fingers(self, fingers: List) -> None:
        self.raised_fingers.extend(fingers)

    def get_hand_rotation_degrees(
        self,
        hand_line: tuple,
        image_shape: tuple,
    ) -> float:
        top_landmark = self.landmarks.landmark[hand_line[0]]
        lower_landmark = self.landmarks.landmark[hand_line[1]]

        image_height, image_width, _ = image_shape

        # Finger coordinates to the image top left corner (default).
        finger_x = top_landmark.x * image_width
        finger_y = top_landmark.y * image_height

        # New coordinates center.
        center_x = lower_landmark.x * image_width
        center_y = lower_landmark.y * image_height

        # Finger coordinates to the image center.
        finger_x = center_x - finger_x
        finger_y = center_y - finger_y

        return degrees(atan2(finger_y, finger_x))


class HandsState:
    def __init__(self, image: ndarray) -> None:
        self.image = image
        self.hands = []

    def clear_detected_hands(self) -> None:
        self.hands.clear()

    def add_new_hand(self, hand: HandState) -> None:
        self.hands.append(hand)
