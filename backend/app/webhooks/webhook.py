from flask import Blueprint, jsonify, request
from app.db_connections.mongo_connect import mongo
# from app.models.models import GitHubEvent
import logging
from app.handlers.github_handler import github_event_handler
from threading import Thread


logger = logging.getLogger(__name__)

webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')

def background_event_processing(event_type, payload):
    """
    This fun runs OUTSIDE the Flask request thread.
    It just does work in the background
    """
    try:
        event = github_event_handler(event_type, payload)

        if not event:
            logger.info("Event ignored")
            return

        mongo.insert_event(event.dict())
        logger.info(f"Stored event: {event.action} by {event.author}")

    except Exception as e:
        logger.error(f"Background processing failed: {e}")

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
   
    # Spawning background thread
    Thread(
        target=background_event_processing,
        args=(event_type, payload),
        daemon=True
    ).start()
    
    # sending immediate response to github
    return jsonify({
        "status": "accepted"
    }), 200
   
@webhook.route('/events', methods=['GET'])
def get_events():
    try:
        events = list(mongo.events_collection.find()
                      .sort("timestamp", -1)
                      .limit(50)
                )
        for event in events:
            event["_id"] = str(event["_id"])  # Convert ObjectId to string
        # return jsonify({
        #     "events": events
        #     }), 200
        return jsonify(events), 200
    except Exception as e:
        logger.error(f"Error fetching events: {e}")
        return jsonify({"error": "Failed to fetch events"}), 500
