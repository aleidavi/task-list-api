from flask import Blueprint, abort, jsonify, make_response, request, Response
from app.db import db
from app.models.task import Task


tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

@tasks_bp.post("")
def create_task():
    
    try:
        request_body = request.get_json()
        title = request_body["title"]
        description = request_body["description"]
        new_task = Task(title=title, description=description)

        db.session.add(new_task)
        db.session.commit()

        return {"task": new_task.to_dict()}, 201
    
    except KeyError as error:
        response = {"details": f"Invalid data"}
        abort(make_response(response, 400))


@tasks_bp.get("")
def get_tasks_sort_title():
    
    title_sort = request.args.get("sort")

    if title_sort == 'asc':
        tasks = Task.query.order_by(Task.title.asc()).all()
    
    elif title_sort == 'desc':
        tasks = Task.query.order_by(Task.title.desc()).all()


    tasks_response = [task.to_dict() for task in tasks]

    return jsonify(tasks_response)


@tasks_bp.get("/<task_id>")
def get_one_task(task_id):
    task = validate_task(task_id)
    response = {"task": task.to_dict()}
    return response


@tasks_bp.put("/<task_id>")
def update_task(task_id):
    task = validate_task(task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]
    
    db.session.commit()

    return {"task": task.to_dict()} # Response(status=204, mimetype="application/json")

@tasks_bp.delete("/<task_id>")
def delete_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    response = {"details": f'Task {task_id} "{task.title}" successfully deleted'}

    # CHECK IF THIS IS CORRECT
    return jsonify(response) # Response(status=200, mimetype="application/json")

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


    
