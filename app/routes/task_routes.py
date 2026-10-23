from flask import Blueprint, abort, make_response, request, Response
from app.models.task import Task
from ..db import db
from datetime import datetime
from ..slack import send_slack_notification
from .route_utilities import validate_model, create_model

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

@tasks_bp.post("")
def create_task():
    request_body = request.get_json()
    new_task = create_model(Task, request_body)
    
    return new_task

@tasks_bp.get("")
def get_all_tasks():
    sort_order = request.args.get("sort", "asc")

    if sort_order == "desc":
        query = db.select(Task).order_by(Task.title.desc())
    else:
        query = db.select(Task).order_by(Task.title.asc())
    
    tasks = db.session.scalars(query)

    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_dict())

    return tasks_response

@tasks_bp.get("/<task_id>")
def get_one_task(task_id):
    task = validate_model(Task, task_id)

    return task.to_dict()

@tasks_bp.put("/<task_id>")
def update_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return Response(status=204, mimetype="application/json")

@tasks_bp.delete("/<task_id>")
def delete_task(task_id):
    task = validate_model(Task, task_id)
    db.session.delete(task)
    db.session.commit()

    return Response(status=204, mimetype="application/json")

@tasks_bp.patch("/<task_id>/mark_complete")
def mark_complete(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = datetime.now()
    db.session.commit()
    send_slack_notification(task.title)

    return task.to_dict(), 200

@tasks_bp.patch("/<task_id>/mark_incomplete")
def mark_incomplete(task_id):
    task = validate_model(Task, task_id)

    task.completed_at = None
    db.session.commit()

    return Response(status=204, mimetype="application/json")
