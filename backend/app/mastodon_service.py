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

    
