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



