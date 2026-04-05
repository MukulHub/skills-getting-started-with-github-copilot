"""
Test POST /activities/{activity_name}/signup endpoint
"""


def test_signup_new_participant_success(test_client):
    """
    Arrange: Prepare new student email and activity
    Act: Call POST signup endpoint
    Assert: Verify participant is added successfully
    """
    # Arrange
    activity = "Chess Club"
    email = "newstudent@mergington.edu"
    
    # Act
    response = test_client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity}"
    
    # Verify participant was added
    activities_response = test_client.get("/activities")
    participants = activities_response.json()[activity]["participants"]
    assert email in participants


def test_signup_nonexistent_activity_returns_404(test_client):
    """
    Arrange: Use non-existent activity name
    Act: Call POST signup endpoint
    Assert: Verify 404 error is returned
    """
    # Arrange
    activity = "NonExistent Club"
    email = "student@mergington.edu"
    
    # Act
    response = test_client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_duplicate_participant_returns_400(test_client):
    """
    Arrange: Use email already registered for activity
    Act: Try to signup same participant twice
    Assert: Verify 400 error is returned
    """
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"  # Already in participants
    
    # Act
    response = test_client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_multiple_activities_same_student(test_client):
    """
    Arrange: Student already in one activity
    Act: Sign up same student for different activity
    Assert: Verify signup succeeds for new activity
    """
    # Arrange
    student_email = "newstudent@mergington.edu"
    activity1 = "Chess Club"
    activity2 = "Basketball Team"
    
    # Act: Signup for first activity
    response1 = test_client.post(
        f"/activities/{activity1}/signup",
        params={"email": student_email}
    )
    
    # Act: Signup for second activity
    response2 = test_client.post(
        f"/activities/{activity2}/signup",
        params={"email": student_email}
    )
    
    # Assert
    assert response1.status_code == 200
    assert response2.status_code == 200
    
    # Verify in both activities
    activities_response = test_client.get("/activities")
    data = activities_response.json()
    assert student_email in data[activity1]["participants"]
    assert student_email in data[activity2]["participants"]
