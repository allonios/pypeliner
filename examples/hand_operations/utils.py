from copy import deepcopy
from enum import Enum
from math import cos, sin


class Orientation(Enum):
    UNIDENTIFIED = "unidentified"
    LEFT = "left"
    RIGHT = "right"
    UP = "up"
    DOWN = "down"

    def __str__(self):
        return self.value


FINGERS_INDEXES = {1: 4, 2: 8, 3: 12, 4: 16, 5: 20}


def get_rotate_landmarks(landmarks, degree):
    rotated_landmarks = deepcopy(landmarks)
    for landmark in rotated_landmarks:
        rotated_x = landmark.x * cos(degree) + landmark.y * sin(degree)
        rotated_y = landmark.y * cos(degree) - landmark.x * sin(degree)
        landmark.x = rotated_x
        landmark.y = rotated_y
    return rotated_landmarks


class FingerLandmarksPairsFactory:
    @classmethod
    def get_thumb_orientation_after_rotation(cls, wrist, thumb):
        if wrist.x > thumb.x:
            return Orientation.LEFT
        else:
            return Orientation.RIGHT

    @classmethod
    def get_fingers_landmarks_pairs(cls, hand) -> dict:
        orientation = cls.get_thumb_orientation_after_rotation(
            hand.rotated_landmarks[0], hand.rotated_landmarks[1]
        )
        if orientation == Orientation.LEFT:

            def thumb_comparator(point1, point2):
                return point1.x > point2.x

        else:

            def thumb_comparator(point1, point2):
                return point1.x < point2.x

        fingers_landmarks_pairs = {
            4: {"threshold": 3, "comparator": thumb_comparator},
            8: {
                "threshold": 6,
                "comparator": lambda point1, point2: point1.y > point2.y,
            },
            12: {
                "threshold": 10,
                "comparator": lambda point1, point2: point1.y > point2.y,
            },
            16: {
                "threshold": 14,
                "comparator": lambda point1, point2: point1.y > point2.y,
            },
            20: {
                "threshold": 18,
                "comparator": lambda point1, point2: point1.y > point2.y,
            },
        }

        return fingers_landmarks_pairs
