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
    limit = request.args.get("limit", default=10, type=int)
    max_id = request.args.get("max_id", default=None, type=int)

    posts = mastodon_service.retrieve_all_posts(limit=limit, max_id=max_id)

    if posts:
        return jsonify([
            {
                "post_id": post["id"],
                "content": post["content"],
                "created_at": post["created_at"]
            }
            for post in posts
        ]), 200

    return jsonify({"error": "No posts found"}), 404


@routes.route("/delete/<int:post_id>", methods=["DELETE"])
def delete_post(post_id):
    success = mastodon_service.delete_post(post_id)

    if success:
        return jsonify({"message": f"Post {post_id} deleted successfully"}), 200
    return jsonify({"error": "Failed to delete post"}), 500
