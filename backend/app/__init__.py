import os
from flask import Flask, jsonify
from flask_cors import CORS
from app.webhooks.webhook import webhook
from app.db_connections.mongo_connect import mongo
from app.config import FlaskAppEnvConfigs
from pprint import pprint
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def create_app():
  
  """App factory pattern: creates and configures Flask app"""
  app = Flask(__name__)
    
  pydantic_env_configs = FlaskAppEnvConfigs()
  # logger.info("[CONFIGS LOADED]: %s", pydantic_env_configs.model_dump())
  pprint(pydantic_env_configs.model_dump())

  allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")
  CORS(
    app,
    resources={
      r"/*": 
        {
          "origins": allowed_origins
        }
      }
  )
  
  try:
    mongo.database_connection()
    logger.info("[MONGO]: Connection initialized successfully")
  except Exception as e:
    logger.error(f"[MONGO ERROR]: Failed to connect at app startup: {e}")
    
  app.register_blueprint(webhook)
  
  @app.route("/", methods=["GET"])
  def health():
    return jsonify({"status": "All up and running!"}), 200

  # # Close MongoDB connection closes cleanly on app teardown
  # @app.teardown_appcontext
  # def shutdown_db(exception=None):
  #   mongo.close()
  #   logger.info("[MONGO]: Connection closed on app teardown")
    
  return app 
