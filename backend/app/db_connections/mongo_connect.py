import os
import logging
from dotenv import load_dotenv
from pymongo import MongoClient, errors, ASCENDING, DESCENDING

load_dotenv()

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class MongoDB:
    """
    MongoDB connection wrapper with connection pooling and health checks
    """

    def __init__(self):
        self.client = None
        self.db = None
        self.events_collection = None

    def database_connection(self):
        """
        Initialize MongoDB connection
        """
        logger.info("Initializing MongoDB connection...")

        mongo_url = os.getenv("DATABASE_URL")
        db_name = os.getenv("DATABASE_NAME", "webhook-data-receiver-app")

        if not mongo_url:
            raise ValueError("DATABASE_URL is not found in .env")

        try:
            self.client = MongoClient(
                mongo_url,
                serverSelectionTimeoutMS=5000,
                maxPoolSize=50,
                minPoolSize=5,
                retryWrites=True
            )

            # Force connection test
            self.client.admin.command("ping")

            self.db = self.client[db_name]
            # self.events_collection = self.db["webhook-events-data"]
            
            
            # Create collection with schema validation if it doesn't exist
            validator = {
                "$jsonSchema": {
                "bsonType": "object",
                "required": ["request_id", "author", "action", "to_branch", "timestamp"],
                "properties": {
                    "request_id": {"bsonType": "string"},
                    "author": {"bsonType": "string"},
                    "action": {"enum": ["PUSH", "PULL_REQUEST", "MERGE"]},
                    "from_branch": {"bsonType": ["string", "null"]},
                    "to_branch": {"bsonType": "string"},
                    "timestamp": {"bsonType": "string"}
                    }
                }
            }

            if "webhook-events-data" not in self.db.list_collection_names():
                self.events_collection =  self.db.create_collection(
                     "webhook-events-data", 
                     validator=validator
                )
                logger.info("Collection created with schema validation")
            else:
                self.db.command({
                    "collMod": "webhook-events-data",
                    "validator": validator,
                    "validationLevel": "strict"
                })
                # self.events_collection reference is set set before creating the validator. after create_collection() or collMod, self.events_collection is still valid but could set it after collMod to be safe.
                self.events_collection = self.db["webhook-events-data"]
                logger.info("Collection schema validation updated")
            
            logger.info(f"MongoDB connected successfully: {db_name}")

            # # Log collections
            # collections = self.db.list_collection_names()
            # logger.info(f"Collections: {collections if collections else 'No collections yet'}")
            
            # # Test insert
            # test_collection = self.db['test_connection']
            # result = test_collection.insert_one({"test": "data", "timestamp": "2024-01-01"})
            # logger.info(f"✅ Test insert successful! ID: {result.inserted_id}")
        
            # # Clean up test
            # test_collection.delete_one({"_id": result.inserted_id})
            # logger.info(f"🧹 Test data cleaned up")
        
            # # client.close()
            # print(f"✅ All connection tests passed!")
            # # return True

            # Create indexes
            self._create_indexes()

            return self.db

        except errors.ServerSelectionTimeoutError:
            logger.error("❌ Could not connect to MongoDB server. Check URL or network.")
            raise

        except Exception as e:
            logger.error(f"❌ MongoDB connection failed: {e}")
            raise
    
    def _create_indexes(self):
        """
        Create indexes optimized for webhook event queries
        """
        try:
            self.events_collection.create_index(
                [("timestamp", DESCENDING)]
            )
            self.events_collection.create_index(
                [("action", ASCENDING)]
            )
            logger.info("✅ MongoDB indexes created successfully")

        except Exception as e:
            logger.warning(f"Index creation failed or skipped: {e}")
    
    def insert_event(self, event_doc):
        """Insert an event document into the collection."""
        if not self.events_collection:
            raise RuntimeError("Events collection not initialized")
        self.events_collection.insert_one(event_doc)

    def get_db(self):
        """
        Return database instance
        """
        if not self.db:
            logger.error("Database instance is not initialized.")
            raise RuntimeError("Database not initialized. Call connect() first.")
        logger.info("Returning initialized database instance.")
        return self.db

    def close(self):
        """
        Close MongoDB connection
        """
        if self.client:
            self.client.close()
            logger.info("MongoDB connection closed")


# Global reusable instance
mongo = MongoDB()    