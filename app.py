from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from pymongo import MongoClient
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
import os
import uuid

load_dotenv()

app = Flask(__name__)
CORS(app)

# MongoDB Atlas connection
mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)
db = client["nature_gallery"]
collection = db["photos"]

# Azure Blob Storage connection
azure_connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
container_name = os.getenv("AZURE_CONTAINER_NAME", "images")

blob_service_client = BlobServiceClient.from_connection_string(azure_connection_string)

@app.route("/")
def index():
    return send_from_directory(os.path.dirname(__file__) or ".", "index.html")

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    title = request.form["title"]
    desc = request.form["desc"]
    cat = request.form["cat"]

    # unique filename
    filename = f"{uuid.uuid4()}-{file.filename}"

    # upload image to Azure Blob Storage
    blob_client = blob_service_client.get_blob_client(
        container=container_name,
        blob=filename
    )

    blob_client.upload_blob(file, overwrite=True)

    # Blob URL
    blob_url = f"https://jagatnaturegallery.blob.core.windows.net/{container_name}/{filename}"

    # save metadata in MongoDB Atlas
    photo = {
        "src": blob_url,
        "title": title,
        "desc": desc,
        "cat": cat,
        "liked": False
    }

    collection.insert_one(photo)

    return jsonify({"message": "Uploaded successfully to Azure Blob Storage"})

@app.route("/photos", methods=["GET"])
def get_photos():
    photos = []

    for p in collection.find():
        photos.append({
            "src": p["src"],
            "title": p["title"],
            "desc": p["desc"],
            "cat": p["cat"],
            "liked": p.get("liked", False)
        })

    return jsonify(photos)

if __name__ == "__main__":
    app.run(debug=True)