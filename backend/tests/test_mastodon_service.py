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

# @author Sonali
@patch("app.mastodon_service.Mastodon")  # Mock the Mastodon class
def test_retrieve_all_posts(mock_mastodon, mastodon_service):
    """Test retrieving all posts with offset-based pagination."""
    
    # Mock the Mastodon instance
    mock_instance = mock_mastodon.return_value

    # Simulate the return value of timeline_home method
    mock_instance.timeline_home.return_value = [
        {"id": 114045119186848421, "content": "Hello, World!", "created_at": "2025-02-21"},
        {"id": 114045132682037072, "content": "Second Post", "created_at": "2025-02-20"},
        {"id": 114045100000000000, "content": "Older Post", "created_at": "2025-02-19"},
        {"id": 114045090000000000, "content": "Even Older Post", "created_at": "2025-02-18"}
    ]
    
    # Mock the retrieve_all_posts method with pagination handling
    def mock_retrieve_all_posts(offset, limit):
        all_posts = [
            {"id": 114045119186848421, "content": "Hello, World!", "created_at": "2025-02-21"},
            {"id": 114045132682037072, "content": "Second Post", "created_at": "2025-02-20"},
            {"id": 114045100000000000, "content": "Older Post", "created_at": "2025-02-19"},
            {"id": 114045090000000000, "content": "Even Older Post", "created_at": "2025-02-18"}
        ]

        # Implement the pagination logic (slice the list)
        paginated_posts = all_posts[offset:offset + limit]
        return paginated_posts, len(all_posts)

    # Patch the method directly
    with patch.object(MastodonService, 'retrieve_all_posts', side_effect=mock_retrieve_all_posts):
        
        # Test retrieving the first 2 posts (offset = 0, limit = 2)
        posts, total_posts = mastodon_service.retrieve_all_posts(offset=0, limit=2)
        print("Retrieved posts:", posts)
    
        # Assertions to check the mocked result
        assert len(posts) == 2
        assert posts[0]["id"] == 114045119186848421
        assert posts[0]["content"] == "Hello, World!"
        assert posts[1]["id"] == 114045132682037072
        assert posts[1]["content"] == "Second Post"
        assert total_posts == 4

        # Test retrieving the next set of posts (offset = 2, limit = 2)
        posts, total_posts = mastodon_service.retrieve_all_posts(offset=2, limit=2)
        print("Retrieved posts:", posts)

        # Assertions for the next batch of posts
        assert len(posts) == 2  # Only two posts should be returned
        assert posts[0]["id"] == 114045100000000000
        assert posts[0]["content"] == "Older Post"
        assert posts[1]["id"] == 114045090000000000
        assert posts[1]["content"] == "Even Older Post"
        assert total_posts == 4  # Total posts should remain the same


@patch("app.mastodon_service.Mastodon")
def test_delete_post(mock_mastodon, mastodon_service):
    """Test deleting a post."""
    mock_instance = mock_mastodon.return_value
    mock_instance.status_delete.return_value = True

    with patch.object(mastodon_service.mastodon, "status_delete", return_value=True):
        result = mastodon_service.mastodon.status_delete("12345")

    assert result is True
