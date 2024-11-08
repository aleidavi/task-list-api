from flask import Blueprint, abort, jsonify, make_response, request
from app.db import db
from app.models.goal import Goal
import requests


goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

@goals_bp.post("")
def create_goal():

    try:
        request_body = request.get_json()
        title = request_body["title"]
        
        new_goal = Goal(title=title)

        db.session.add(new_goal)
        db.session.commit()

        return {"goal": new_goal.to_dict()}, 201
    
    except KeyError as error:
        response = {"details": f"Invalid data"}
        abort(make_response(response, 400))

@goals_bp.get("/<goal_id>/tasks")
def get_tasks_by_goal(goal_id):
    goal = validate_goal(goal_id)
    response = [task.to_dict() for task in goal.tasks]
    return response


@goals_bp.get("")
def get_all_goals():

    query = db.select(Goal).order_by(Goal.id)
    goals = db.session.scalars(query)

    goals_response = [goal.to_dict() for goal in goals]

    return goals_response

@goals_bp.get("/<goal_id>")
def get_one_goal(goal_id):

    goal = validate_goal(goal_id)
    response = {"goal": goal.to_dict()}

    return response

@goals_bp.delete("/<goal_id>")
def delete_goal(goal_id):

    goal = validate_goal(goal_id)

    db.session.delete(goal)
    db.session.commit()

    response = {"details": f'Goal {goal_id} "{goal.title}" successfully deleted'}
    return jsonify(response)
    
@goals_bp.put("/<goal_id>")
def update_goal(goal_id):
    goal = validate_goal(goal_id)
    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()

    return {"goal": goal.to_dict()}


def validate_goal(goal_id):
    try:
        goal_id = int(goal_id)
    
    except:
        response = {"details": f"Invalid data"}
        abort(make_response(response, 400))

    query = db.select(Goal).where(Goal.id == goal_id)
    goal = db.session.scalar(query)

    if not goal:
        response = {"details": f"Goal {goal_id} not found"}
        abort(make_response(response, 404))

    return goal