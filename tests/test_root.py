"""
Test GET / endpoint redirect
"""


def test_root_redirects_to_static_index(test_client):
    """
    Arrange: Use test client
    Act: Call GET /
    Assert: Verify redirect to /static/index.html
    """
    # Arrange/Act
    response = test_client.get("/", follow_redirects=False)
    
    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_root_redirect_with_follow(test_client):
    """
    Arrange: Use test client with follow_redirects=True
    Act: Call GET / and follow redirect
    Assert: Verify final response is HTML (200 or HTML content-type)
    """
    # Arrange/Act
    response = test_client.get("/", follow_redirects=True)
    
    # Assert - StaticFiles endpoint returns 200 for index.html
    assert response.status_code == 200
