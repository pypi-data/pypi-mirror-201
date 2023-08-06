import os
import pytest
from ..conftest import FIXTURE_DIR
from pathlib import Path
import requests
from geovisio_cli import sequence
from datetime import timedelta


@pytest.mark.datafiles(
    os.path.join(FIXTURE_DIR, "e1.jpg"),
    os.path.join(FIXTURE_DIR, "e2.jpg"),
    os.path.join(FIXTURE_DIR, "e3.jpg"),
)
def test_valid_upload(geovisio, datafiles):
    collection = sequence.upload(path=Path(datafiles), geovisio=geovisio)

    assert len(collection.uploaded_pictures) == 3
    assert len(collection.errors) == 0

    sequence.wait_for_sequence(collection.location, timeout=timedelta(minutes=1))
    status = sequence.status(collection.location)
    sequence_info = sequence.info(collection.location)
    # 3 pictures should have been uploaded
    assert len(status.pictures) == 3

    for i in status.pictures:
        assert i.status == "ready"

    # the collection should also have 3 items
    collection = requests.get(f"{collection.location}/items")
    collection.raise_for_status()

    features = collection.json()["features"]
    assert len(features) == 3

    assert sequence_info.title == "test_valid_upload0"
    assert sequence_info.interior_orientation == [
        sequence.InteriorOrientation(
            make="SONY", model="FDR-X1000V", field_of_view=None
        )
    ]


@pytest.mark.datafiles(
    os.path.join(FIXTURE_DIR, "e1.jpg"),
    os.path.join(FIXTURE_DIR, "e2.jpg"),
    os.path.join(FIXTURE_DIR, "e3.jpg"),
    os.path.join(FIXTURE_DIR, "invalid_pic.jpg"),
)
def test_upload_with_invalid_file(geovisio, datafiles):
    collection = sequence.upload(path=Path(datafiles), geovisio=geovisio)

    # Only 3 pictures should have been uploaded, 1 is in error
    assert len(collection.uploaded_pictures) == 3
    assert len(collection.errors) == 1

    # But the collection status should have 3 items (and be valid)
    sequence.wait_for_sequence(collection.location, timeout=timedelta(minutes=1))
    status = sequence.status(collection.location)
    # 3 pictures should have been uploaded
    assert len(status.pictures) == 3

    assert all([i.status == "ready" for i in status.pictures])

    # the collection should also have 3 items
    collection = requests.get(f"{collection.location}/items")
    collection.raise_for_status()
    features = collection.json()["features"]
    assert len(features) == 3


@pytest.mark.datafiles(
    os.path.join(FIXTURE_DIR, "invalid_pic.jpg"),
)
def test_upload_with_no_valid_file(geovisio, datafiles):
    collection = sequence.upload(path=Path(datafiles), geovisio=geovisio)

    assert len(collection.uploaded_pictures) == 0
    assert len(collection.errors) == 1

    status = requests.get(f"{collection.location}/geovisio_status")
    assert (
        status.status_code == 404
    )  # TODO: For the moment geovisio return a 404, we it should return a valid status response with the sequence status

    items = requests.get(f"{collection.location}/items")
    items.raise_for_status()
    features = items.json()["features"]
    assert len(features) == 0
