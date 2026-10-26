import os
from datetime import datetime, timezone
from bson import ObjectId
from pymongo import MongoClient, ASCENDING, DESCENDING


def utcnow():
    return datetime.now(timezone.utc)


def serialize(value):
    if isinstance(value, ObjectId):
        return str(value)
    if isinstance(value, datetime):
        return value.isoformat()
    return value


class MongoDB:
    def __init__(self):
        self.uri = os.getenv("MONGO_URI", "").strip()
        self.name = os.getenv("MONGO_DB_NAME", "farmnova").strip()
        if not self.uri:
            raise RuntimeError("MONGO_URI is missing. Add your MongoDB Atlas URI to .env")
        self.client = MongoClient(self.uri, serverSelectionTimeoutMS=10000, connectTimeoutMS=10000)
        self.db = self.client[self.name]
        self.conversations = self.db["conversations"]
        self.messages = self.db["messages"]
        self.users = self.db["users"]
        self.disease_history = self.db["disease_history"]
        self.crop_recommendations = self.db["crop_recommendations"]
        self.weather_history = self.db["weather_history"]
        self.reports = self.db["reports"]
        self.messages.create_index([("conversation_id", ASCENDING), ("created_at", ASCENDING)])
        self.conversations.create_index([("updated_at", DESCENDING)])

    def ping(self):
        self.client.admin.command("ping")
        return True

    def conversation_dict(self, doc):
        return {"id": str(doc["_id"]), "title": doc.get("title", "New FarmNova Chat"),
                "created_at": serialize(doc.get("created_at")), "updated_at": serialize(doc.get("updated_at"))}

    def message_dict(self, doc):
        return {"id": str(doc["_id"]), "role": doc.get("role"), "content": doc.get("content", ""),
                "file_name": doc.get("file_name"), "file_type": doc.get("file_type"),
                "created_at": serialize(doc.get("created_at"))}

    def oid(self, value):
        try:
            return ObjectId(value)
        except Exception:
            return None

    def create_conversation(self, title="New FarmNova Chat"):
        now = utcnow()
        r = self.conversations.insert_one({"title": title, "created_at": now, "updated_at": now})
        return self.conversations.find_one({"_id": r.inserted_id})

    def get_conversation(self, cid):
        oid = self.oid(cid)
        return self.conversations.find_one({"_id": oid}) if oid else None

    def list_conversations(self):
        return list(self.conversations.find().sort("updated_at", DESCENDING))

    def delete_conversation(self, cid):
        oid = self.oid(cid)
        if not oid:
            return False
        self.messages.delete_many({"conversation_id": oid})
        result = self.conversations.delete_one({"_id": oid})
        return result.deleted_count == 1

    def get_messages(self, cid):
        oid = self.oid(cid)
        if not oid:
            return []
        return list(self.messages.find({"conversation_id": oid}).sort("created_at", ASCENDING))

    def add_message(self, cid, role, content, file_name=None, file_type=None, file_path=None):
        oid = self.oid(cid)
        if not oid:
            raise ValueError("Invalid conversation id")
        now = utcnow()
        doc = {"conversation_id": oid, "role": role, "content": content, "file_name": file_name,
               "file_type": file_type, "file_path": file_path, "created_at": now}
        r = self.messages.insert_one(doc)
        self.conversations.update_one({"_id": oid}, {"$set": {"updated_at": now}})
        doc["_id"] = r.inserted_id
        return doc

    def update_title(self, cid, title):
        oid = self.oid(cid)
        if oid:
            self.conversations.update_one({"_id": oid}, {"$set": {"title": title, "updated_at": utcnow()}})


db = MongoDB()
Conversation = None
Message = None
