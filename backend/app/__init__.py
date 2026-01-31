import os
from flask import Flask, jsonify
from flask_cors import CORS
from app.webhooks.webhook import webhook
from app.db_connections.mongo_connect import mongo

app = Flask(__name__)

allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")
CORS(
  app,
  resources={
    r"/*": 
      {
        "origins": allowed_origins
        }
      }, 
  )

mongo.database_connection();

def create_app():
  app.register_blueprint(webhook)
  return app 

@app.route("/", methods=["GET"])
def health():
    return jsonify({
      "status": "Webhook server running"
      }), 200