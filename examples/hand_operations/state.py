from math import atan2, degrees, radians
from typing import List

from mediapipe.framework.formats.landmark_pb2 import NormalizedLandmarkList
from numpy import ndarray

from examples.hand_operations.utils import (
    FINGERS_INDEXES,
    FingerLandmarksPairsFactory,
    Orientation,
    get_rotate_landmarks,
)


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


class Hand:
    def __init__(self, id, hand_landmarks, hand_type, image):
        self.id = id
        self.landmarks = hand_landmarks
        self.hand_type = hand_type
        self.image = image
        self.thumb_orientation = Orientation.UNIDENTIFIED
        self.orientation = Orientation.UNIDENTIFIED
        self.identify_hand_orientation()
        self.identify_thumb_orientation()

    def identify_hand_orientation(self):
        degree = self.get_hand_rotation_degrees()

        if -135 < degree < -45:
            self.orientation = Orientation.DOWN
        elif 45 < degree < 135:
            self.orientation = Orientation.UP
        elif -45 < degree < 45:
            self.orientation = Orientation.LEFT
        else:
            self.orientation = Orientation.RIGHT

    def identify_thumb_orientation(self):
        wrist = self.landmarks.landmark[0]
        thumb = self.landmarks.landmark[2]
        if (
            self.orientation == Orientation.UP
            or self.orientation == Orientation.DOWN
        ):
            if thumb.x < wrist.x:
                self.thumb_orientation = Orientation.LEFT
            else:
                self.thumb_orientation = Orientation.RIGHT

        if (
            self.orientation == Orientation.LEFT
            or self.orientation == Orientation.RIGHT
        ):
            if thumb.y > wrist.y:
                self.thumb_orientation = Orientation.DOWN
            else:
                self.thumb_orientation = Orientation.UP

    def get_hand_rotation_degrees(self):
        middle_finger_tip = self.landmarks.landmark[9]
        hand_center = self.landmarks.landmark[0]

        image_height, image_width, _ = self.image.shape

        # Finger coordinates to the image top left corner (default).
        finger_x = middle_finger_tip.x * image_width
        finger_y = middle_finger_tip.y * image_height

        # New coordinates center.
        center_x = hand_center.x * image_width
        center_y = hand_center.y * image_height

        # Finger coordinates to the image center.
        finger_x = center_x - finger_x
        finger_y = center_y - finger_y

        return degrees(atan2(finger_y, finger_x))

    def is_closed_finger(self, landmark_index: int):
        fingers_landmarks_pairs = (
            FingerLandmarksPairsFactory.get_fingers_landmarks_pairs(self)
        )
        point1_index = landmark_index
        point2_index = fingers_landmarks_pairs[landmark_index]["threshold"]
        comparator = fingers_landmarks_pairs[landmark_index]["comparator"]
        return comparator(
            self.rotated_landmarks[point1_index],
            self.rotated_landmarks[point2_index],
        )

    def get_raised_fingers(self):
        raised = []
        rotation = self.get_hand_rotation_degrees()
        rotated_landmarks = get_rotate_landmarks(
            self.landmarks.landmark, radians(rotation - 90)
        )
        self.rotated_landmarks = rotated_landmarks
        for finger_id, finger_landmark in FINGERS_INDEXES.items():
            if not self.is_closed_finger(finger_landmark):
                raised.append(finger_id)

        return raised
