import pytest
import os
import cv2
from polyfiller_g4 import PolyFiller
from utilspy_g4 import templated_remove_files
from compare_frames_g4 import compare_frames


def _remove_temp_files() -> None:
    """
    Remove temp files
    :rtype: None
    :return: None
    """

    templated_remove_files('tests/images/*.fill.*')


def test_1():
    pf = PolyFiller()

    assert pf._ext == 'fill'
    assert pf._color == 0
    assert pf._polygons == []


def test_2():
    pf = PolyFiller('new_ext', (200, 100, 250))

    assert pf._ext == 'new_ext'
    assert pf._color == (200, 100, 250)
    assert pf._polygons == []


def test_3():
    pf = PolyFiller(color=(200, 100, 250), ext='new_ext')

    assert pf._ext == 'new_ext'
    assert pf._color == (200, 100, 250)
    assert pf._polygons == []


def test_4():
    pf = PolyFiller()

    pf.add_polygon([[10, 15], [25, 20], [15, 50]])
    assert pf._polygons == [[[10, 15], [25, 20], [15, 50]]]


def test_5():
    pf = PolyFiller()

    pf.add_polygon([[10, 15], [25, 20], [15, 50]])
    pf.add_polygon([[1, 2], [3, 4], [5, 6], [7, 8]])
    assert pf._polygons == [[[10, 15], [25, 20], [15, 50]], [[1, 2], [3, 4], [5, 6], [7, 8]]]


def test_6():
    _remove_temp_files()

    pf = PolyFiller()

    pf.fill('tests/images/frame_1.png')
    assert os.path.exists('tests/images/frame_1.fill.png') is True


def test_7():
    _remove_temp_files()

    pf = PolyFiller(ext='fill2')

    pf.fill('tests/images/frame_1.png')
    assert os.path.exists('tests/images/frame_1.fill2.png') is True


def test_8():
    _remove_temp_files()

    pf = PolyFiller()

    pf.fill('tests/images/frame_1.png')

    assert compare_frames('tests/images/frame_1.png', 'tests/images/frame_1.fill.png') is True


def test_9():
    _remove_temp_files()

    pf = PolyFiller()
    pf.add_polygon([[750, 500], [850, 500], [800, 600]])
    pf.add_polygon([[1000, 600], [1100, 650], [1200, 800], [900, 650]])
    pf.fill('tests/images/frame_1.png')

    frame_fill = cv2.imread('tests/images/frame_1.fill.png')

    (b, g, r) = frame_fill[530, 800]
    assert int(r) + int(g) + int(b) == 0

    (b, g, r) = frame_fill[640, 970]
    assert int(r) + int(g) + int(b) == 0

    (b, g, r) = frame_fill[730, 1123]
    assert int(r) + int(g) + int(b) == 0

    (b, g, r) = frame_fill[551, 771]
    assert int(r) + int(g) + int(b) == 309

    (b, g, r) = frame_fill[564, 824]
    assert int(r) + int(g) + int(b) == 321

    (b, g, r) = frame_fill[711, 1007]
    assert int(r) + int(g) + int(b) == 456

    (b, g, r) = frame_fill[672, 1123]
    assert int(r) + int(g) + int(b) == 477

    _remove_temp_files()


def test_10():
    _remove_temp_files()

    pf = PolyFiller(color=(100, 250, 50))
    pf.add_polygon([[750, 500], [850, 500], [800, 600]])
    pf.add_polygon([[1000, 600], [1100, 650], [1200, 800], [900, 650]])
    pf.fill('tests/images/frame_1.png')

    frame_fill = cv2.imread('tests/images/frame_1.fill.png')

    (b, g, r) = frame_fill[530, 800]
    assert int(r) + int(g) + int(b) == 400

    (b, g, r) = frame_fill[640, 970]
    assert int(r) + int(g) + int(b) == 400

    (b, g, r) = frame_fill[730, 1123]
    assert int(r) + int(g) + int(b) == 400

    (b, g, r) = frame_fill[551, 771]
    assert int(r) + int(g) + int(b) == 309

    (b, g, r) = frame_fill[564, 824]
    assert int(r) + int(g) + int(b) == 321

    (b, g, r) = frame_fill[711, 1007]
    assert int(r) + int(g) + int(b) == 456

    (b, g, r) = frame_fill[672, 1123]
    assert int(r) + int(g) + int(b) == 477

    _remove_temp_files()


def test_11():
    _remove_temp_files()

    pf = PolyFiller(color=(100, 250, 50))
    pf.add_polygon([[750, 500], [850, 500], [800, 600]])
    pf.add_polygon([[1000, 600], [1100, 650], [1200, 800], [900, 650]])
    pf.fill('tests/images/frame_1.png')
    pf.fill('tests/images/frame_2.png')

    frame_fill = cv2.imread('tests/images/frame_2.fill.png')

    (b, g, r) = frame_fill[530, 800]
    assert int(r) + int(g) + int(b) == 400

    (b, g, r) = frame_fill[640, 970]
    assert int(r) + int(g) + int(b) == 400

    (b, g, r) = frame_fill[730, 1123]
    assert int(r) + int(g) + int(b) == 400

    (b, g, r) = frame_fill[551, 771]
    assert int(r) + int(g) + int(b) == 318

    (b, g, r) = frame_fill[564, 824]
    assert int(r) + int(g) + int(b) == 315

    (b, g, r) = frame_fill[711, 1007]
    assert int(r) + int(g) + int(b) == 438

    (b, g, r) = frame_fill[672, 1123]
    assert int(r) + int(g) + int(b) == 483

    _remove_temp_files()
