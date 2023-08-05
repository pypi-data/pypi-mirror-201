import pytest

from io import BytesIO, SEEK_CUR, SEEK_END, SEEK_SET
from mehr.stream import StreamProgressWrapper

LINE_ODD = b"QWERTZUIOP\n"
LINE_EVEN = b"ASDFGHJKLYXCVBNM\n"

NUM_LINE_REPEAT = 10_000

NUM_SMALL_READ = 8

FIRST_SEEK = 40
SECOND_SEEK = 20
THIRD_SEEK = -50

EXPECTED_SIZE = 420

BAD_SEEK_MODE_VALUES = [-1, -42, 3]
BAD_SEEK_MODE_TYPES = [1.0, "2", b"1"]


def bytes_stream():
    stream = BytesIO()
    for _ in range(NUM_LINE_REPEAT):
        stream.write(LINE_ODD)
        stream.write(LINE_EVEN)
    stream.seek(0)
    final_pos = NUM_LINE_REPEAT * (len(LINE_ODD) + len(LINE_EVEN))

    return stream, final_pos


def test_read():
    stream, _ = bytes_stream()
    with StreamProgressWrapper(stream) as f:
        data = f.read(NUM_SMALL_READ)

    assert data == LINE_ODD[:NUM_SMALL_READ]


def test_seek_tell():
    stream, final_pos = bytes_stream()

    with StreamProgressWrapper(stream) as f:
        assert f.tell() == 0
        f.seek(FIRST_SEEK)
        assert f.tell() == FIRST_SEEK
        f.seek(SECOND_SEEK, SEEK_CUR)
        assert f.tell() == FIRST_SEEK + SECOND_SEEK
        f.seek(THIRD_SEEK, SEEK_END)
        assert f.tell() == final_pos + THIRD_SEEK


def test_bad_seek_mode_values():
    for bad_mode in BAD_SEEK_MODE_VALUES:
        stream, _ = bytes_stream()
        with StreamProgressWrapper(stream) as f:
            with pytest.raises(ValueError):
                f.seek(FIRST_SEEK, bad_mode)


def test_bad_seek_mode_types():
    for bad_mode in BAD_SEEK_MODE_TYPES:
        stream, _ = bytes_stream()
        with StreamProgressWrapper(stream) as f:
            with pytest.raises(TypeError):
                f.seek(FIRST_SEEK, bad_mode)
        assert f.closed


def test_neg_seek_position():
    stream, final_pos = bytes_stream()
    with StreamProgressWrapper(stream) as f:
        with pytest.raises(ValueError):
            f.seek(-1, SEEK_SET)


def test_far_seek():
    stream, final_pos = bytes_stream()
    with StreamProgressWrapper(stream) as f:
        pos = f.seek(final_pos * 100, SEEK_SET)
        assert pos == final_pos * 100
        rest_data = f.read(NUM_SMALL_READ)
        assert rest_data == b""


def test_close():
    stream, final_pos = bytes_stream()
    with StreamProgressWrapper(stream) as f:
        f.close()

    assert f.closed
    assert stream.closed


def test_guessed_size():
    stream, final_pos = bytes_stream()
    with StreamProgressWrapper(stream, guess_size=True) as f:
        assert f.size == final_pos


def test_expected_size():
    stream, final_pos = bytes_stream()
    with StreamProgressWrapper(stream, expected_size=EXPECTED_SIZE) as f:
        assert f.size == EXPECTED_SIZE


def test_readline():
    stream, final_pos = bytes_stream()
    with StreamProgressWrapper(stream) as f:
        line_odd = f.readline()
        assert line_odd == LINE_ODD
        line_even = f.readline()
        assert line_even == LINE_EVEN
        line_odd2 = f.readline()
        assert line_odd2 == LINE_ODD
        line_even2 = f.readline()
        assert line_even2 == LINE_EVEN


def test_readlines():
    stream, final_pos = bytes_stream()
    with StreamProgressWrapper(stream) as f:
        lines = f.readlines(2 * len(LINE_ODD) + 2 * len(LINE_EVEN))
        assert len(lines) == 4
        assert lines[0] == LINE_ODD
        assert lines[1] == LINE_EVEN
        assert lines[2] == LINE_ODD
        assert lines[3] == LINE_EVEN
