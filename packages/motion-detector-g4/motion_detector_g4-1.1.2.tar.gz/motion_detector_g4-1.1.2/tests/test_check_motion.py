import pytest
from motion_detector_g4 import MotionDetector


def test_01_1():
    md = MotionDetector()
    md.apply_first_frame('tests/images/01_frame_1.png')
    assert md.check_motion('tests/images/01_frame_2.png') is False


def test_01_2():
    md = MotionDetector()
    md.apply_first_frame('tests/images/01_frame_2.png')
    assert md.check_motion('tests/images/01_frame_3.png') is False


def test_01_3():
    md = MotionDetector()
    md.apply_first_frame('tests/images/01_frame_3.png')
    assert md.check_motion('tests/images/01_frame_4.png') is False


def test_01_4():
    md = MotionDetector(min_area=2000)
    md.apply_first_frame('tests/images/01_frame_1.png')
    assert md.check_motion('tests/images/01_frame_2.png') is True


def test_01_5():
    md = MotionDetector(min_area=2000)
    md.apply_first_frame('tests/images/01_frame_2.png')
    assert md.check_motion('tests/images/01_frame_3.png') is True


def test_01_6():
    md = MotionDetector(min_area=2000)
    md.apply_first_frame('tests/images/01_frame_1.png')
    assert md.check_motion('tests/images/01_frame_2.png') is True
    assert md.check_motion('tests/images/01_frame_3.png') is True


def test_01_7():
    md = MotionDetector()
    md.apply_first_frame('tests/images/01_frame_1.png')
    assert md.check_motion('tests/images/01_frame_2.png') is False
    assert md.check_motion('tests/images/01_frame_3.png') is False


def test_02_1():
    md = MotionDetector()
    md.apply_first_frame('tests/images/02_frame_1.png')
    assert md.check_motion('tests/images/02_frame_2.png') is False


def test_03_1():
    md = MotionDetector()
    md.apply_first_frame('tests/images/03_frame_1.bmp')
    assert md.check_motion('tests/images/03_frame_2.bmp') is False


def test_03_2():
    md = MotionDetector()
    md.apply_first_frame('tests/images/03_frame_1.bmp')
    assert md.check_motion('tests/images/03_frame_2.bmp') is False
    assert md.check_motion('tests/images/03_frame_3.bmp') is False


def test_03_3():
    md = MotionDetector()
    md.apply_first_frame('tests/images/03_frame_3.bmp')
    assert md.check_motion('tests/images/03_frame_4.bmp') is True
