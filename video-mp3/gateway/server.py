from gridfs import GridFS
import pika
import json
from flask import Flask, request
from flask_pymongo import PyMongo
from auth import validate
from auth_svc import access
from storage import util

server = Flask(__name__)
# server.config["MONGO_URI"] = "mongodb://localhost:27017/videos"

mongo = PyMongo(server, uri="mongodb://0.0.0.0:27017/videos")
fs = GridFS(mongo.db)

filename = "test.txt"
content = b"This is a test file content."

# Upload the file to GridFS
with fs.new_file(filename=filename) as f:
    f.write(content)

connection = pika.BlockingConnection(pika.ConnectionParameters(
    "rabbitmq"
))

channel = connection.channel()


@server.route("/login", methods=["POST"])
def login():
    token, err = access.login(request)
    if not err:
        return token
    else:
        return err


@server.route("/upload", methods=["POST"])
def upload():
    access, err = validate.token(request)
    if err:
        return err
    access = json.loads(access)
    if access["admin"]:
        if len(request.files) > 1 or len(request.files) < 1:
            return "only 1 file required", 400

        for _, f in request.files.items():
            err = util.upload(f, fs, channel, access)
            if err:
                print(err)
                return err
        return "success", 200
    else:
        return "not authorized", 401


@server.route("/download", methods=["GET"])
def download():
    pass


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=8080)
