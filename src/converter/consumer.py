import os
import pika
import sys
import time
from pymongo import MongoClient
import gridfs
from convert import mp3converter


def main():
    client = MongoClient("my-mongo", 27017)
    db_videos = client.videos
    db_mp3s = client.mp3s

    fs_videos = gridfs.GridFS(db_videos)
    fs_mp3s = gridfs.GridFS(db_mp3s)

    # rabbitmq conn
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="rabbitmq")
    )
    channel = connection.channel()

    def callback(ch, method, properties, body):
        err = mp3converter.start(body, fs_videos, fs_mp3s, ch)
        if err:
            ch.basic_nack(delivery_tah=method.delivery_tag)
        else:
            ch.basic_ack(delivery_tah=method.delivery_tag)
    channel.basic_consume(
        queue=os.environ.get("VIDEO_QUEUE"), on_message_callback=callback
    )

    print("Waiting for messages")
    channel.start_consuming()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrumped")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
