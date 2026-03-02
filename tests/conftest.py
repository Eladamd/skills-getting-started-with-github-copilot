import copy
import pytest
from fastapi.testclient import TestClient

from src.app import app, activities


# Keep an original deep copy of activities to restore between tests
_original_activities = copy.deepcopy(activities)


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture(autouse=True)
def reset_activities():
    # Arrange: restore in-memory activities to original state
    activities.clear()
    activities.update(copy.deepcopy(_original_activities))
    yield