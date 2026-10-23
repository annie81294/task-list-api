from flask import Blueprint, request, Response
from app.models.goal import Goal
from ..db import db
from .route_utilities import validate_model, create_model

goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

@goals_bp.post("")
def create_goal():
    request_body = request.get_json()

    new_goal = create_model(Goal, request_body)
    return new_goal

@goals_bp.get("")
def get_all_goals():
    query = db.select(Goal).order_by(Goal.id)
    goals = db.session.scalars(query)

    goals_response = []
    for goal in goals:
        goals_response.append(goal.to_dict())

    return goals_response

@goals_bp.get("/<goal_id>")
def get_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    return goal.to_dict()

@goals_bp.put("/<goal_id>")
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()

    return Response(status=204, mimetype="application/json")

@goals_bp.delete("/<goal_id>")
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    db.session.delete(goal)
    db.session.commit()

    return Response(status=204, mimetype="application/json")