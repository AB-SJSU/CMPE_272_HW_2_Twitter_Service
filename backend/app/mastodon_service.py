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

    def user_profile_get(self):
        """Get user information"""
        try:
            user = self.mastodon.account_verify_credentials()
            logger.debug("User profile", user)
            return {
                "id": user["id"],
                "username": user["username"],
                "display_name": user["display_name"],
                "created_at": user["created_at"],
                "statuses_count": user["statuses_count"],
                "followers_count": user["followers_count"],
                "following_count": user["following_count"],
                "avatar": user["avatar"],
                "header": user["header"],
                "bio": user["note"]
            }
            
        except Exception as e:
            logger.error(f"Error creating post: {e}")
            return None
        
    def create_post(self, content):
        """Creates a new Mastodon post."""
        try:
            post = self.mastodon.status_post(content)
            logger.info(f"Post created:{post['id']}")
            return {"id": post["id"], "content": post["content"]}
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
        
    def retrieve_all_posts(self, limit=10, max_id=None):
        try:
            params = {"limit": limit}
            if max_id:
                params["max_id"] = max_id  # Get older posts

            print("DEBUG: Fetching posts with params:", params)
            posts = self.mastodon.timeline_home(**params)
            return posts if posts else []
        except Exception as e:
            print("ERROR: Failed to fetch posts:", str(e))
            return []

    def delete_post(self, post_id):
        """Deletes a specific Mastodon post by ID."""
        try:
            self.mastodon.status_delete(post_id)
            logger.info(f"Post {post_id} deleted successfully.")
            return True
        except Exception as e:
            logger.error(f"Error deleting post {post_id}: {e}")
            return False
        
    
