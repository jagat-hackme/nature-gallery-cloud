from pymongo import MongoClient

client = MongoClient("mongodb+srv://neupanejagat545_db_user:neupanejagat545@jagat.mghqoyp.mongodb.net/?retryWrites=true&w=majority&appName=Jagat")

db = client["nature_gallery"]
collection = db["photos"]

collection.insert_one({
    "src": "test.jpg",
    "title": "Test Photo",
    "desc": "Testing MongoDB Atlas connection",
    "cat": "Forest",
    "liked": False
})

print("SUCCESS: Data inserted into MongoDB Atlas")