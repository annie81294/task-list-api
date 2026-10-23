from flask import Blueprint, abort, make_response, request, Response
from app.models.task import Task
from ..db import db
from datetime import datetime
from ..slack import send_slack_notification

bp = Blueprint("bp", __name__, url_prefix="/tasks")

@bp.post("")
def create_task():
    request_body = request.get_json()
    
    try:
        new_task = Task.from_dict(request_body)
    except KeyError:
        return {"details": "Invalid data"}, 400
    
    db.session.add(new_task)
    db.session.commit()

    return new_task.to_dict(), 201

@bp.get("")
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

def validate_task(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        response = {"message": f"task {task_id} invalid"}
        abort(make_response(response , 400))

    query = db.select(Task).where(Task.id == task_id)
    task = db.session.scalar(query)

    if not task:
        response = {"message": f"task {task_id} not found"}
        abort(make_response(response, 404))

    return task

@bp.get("/<task_id>")
def get_one_task(task_id):
    task = validate_task(task_id)

    return task.to_dict()

@bp.put("/<task_id>")
def update_task(task_id):
    task = validate_task(task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return Response(status=204, mimetype="application/json")

@bp.delete("/<task_id>/")
def delete_task(task_id):
    task = validate_task(task_id)
    db.session.delete(task)
    db.session.commit()

    return Response(status=204, mimetype="application/json")

@bp.patch("/<task_id>/mark_complete")
def mark_complete(task_id):
    task = validate_task(task_id)
    print("Task title:", task.title)
    print("Completed at before PATCH:", task.completed_at)

    task.completed_at = datetime.now()
    db.session.commit()
    send_slack_notification(task.title)

    return task.to_dict(), 200

@bp.patch("/<task_id>/mark_incomplete")
def mark_incomplete(task_id):
    task = validate_task(task_id)

    task.completed_at = None
    db.session.commit()

    return Response(status=204, mimetype="application/json")
