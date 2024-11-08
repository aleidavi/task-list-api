from flask import abort, make_response
from ..db import db
from app.models.task import Task
from app.models.goal import Goal

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        response = {"details": f"Invalid data"}
        abort(make_response(response, 400))
    
    query = db.select(cls).where(cls.id == model_id)
    model = db.session.scalar(query)

    if not model:
        abort(make_response({ "details": f"{cls.__name__} {model_id} not found"}, 404))
    
    return model



def create_model(cls, model_data):
    try:
        new_model = cls.from_dict(model_data)
    
    except KeyError as error:
        response = {"details": f"Invalid data"}
        abort(make_response(response, 400))
    
    db.session.add(new_model)
    db.session.commit()
    model_name = cls.__name__

    return {f"{model_name.lower()}": new_model.to_dict()}, 201


def get_models_with_filters(cls, filters=None):
    query = db.select(cls)

    if filters:
        for attribute, value in filters.items():
            if hasattr(cls, attribute):
                query = query.order_by(getattr(cls, attribute).ilike(f"%{value}%"))
    
    models = db.session.scalars(query.order_by(cls.id))
    models_response = [model.to_dict() for model in models]

    return models_response


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


