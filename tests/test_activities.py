"""
Test GET /activities endpoint
"""


def test_get_activities_returns_all_activities(test_client):
    """
    Arrange: Use test client
    Act: Call GET /activities
    Assert: Verify all activities are returned with correct structure
    """
    # Arrange
    expected_activities = ["Chess Club", "Programming Class", "Gym Class", 
                         "Basketball Team", "Volleyball Club", "Debate Team",
                         "Science Olympiad", "Art Club", "Music Ensemble"]
    
    # Act
    response = test_client.get("/activities")
    data = response.json()
    
    # Assert
    assert response.status_code == 200
    assert isinstance(data, dict)
    assert len(data) == len(expected_activities)
    for activity_name in expected_activities:
        assert activity_name in data
        assert "description" in data[activity_name]
        assert "schedule" in data[activity_name]
        assert "max_participants" in data[activity_name]
        assert "participants" in data[activity_name]
        assert isinstance(data[activity_name]["participants"], list)


def test_get_activities_has_participants(test_client):
    """
    Arrange: Use test client
    Act: Call GET /activities
    Assert: Verify activities contain participant data
    """
    # Arrange/Act
    response = test_client.get("/activities")
    data = response.json()
    
    # Assert
    assert data["Chess Club"]["participants"] == ["michael@mergington.edu", "daniel@mergington.edu"]
    assert data["Programming Class"]["participants"] == ["emma@mergington.edu", "sophia@mergington.edu"]
