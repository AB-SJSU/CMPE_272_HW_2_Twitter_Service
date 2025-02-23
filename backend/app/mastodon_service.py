from mastodon import Mastodon
import logging
from app.config import Config

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MastodonService:
    """Handles interactions with the Mastodon API"""
    
    def __init__(self):
        self.mastodon = Mastodon(
            access_token=Config.ACCESS_TOKEN,
            api_base_url=Config.API_BASE_URL
        )

    def create_post(self, content):
        """Creates a new Mastodon post."""
        try:
            post = self.mastodon.status_post(content)
            logger.info(f"Post created: {post['id']}")
            return post["id"]
        except Exception as e:
            logger.error(f"Error creating post: {e}")
            return None

    def retrieve_post(self, post_id):
        """Retrieves a specific Mastodon post by ID."""
        try:
            post = self.mastodon.status(post_id)
            logger.info(f"Post retrieved: {post_id}")
            return post
        except Exception as e:
            logger.error(f"Error retrieving post {post_id}: {e}")
            return None

    def delete_post(self, post_id):
        """Deletes a specific Mastodon post by ID."""
        try:
            self.mastodon.status_delete(post_id)
            logger.info(f"Post {post_id} deleted successfully.")
            return True
        except Exception as e:
            logger.error(f"Error deleting post {post_id}: {e}")
            return False
        
    
