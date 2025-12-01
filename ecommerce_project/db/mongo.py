from pymongo import MongoClient

MONGO_URL = "mongodb://localhost:27017/"
client = MongoClient(MONGO_URL)
db = client["ecommerce_db"]



user = {"name": "Himanshu", "age": 26}
db.users.insert_one(user)

def get_db():
	client = MongoClient("mongodb://localhost:27017/")
	return client["ecommerce"]
