import os
from flask import Flask, jsonify
from flask_cors import CORS
from app.webhooks.webhook import webhook
from app.db_connections.mongo_connect import mongo
from app.config import FlaskAppEnvConfigs
from pprint import pprint

app = Flask(__name__)
pydantic_env_configs = FlaskAppEnvConfigs()
pprint(pydantic_env_configs.model_dump())

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
  # pprint("[PYDANTIC SETTINGS]: ", pydantic_env_configs.model_dump())
  return jsonify({
    "status": "All up and running!"
  }), 200