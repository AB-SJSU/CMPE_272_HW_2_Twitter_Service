from flask import Blueprint, request, jsonify
from app.mastodon_service import MastodonService

mastodon_service = MastodonService()
routes = Blueprint("routes", __name__)

@routes.route("/create", methods=["POST"])
def create_post():
    data = request.json
    content = data.get("content", "")

    if not content:
        return jsonify({"error": "Content is required"}), 400

    post_id = mastodon_service.create_post(content)
    if post_id:
        return jsonify({"post_id": post_id}), 201
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


@routes.route("/delete/<int:post_id>", methods=["DELETE"])
def delete_post(post_id):
    success = mastodon_service.delete_post(post_id)

    if success:
        return jsonify({"message": f"Post {post_id} deleted successfully"}), 200
    return jsonify({"error": "Failed to delete post"}), 500