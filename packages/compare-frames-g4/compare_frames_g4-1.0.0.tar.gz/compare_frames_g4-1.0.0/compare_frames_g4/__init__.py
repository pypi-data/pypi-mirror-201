import cv2


def compare_frames(frame_path_1: str, frame_path_2: str) -> bool:
    """
    Compare 2 frames

    :param frame_path_1: Path to frame 1
    :type frame_path_1: str
    :param frame_path_2: Path to frame 2
    :type frame_path_2: str
    :return: bool
    """

    # TODO: Check different frames size

    frame_1 = cv2.imread(frame_path_1)
    frame_2 = cv2.imread(frame_path_2)
    diff = cv2.norm(frame_1, frame_2, cv2.NORM_L2)

    if diff == 0.0:
        return True

    return False
