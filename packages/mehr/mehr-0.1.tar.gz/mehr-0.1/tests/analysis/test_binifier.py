import pytest

from mehr.analysis.mifs import binifier


@pytest.mark.parametrize("center,min_,max_,bin_width,low,high", [
    (0.5, 0, 1, 1, 0, 1),
    (0.5, 0.1, 0.9, 1, 0, 1),
    (0.5, -0.1, 1.1, 1, -1, 2),
    (3.14, 1, 7, 0.5, 0.89, 7.39)
])
def test_binifier(center, min_, max_, bin_width, low, high):
    bin_edges = binifier(center, min_, max_, bin_width)
    
    bin_edges[0] == pytest.approx(low)
    bin_edges[-1] == pytest.approx(high)