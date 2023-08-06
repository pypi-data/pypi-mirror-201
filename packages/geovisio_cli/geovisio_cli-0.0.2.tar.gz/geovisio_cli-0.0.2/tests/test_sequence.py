import pytest
from geovisio_cli import sequence


@pytest.mark.parametrize(
    ("data", "expected"),
    (
        (["1.jpg", "2.jpg", "3.jpg"], ["1.jpg", "2.jpg", "3.jpg"]),
        (["3.jpg", "1.jpg", "2.jpg"], ["1.jpg", "2.jpg", "3.jpg"]),
        (["3.jpg", "1.jpg", "2.jpeg"], ["1.jpg", "2.jpeg", "3.jpg"]),
        (["10.jpg", "5.jpg", "1.jpg"], ["1.jpg", "5.jpg", "10.jpg"]),
        (["C.jpg", "A.jpg", "B.jpg"], ["A.jpg", "B.jpg", "C.jpg"]),
        (
            ["CAM1_001.jpg", "CAM2_002.jpg", "CAM1_002.jpg"],
            ["CAM1_001.jpg", "CAM1_002.jpg", "CAM2_002.jpg"],
        ),
    ),
)
def test_sort_files(data, expected):
    dataPictures = [sequence.Picture(path=p) for p in data]
    resPictures = sequence._sort_files(dataPictures)
    assert expected == [pic.path for pic in resPictures]
