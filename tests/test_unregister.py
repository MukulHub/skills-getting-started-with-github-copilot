"""
Test DELETE /activities/{activity_name}/signup endpoint
"""


def test_unregister_participant_success(test_client):
    """
    Arrange: Verify participant exists, then unregister
    Act: Call DELETE unregister endpoint
    Assert: Verify participant is removed successfully
    """
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"  # Already registered
    
    # Verify participant exists before deletion
    activities_before = test_client.get("/activities").json()
    assert email in activities_before[activity]["participants"]
    
    # Act
    response = test_client.delete(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity}"
    
    # Verify participant was removed
    activities_after = test_client.get("/activities").json()
    assert email not in activities_after[activity]["participants"]


def test_unregister_nonexistent_activity_returns_404(test_client):
    """
    Arrange: Use non-existent activity name
    Act: Call DELETE unregister endpoint
    Assert: Verify 404 error is returned
    """
    # Arrange
    activity = "NonExistent Club"
    email = "student@mergington.edu"
    
    # Act
    response = test_client.delete(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_nonregistered_participant_returns_400(test_client):
    """
    Arrange: Use email not registered for activity
    Act: Try to unregister non-existent participant
    Assert: Verify 400 error is returned
    """
    # Arrange
    activity = "Chess Club"
    email = "notregistered@mergington.edu"
    
    # Act
    response = test_client.delete(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student not registered for this activity"


def test_unregister_then_signup_again(test_client):
    """
    Arrange: Register participant, unregister, then try to register again
    Act: Perform signup -> unregister -> signup sequence
    Assert: All operations succeed
    """
    # Arrange
    activity = "Chess Club"
    email = "tempstudent@mergington.edu"
    
    # Act: First signup
    signup1 = test_client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    
    # Act: Unregister
    unregister = test_client.delete(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    
    # Act: Signup again
    signup2 = test_client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    
    # Assert
    assert signup1.status_code == 200
    assert unregister.status_code == 200
    assert signup2.status_code == 200
    
    # Verify participant is registered
    activities = test_client.get("/activities").json()
    assert email in activities[activity]["participants"]
