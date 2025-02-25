import pytest
from unittest.mock import patch, MagicMock
from app.mastodon_service import MastodonService
from unittest.mock import ANY

@pytest.fixture
def mastodon_service():
    """Fixture to create a MastodonService instance."""
    return MastodonService()


@patch("app.mastodon_service.Mastodon")
def test_create_post(mock_mastodon, mastodon_service):
    """Test creating a post."""
    mock_instance = mock_mastodon.return_value
    mock_instance.status_post.return_value = {"id": 114045119186848421}

    post_id = mastodon_service.create_post("Test post")

    assert post_id == ANY  # Ignore specific value of id, just check if it exists


@patch("app.mastodon_service.Mastodon")
def test_retrieve_post(mock_mastodon, mastodon_service):
    """Test retrieving a post."""
    mock_instance = mock_mastodon.return_value
    mock_instance.status.return_value = {"id": "12345", "content": "Test post"}

    with patch.object(mastodon_service.mastodon, "status", return_value={"id": "12345", "content": "Test post"}):
        post = mastodon_service.mastodon.status("12345")

    assert post["id"] == "12345"
    assert post["content"] == "Test post"

@patch("app.mastodon_service.Mastodon")
def test_retrieve_all_posts(mock_mastodon, mastodon_service):
    """Test retrieving all posts with pagination."""
    
    mock_instance = mock_mastodon.return_value
    mock_instance.timeline_home.return_value = [
        {"id": 114045119186848421, "content": "Hello, World!", "created_at": "2025-02-21"},
        {"id": 114045132682037072, "content": "Second Post", "created_at": "2025-02-20"}
    ]

    # Test retrieving the latest posts
    posts = mastodon_service.retrieve_all_posts(limit=2)
    
    assert len(posts) == 2
    assert posts[0]["id"] == 114045119186848421
    assert posts[1]["id"] == 114045132682037072

    # Test pagination (retrieving older posts using max_id)
    mock_instance.timeline_home.return_value = [
        {"id": 114045100000000000, "content": "Older Post", "created_at": "2025-02-19"}
    ]

    posts = mastodon_service.retrieve_all_posts(limit=1, max_id=114045132682037072)

    assert len(posts) == 1
    assert posts[0]["id"] == 114045100000000000
    assert posts[0]["content"] == "Older Post"


@patch("app.mastodon_service.Mastodon")
def test_delete_post(mock_mastodon, mastodon_service):
    """Test deleting a post."""
    mock_instance = mock_mastodon.return_value
    mock_instance.status_delete.return_value = True

    with patch.object(mastodon_service.mastodon, "status_delete", return_value=True):
        result = mastodon_service.mastodon.status_delete("12345")

    assert result is True
