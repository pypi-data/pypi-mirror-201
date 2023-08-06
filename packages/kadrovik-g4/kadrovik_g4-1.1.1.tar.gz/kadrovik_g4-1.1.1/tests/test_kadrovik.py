import pytest
from kadrovik_g4 import Kadrovik
from utilspy_g4 import templated_remove_files
from compare_frames_g4 import compare_frames


def _remove_temp_files() -> None:
    """
    Remove temp files
    :rtype: None
    :return: None
    """

    templated_remove_files('tests/frames/*.png')


def test_1():
    kadrovik = Kadrovik()

    assert kadrovik.video == ''
    assert kadrovik.frame_n == 5
    assert kadrovik.out_path == 'frame_%d.png'


def test_2():
    kadrovik = Kadrovik(video='test.mp4', frame_n=10, out_path='test%d.png')

    assert kadrovik.video == 'test.mp4'
    assert kadrovik.frame_n == 10
    assert kadrovik.out_path == 'test%d.png'

    kadrovik.video = 'test2.mkv'
    kadrovik.frame_n = 15
    kadrovik.out_path = 'out_path/out_path.png'

    assert kadrovik.video == 'test2.mkv'
    assert kadrovik.frame_n == 15
    assert kadrovik.out_path == 'out_path/out_path.png'


def test_3():
    _remove_temp_files()

    kadrovik = Kadrovik(frame_n=5, out_path='tests/frames/frame_%d.png')
    kadrovik.process('tests/test.mp4')

    for i in [1, 2, 3, 4]:
        assert compare_frames('tests/frames/frame_%i.png' % i, 'tests/good_frames/frame_%i.png' % i)

    _remove_temp_files()


def test_print(capsys):
    kadrovik = Kadrovik(video='test.mp4', frame_n=10, out_path='test%d.png')
    print(kadrovik)
    captured = capsys.readouterr()
    assert captured.out == 'test.mp4 => test%d.png (10)\n'
