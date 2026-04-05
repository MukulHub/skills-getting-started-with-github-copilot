"""
Pytest configuration and fixtures for API tests
"""
import copy
from fastapi.testclient import TestClient
import pytest
from src.app import app, activities


@pytest.fixture
def test_client():
    """Provide a TestClient for API testing"""
    return TestClient(app)


@pytest.fixture
def test_activities():
    """
    Provide a deep copy of activities for each test
    to ensure test isolation and prevent state pollution
    """
    return copy.deepcopy(activities)


@pytest.fixture(autouse=True)
def reset_activities(test_activities, monkeypatch):
    """
    Automatically reset the activities module variable
    before each test to ensure isolation
    """
    monkeypatch.setattr("src.app.activities", test_activities)
