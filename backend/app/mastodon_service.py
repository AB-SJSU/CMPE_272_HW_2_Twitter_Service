from mastodon import Mastodon, MastodonRatelimitError, MastodonAPIError
import logging
from app.config import Config
import time
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

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
        self.last_request_time = 0
        self.min_request_interval = 0.2  # 200ms minimum interval between requests

    def _throttle_request(self):
        """Enforce minimum time between API requests"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        if time_since_last < self.min_request_interval:
            time.sleep(self.min_request_interval - time_since_last)
        self.last_request_time = time.time()

    def user_profile_get(self):
        """Get user information"""
        try:
            self._throttle_request()
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
        except MastodonRatelimitError:
            logger.error("API rate limit exceeded while fetching user profile.")
            return {"error": "API rate limit exceeded. Please try again later."}
        except MastodonAPIError as e:
            logger.error(f"Mastodon API error while fetching user profile: {e}")
            return {"error": f"Mastodon API error: {e}"}
        except Exception as e:
            logger.error(f"Error fetching user profile: {e}")
            return {"error": f"Unexpected error: {e}"}
        
    def create_post(self, content):
        """Creates a new Mastodon post."""
        if not content or not isinstance(content, str) or not content.strip():
            logger.error("Invalid content for post.")
            return {"error": "Invalid content. Content must be a non-empty string."}
        try:
            self._throttle_request()
            post = self.mastodon.status_post(content)
            logger.info(f"Post created:{post['id']}")
            return {"id": post["id"], "content": post["content"], "created_at": post["created_at"]}
        except MastodonRatelimitError:
            logger.error("API rate limit exceeded while creating post.")
            return {"error": "API rate limit exceeded. Please try again later."}
        except MastodonAPIError as e:
            logger.error(f"Mastodon API error while creating post: {e}")
            return {"error": f"Mastodon API error: {e}"}
        except Exception as e:
            logger.error(f"Error creating post: {e}")
            return {"error": f"Unexpected error: {e}"}

    def retrieve_post(self, post_id):
        """Retrieves a specific Mastodon post by ID."""
        if not post_id or not isinstance(post_id, int):
            logger.error("Invalid post_id for retrieving post.")
            return {"error": "Invalid post_id. Must be a valid integer."}
        try:
            self._throttle_request()
            post = self.mastodon.status(post_id)
            logger.info(f"Post retrieved: {post_id}")
            return post
        except MastodonRatelimitError:
            logger.error("API rate limit exceeded while retrieving post.")
            return {"error": "API rate limit exceeded. Please try again later."}
        except MastodonAPIError as e:
            logger.error(f"Mastodon API error while retrieving post: {e}")
            return {"error": f"Mastodon API error: {e}"}
        except Exception as e:
            logger.error(f"Error retrieving post {post_id}: {e}")
            return {"error": f"Unexpected error: {e}"}
        
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=60),
        retry=retry_if_exception_type(MastodonRatelimitError),
        before_sleep=lambda retry_state: logger.info(
            f"Rate limit hit, retrying in {retry_state.next_action.sleep} seconds..."
        )
    )
    def retrieve_all_posts(self, limit=10, max_id=None, since_id=None):
        """
        Retrieves posts using Mastodon's built-in cursor-based pagination with rate limit handling.
        :param limit: Number of posts to fetch (max 40 per Mastodon API).
        :param max_id: Return results older than or equal to this ID.
        :param since_id: Return results newer than this ID.
        :return: (posts, next_max_id, prev_since_id)
        """
        if not isinstance(limit, int) or limit <= 0 or limit > 40:
            logger.error(f"Invalid limit {limit} for retrieving posts. Must be 1-40.")
            return {"error": "Invalid limit. Limit must be a positive integer up to 40."}, None, None
        
        try:
            self._throttle_request()
            params = {"limit": min(limit, 40)}  # Ensure limit doesn't exceed API max
            if max_id is not None:
                params["max_id"] = max_id
            if since_id is not None:
                params["since_id"] = since_id

            posts = self.mastodon.timeline_home(**params)
            logger.info(f"Fetched {len(posts)} posts with limit={limit}, max_id={max_id}, since_id={since_id}")

            # Prepare pagination cursors for client
            next_max_id = posts[-1]['id'] if posts else None
            prev_since_id = posts[0]['id'] if posts else None

            return posts, next_max_id, prev_since_id
        except MastodonRatelimitError as e:
            logger.error(f"API rate limit exceeded while retrieving all posts: {e}")
            raise  # Let tenacity handle retry
        except MastodonAPIError as e:
            logger.error(f"Mastodon API error while retrieving all posts: {e}")
            return {"error": f"Mastodon API error: {e}"}, None, None
        except Exception as e:
            logger.error(f"Failed to fetch posts: {e}")
            return {"error": f"Unexpected error: {e}"}, None, None

    def delete_post(self, post_id):
        """Deletes a specific Mastodon post by ID."""
        if not post_id or not isinstance(post_id, int):
            logger.error("Invalid post_id for deleting post.")
            return {"error": "Invalid post_id. Must be a valid integer."}
        try:
            self._throttle_request()
            self.mastodon.status_delete(post_id)
            logger.info(f"Post {post_id} deleted successfully.")
            return True
        except MastodonRatelimitError:
            logger.error("API rate limit exceeded while deleting post.")
            return {"error": "API rate limit exceeded. Please try again later."}
        except MastodonAPIError as e:
            logger.error(f"Mastodon API error while deleting post: {e}")
            return {"error": f"Mastodon API error: {e}"}
        except Exception as e:
            logger.error(f"Error deleting post {post_id}: {e}")
            return {"error": f"Unexpected error: {e}"}