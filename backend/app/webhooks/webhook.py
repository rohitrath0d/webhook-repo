from flask import Blueprint, jsonify, request
from app.db_connections.mongo_connect import mongo
from app.models.models import GitHubEvent
import logging

logger = logging.getLogger(__name__)

webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')

@webhook.route('/receiver', methods=["POST"])
def github_actions_webhook_receiver():
    
    event_type = request.headers.get("X-Github-Event")
    payload = request.json
    
    if not event_type or not payload:
        return jsonify({
            "error" : "Invalid payload"
        }), 400
        
    # ignore ping events
    if event_type == "ping":
        return jsonify({
            "message" : "pong"
        }), 200
    
    event_doc = None
    
    
    try:
        # push events
        if event_type == "push" and payload.get("head_commit"):
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
        
        # Validate and insert event
        if event_doc:
            validated_event = GitHubEvent(**event_doc)
            mongo.insert_event(validated_event.dict())
            logger.info(f"Stored event: {validated_event.action} by {validated_event.author}")
            return jsonify({"status": "stored"}), 200
    
        return jsonify({
            "status" : "ignored"
        }), 200
        
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        return jsonify({"error": str(e)}), 500

@webhook.route('/events', methods=['GET'])
def get_events():
    try:
        events = list(mongo.events_collection.find().sort("timestamp", -1).limit(50))
        for event in events:
            event["_id"] = str(event["_id"])  # Convert ObjectId to string
        return jsonify(events), 200
    except Exception as e:
        logger.error(f"Error fetching events: {e}")
        return jsonify({"error": "Failed to fetch events"}), 500
