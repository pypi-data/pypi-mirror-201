import pytest
import os
import cv2

from motion_detector_g4 import MotionDetector
from utilspy_g4 import templated_remove_files


def _remove_temp_files() -> None:
    """
    Remove temp files
    :rtype: None
    :return: None
    """

    templated_remove_files('tests/images/*.clear.*')
    templated_remove_files('tests/images/*.mask.*')
    templated_remove_files('tests/images/*.blobs.*')
    templated_remove_files('tests/images/*.blobs2.*')


def test_1():
    _remove_temp_files()

    md = MotionDetector()
    md.apply_first_frame('tests/images/01_frame_1.png')
    md.check_motion('tests/images/01_frame_2.png')
    assert os.path.exists('tests/images/01_frame_2.clear.png') is False
    assert os.path.exists('tests/images/01_frame_2.mask.png') is False
    assert os.path.exists('tests/images/01_frame_2.blobs.png') is False
    assert os.path.exists('tests/images/01_frame_2.blobs2.png') is False
    _remove_temp_files()


def test_2():
    md = MotionDetector(debug=True)
    md.apply_first_frame('tests/images/01_frame_1.png')
    md.check_motion('tests/images/01_frame_2.png')
    assert os.path.exists('tests/images/01_frame_2.clear.png') is True
    assert os.path.exists('tests/images/01_frame_2.mask.png') is True
    assert os.path.exists('tests/images/01_frame_2.blobs.png') is False
    assert os.path.exists('tests/images/01_frame_2.blobs2.png') is False
    _remove_temp_files()


def test_3():
    md = MotionDetector(min_area=2000, debug=True)
    md.apply_first_frame('tests/images/01_frame_1.png')
    md.check_motion('tests/images/01_frame_2.png')
    assert os.path.exists('tests/images/01_frame_2.clear.png') is True
    assert os.path.exists('tests/images/01_frame_2.mask.png') is True
    assert os.path.exists('tests/images/01_frame_2.blobs.png') is True
    assert os.path.exists('tests/images/01_frame_2.blobs2.png') is True
    _remove_temp_files()


def test_mask():
    md = MotionDetector(debug=True)
    md.apply_first_frame('tests/images/01_frame_1.png')
    md.check_motion('tests/images/01_frame_2.png')

    frame_mask = cv2.imread('tests/images/01_frame_2.mask.png')

    (b, g, r) = frame_mask[17, 65]
    assert int(r) + int(g) + int(b) == 765

    (b, g, r) = frame_mask[38, 36]
    assert int(r) + int(g) + int(b) == 0

    (b, g, r) = frame_mask[104, 1713]
    assert int(r) + int(g) + int(b) == 765

    (b, g, r) = frame_mask[53, 1752]
    assert int(r) + int(g) + int(b) == 0

    (b, g, r) = frame_mask[881, 1868]
    assert int(r) + int(g) + int(b) == 765

    (b, g, r) = frame_mask[877, 1834]
    assert int(r) + int(g) + int(b) == 0

    (b, g, r) = frame_mask[1002, 62]
    assert int(r) + int(g) + int(b) == 765

    (b, g, r) = frame_mask[994, 140]
    assert int(r) + int(g) + int(b) == 0

    _remove_temp_files()


def test_clear():
    md = MotionDetector(debug=True)
    md.apply_first_frame('tests/images/01_frame_1.png')
    md.check_motion('tests/images/01_frame_2.png')

    frame_clear = cv2.imread('tests/images/01_frame_2.clear.png')

    (b, g, r) = frame_clear[17, 65]
    assert int(r) + int(g) + int(b) == 0

    (b, g, r) = frame_clear[38, 36]
    assert int(r) + int(g) + int(b) == 0

    (b, g, r) = frame_clear[104, 1713]
    assert int(r) + int(g) + int(b) == 0

    (b, g, r) = frame_clear[53, 1752]
    assert int(r) + int(g) + int(b) == 0

    (b, g, r) = frame_clear[881, 1868]
    assert int(r) + int(g) + int(b) == 765

    (b, g, r) = frame_clear[877, 1834]
    assert int(r) + int(g) + int(b) == 0

    (b, g, r) = frame_clear[1002, 62]
    assert int(r) + int(g) + int(b) == 0

    (b, g, r) = frame_clear[994, 140]
    assert int(r) + int(g) + int(b) == 0

    _remove_temp_files()
