import sqlite3
import datetime
import jwt
import os
from flask import Flask, render_template, request

DATABASE = 'data.db'


server = Flask(__name__)


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# c = sqlite3.connect('data.db')
# with open('schema.sql') as f:
#     c.executescript(f.read())
#
# c.commit()
# c.close()


@server.route('/')
def index():
    conn = get_db()
    data = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    return render_template('index.html', users=data)


@server.route("/login", methods=["POST"])
def login():
    auth = request.authorization
    if not auth:
        return "missing credentials", 401

    conn = get_db()
    res = conn.execute("SELECT email, password FROM users WHERE email = %s",
                       (auth.username))

    if res > 0:
        user_row = res.fetchone()
        email = user_row[0]
        password = user_row[1]
        if auth.username != email or auth.password != password:
            return "invalid credentials", 401
        else:
            return createJWT(auth.username, os.environ.get("JWT_SECRET"), True)
    else:
        return "invalid credentials", 401


@server.route("/validate", methods=["POST"])
def validate():
    encoded_jwt = request.headers["Authorization"]
    if not encoded_jwt:
        return "missing credentials", 401
    encoded_jwt = encoded_jwt.split(" ")[1]
    try:
        decoded = jwt.decode(encoded_jwt, os.environ.get(
            "JWT_SECRET"), algorithm=["HS256"])
    except:
        return "not authorized", 403
    return decoded, 200


def createJWT(username, secret, authz):
    return jwt.encode(
        {
            "username": username,
            "exp": datetime.datetime.now(tz=datetime.timezone.utc)
            + datetime.timedelta(days=1),
            "iat": datetime.datetime.utcnow(),
            "admin": authz
        },
        secret,
        algorithm="HS256"
    )


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=5000)
