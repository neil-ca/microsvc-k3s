import pika 
import json
import tempfile
import os
from bson.objectid import ObjectId


def start(message, fs_videos, fs_mp3s, channel):
    message = json.loads(message)
    tf = tempfile.NamedTemporaryFile()
    out = fs_videos.get(ObjectId["video_fid"])

    tf.write(out.read())

