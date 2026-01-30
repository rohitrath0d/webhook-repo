from flask import Blueprint, jsonify, request
from app.db_connections.mongo_connect import mongo

webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')

@webhook.route('/receiver', methods=["POST"])
def github_actions_webhook_receiver():
    
    event_type = request.headers.get("X-Github-Event")
    payload = request.json
    
    if not event_type or not payload:
        return jsonify({
            "error" : "Invalid payload"
        }), 400
        
    # ignore ping event
    if event_type == "ping":
        return jsonify({
            "message" : "pong"
        }), 200
    
    event_doc = None
    
    # push events
    if event_type == "push":
        event_doc = {
            "request_id": payload["head_commit"]["id"],
            "author": payload["pusher"]["name"],
            "action": "PUSH",
            "from_branch": None,
            "to_branch": payload["ref"].split("/")[-1],
            "timestamp": payload["head_commit"]["timestamp"]
        }
        
    # pull requests
    elif event_type == "pull_request":
        pr = payload["pull_request"]

        # PR opened
        if payload["action"] == "opened":
            event_doc = {
                "request_id": str(pr["id"]),
                "author": pr["user"]["login"],
                "action": "PULL_REQUEST",
                "from_branch": pr["head"]["ref"],
                "to_branch": pr["base"]["ref"],
                "timestamp": pr["created_at"]
            }
            
         # MERGE
        elif payload["action"] == "closed" and pr["merged"]:
            event_doc = {
                "request_id": str(pr["id"]),
                "author": pr["merged_by"]["login"],
                "action": "MERGE",
                "from_branch": pr["head"]["ref"],
                "to_branch": pr["base"]["ref"],
                "timestamp": pr["merged_at"]
            }
    
    # storing the events 
    if event_doc:
        mongo.insert_event(event_doc)
        return jsonify({"status": "stored"}), 200    
    
    return jsonify({
        "status" : "ignored"
    }), 200