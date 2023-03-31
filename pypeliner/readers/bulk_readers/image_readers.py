from pypeliner.exceptions import MissingDependency
from pypeliner.readers.bulk_readers.file_readers import FileReader

try:
    import cv2
    # if open-cv is installed then numpy is too since it is a
    # requirement.
    import numpy as np
    from numpy import ndarray
except ImportError:
    raise MissingDependency(
        "Image readers requires opencv-contrib-python==4.5.5.64 to be "
        "installed\nrun pip install opencv-contrib-python==4.5.5.64 "
        "to fix."
    )


class ImageFileReader(FileReader):
    def read(self) -> str:
        return cv2.imread(self.file_path)


class VideoFileReader(FileReader):
    def read(self) -> ndarray:
        cap = cv2.VideoCapture(self.file_path)

        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        frames = np.empty(
            (frame_count, frame_height, frame_width, 3), np.dtype("uint8")
        )

        loaded_frames = 0
        while loaded_frames < frame_count:
            success, frames[loaded_frames] = cap.read()
            if not success:
                raise ValueError("Error Reading Frame.")
            loaded_frames += 1

        return np.array(frames)
