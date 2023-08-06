import pytest
from compare_frames_g4 import compare_frames


def test_1():
    assert compare_frames('tests/frames_compareFrames/frame_1.png',
                          'tests/frames_compareFrames/frame_1_good.png'
                          ) is True

    assert compare_frames('tests/frames_compareFrames/frame_1.png',
                          'tests/frames_compareFrames/frame_1_bad.png'
                          ) is False
