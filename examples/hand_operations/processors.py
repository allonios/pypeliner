from math import radians
from typing import Any

import cv2
import mediapipe as mp

from examples.hand_operations.state import HandsState, HandState
from examples.hand_operations.utils import (
    FINGERS_INDEXES,
    FingerLandmarksPairsFactory,
    Orientation,
    get_rotate_landmarks,
)
from pypeliner.processors.base import BaseProcessor

mp_hands = mp.solutions.hands


class HandLandmarksProcessor(BaseProcessor):
    def __init__(
        self,
        init_state: HandsState = None,
        max_num_hands: int = 2,
        min_detection_confidence: float = 0.4,
        min_tracking_confidence: float = 0.3,
        mirror_image: bool = True,
    ) -> None:
        super().__init__(init_state)
        self.max_num_hands = max_num_hands
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence
        self.mirror_image = mirror_image

    def process(self, input_state: Any = None) -> HandsState:
        self.state = super().process(input_state)

        # clear out previously detected hands.
        self.state.clear_detected_hands()

        with mp_hands.Hands(
            max_num_hands=self.max_num_hands,
            min_detection_confidence=self.min_detection_confidence,
            min_tracking_confidence=self.min_tracking_confidence,
        ) as hands_solution:
            self.state.image.flags.writeable = False
            self.state.image = cv2.cvtColor(
                self.state.image, cv2.COLOR_BGR2RGB
            )

            if self.mirror_image:
                self.state.image = cv2.flip(self.state.image, 1)

            results = hands_solution.process(self.state.image)

            self.state.image.flags.writeable = True
            self.state.image = cv2.cvtColor(
                self.state.image, cv2.COLOR_RGB2BGR
            )

            if results.multi_hand_landmarks:
                # hand_info[0]: hand_landmarks
                # hand_info[1]: hand_type
                for index, hand_info in enumerate(
                    zip(results.multi_hand_landmarks, results.multi_handedness)
                ):
                    hand = HandState(index, hand_info[0], hand_info[1])
                    self.state.add_new_hand(hand)

        return self.state


class HandOrientationProcessor(BaseProcessor):
    def __init__(
        self,
        init_state: Any = None,
        hand_line: tuple = (9, 0),
    ) -> None:
        super().__init__(init_state)
        self.hand_line = hand_line

    def identify_hand_orientation(
        self,
        hand: HandState,
        image_shape: tuple,
    ) -> Orientation:
        degree = hand.get_hand_rotation_degrees(self.hand_line, image_shape)

        if -135 < degree < -45:
            return Orientation.DOWN
        elif 45 < degree < 135:
            return Orientation.UP
        elif -45 < degree < 45:
            return Orientation.LEFT
        else:
            return Orientation.RIGHT

    def process(self, input_state: HandState = None) -> HandsState:
        self.state = super().process(input_state)

        for hand in self.state.hands:
            hand.orientation = self.identify_hand_orientation(
                hand, self.state.image.shape
            )

        return self.state


class HandThumbOrientationProcessor(BaseProcessor):
    def __init__(
        self,
        init_state: HandsState = None,
        thumb_line: tuple = (0, 2),
    ) -> None:
        super().__init__(init_state)
        self.thumb_line = thumb_line

    def identify_thumb_orientation(self, hand: HandState):
        wrist = hand.landmarks.landmark[self.thumb_line[0]]
        thumb = hand.landmarks.landmark[self.thumb_line[1]]
        if (
            hand.orientation == Orientation.UP
            or hand.orientation == Orientation.DOWN
        ):
            if thumb.x < wrist.x:
                return Orientation.LEFT
            else:
                return Orientation.RIGHT

        if (
            hand.orientation == Orientation.LEFT
            or hand.orientation == Orientation.RIGHT
        ):
            if thumb.y > wrist.y:
                return Orientation.DOWN
            else:
                return Orientation.UP

    def process(self, input_state: HandsState = None) -> HandsState:
        self.state = super().process(input_state)

        for hand in self.state.hands:
            hand.thumb_orientation = self.identify_thumb_orientation(hand)

        return self.state


class RaisedFingersProcessor(BaseProcessor):
    def __init__(
        self,
        init_state: Any = None,
        hand_line: tuple = (9, 0),
        thumb_line: tuple = (0, 2),
    ) -> None:
        super().__init__(init_state)
        self.hand_line = hand_line
        self.thumb_line = thumb_line

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

    def get_raised_fingers(self, hand: HandState):
        raised = []
        rotation = hand.get_hand_rotation_degrees(
            self.hand_line, self.state.image.shape
        )
        rotated_landmarks = get_rotate_landmarks(
            hand.landmarks.landmark, radians(rotation - 90)
        )
        self.rotated_landmarks = rotated_landmarks
        for finger_id, finger_landmark in FINGERS_INDEXES.items():
            if not self.is_closed_finger(finger_landmark):
                raised.append(finger_id)

        return raised

    def process(self, input_state: Any = None) -> Any:
        self.state = super().process(input_state)

        for hand in self.state.hands:
            hand.clear_raised_fingers()
            raised_fingers = self.get_raised_fingers(hand)
            hand.add_raised_fingers(raised_fingers)

        return self.state
