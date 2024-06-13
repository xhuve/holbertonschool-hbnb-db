
from flask import Blueprint, jsonify, request
from persistence.data_manager import DataManager
from models.review import Review

review_bp = Blueprint("review_bp", __name__)
dm = DataManager()

@review_bp.route("/reviews/<int:review_id>", methods=['GET'])
def get_review(review_id):
    return dm.get(review_id, "Review")

@review_bp.route("/reviews/<int:review_id>", methods=['PUT'])
def put_review(review_id):
    jData = request.get_json()
    req_review = dm.get(review_id, "Review")
    for field in ["feedback", "rating", "comment"]:
        if not isinstance(jData[field], str):
            return jsonify("Bad Request"), 400

    review = Review(
        feedback = jData['feedback'],
        rating = jData['rating'],
        comment = jData['comment'],
        place_id = jData['place_id'],
        user_id = jData['user_id']
    )

    review.id = req_review["id"]
    review.created_at = req_review["created_at"]

    try:
        dm.update(review)
        return jsonify("Updated")
    except Exception:
        return "Bad Request", 400

@review_bp.route('/reviews/<int:review_id>', methods=['DELETE'])
def delete_user(review_id):
    dm.delete(review_id, "Review")
    return jsonify("Deleted"), 204
