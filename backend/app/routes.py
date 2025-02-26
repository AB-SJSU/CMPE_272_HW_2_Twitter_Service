from flask import Blueprint, request, jsonify
from app.mastodon_service import MastodonService

mastodon_service = MastodonService()
routes = Blueprint("routes", __name__)

@routes.route("/user", methods=["GET"])
def get_user_profile():
    
    user = mastodon_service.user_profile_get()

    if user:
        return jsonify(user), 201
    return jsonify({"error": "Failed get user information"}), 500

@routes.route("/create", methods=["POST"])
def create_post():
    data = request.json
    content = data.get("content", "")

    if not content:
        return jsonify({"error": "Content is required"}), 400

    post = mastodon_service.create_post(content)
    if post:
        return jsonify(post), 201
    return jsonify({"error": "Failed to create post"}), 500

@routes.route("/retrieve/<int:post_id>", methods=["GET"])
def retrieve_post(post_id):
    post = mastodon_service.retrieve_post(post_id)

    if post:
        return jsonify({
            "post_id": post["id"],
            "content": post["content"],
            "created_at": post["created_at"]
        }), 200
    return jsonify({"error": "Post not found"}), 404

@routes.route("/retrieve_all", methods=["GET"])
def retrieve_all_posts():
    page = request.args.get("page", default=1, type=int)
    limit = request.args.get("limit", default=50, type=int)

     # Calculate offset
    offset = (page - 1) * limit

     # Fetch posts using offset-based pagination
    posts, total_posts = mastodon_service.retrieve_all_posts(offset=offset, limit=limit)

    if not posts:
        return jsonify({"error": "No posts found"}), 404
    
    # Calculate total pages
    total_pages = (total_posts + limit - 1) // limit  # Round up divisi

    if posts:
        return jsonify({
            "posts": [
                {
                    "id": post["id"],
                    "content": post["content"],
                    "created_at": post["created_at"]
                }
                for post in posts
            ],
            "current_page": page,
            "total_pages": total_pages,
            "has_next": offset + limit < total_posts ,
            "has_prev": page > 1
        }), 200

    return jsonify({"error": "No posts found"}), 404


@routes.route("/delete/<int:post_id>", methods=["DELETE"])
def delete_post(post_id):
    success = mastodon_service.delete_post(post_id)

    if success:
        return jsonify({"message": f"Post {post_id} deleted successfully"}), 200
    return jsonify({"error": "Failed to delete post"}), 500
