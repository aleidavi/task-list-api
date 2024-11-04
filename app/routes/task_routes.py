from flask import Blueprint, abort, make_response, request, Response
from app.db import db
from app.models.task import Task


tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

@tasks_bp.post("")
def create_task():
    request_body = request.get_json()
    title = request_body["title"]
    description = request_body["description"]
    completed_at = request_body["completed_at"]

    new_task = Task(title=title, description=description, completed_at=completed_at)

    # validating a new task with ALL required info
    if not new_task:
        response = {"details": f"Invalid data"}
        abort(make_response(response, 400))

    db.session.add(new_task)
    db.session.commit()
    response = new_task.to_dict()

    return response, 201

@tasks_bp.get("")
def get_all_task():
    query = db.select(Task)
    title_param = request.args.get("title")

    if title_param:
        query = query.where(Task.title == title_param)

    description_param = request.args.get("description")
    if description_param:
        query = query.where(Task.description.ilike(f"%{description_param}%"))
    
    completed_at_param = request.args.get("completed_at")
    if completed_at_param:
        query = query.where(Task.completed_at.ilike(f"%{completed_at_param}%"))
    
    query = query.order_by(Task.id)

    tasks = db.session.scalars(query)

    tasks_response = [task.to_dict() for task in tasks]

    return tasks_response


@tasks_bp.get("/<task_id>")
def get_one_task(task_id):
    task = validate_task(task_id)
    response = task.to_dict()
    return response


@tasks_bp.put("/<task_id>")
def update_task(task_id):
    task = validate_task(task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]
    task.completed_at = request_body["completed_at"]
    db.session.commit()

    return Response(status=204, mimetype="application/json")

@tasks_bp.delete("/<task_id>")
def delete_task(task_id):
    task = validate_task(task_id)
    db.session.delete(task)
    db.session.commit()

    response = {"details": f"Task {task_id} \{task}\ successfully deleted"}

    # CHECK IF THIS IS CORRECT
    return Response(response, status=204, mimetype="application/json")

def validate_task(task_id):
    try:
        task_id = int(task_id)
    
    except:
        response = {"details": f"Invalid data"}
        abort(make_response(response, 400))

    query = db.select(Task).where(Task.id == task_id)
    task = db.session.scalar(query)

    if not task:
        response = {"details": f"Task {task_id} not found"}
        abort(make_response(response, 404))

    return task
