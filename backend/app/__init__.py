from flask import Flask

from app.webhooks.webhook import webhook
from app.db_connections.mongo_connect import mongo

app = Flask(__name__)

mongo.database_connection();

def create_app():
  app.register_blueprint(webhook)
  return app 

@app.route("/", methods=["GET"])
def health():
    return {"status": "Webhook server running"}, 200