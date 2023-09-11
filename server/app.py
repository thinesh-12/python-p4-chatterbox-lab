from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

app.route("/messages", methods=["GET", "POST"])
def messages():
    if request.method == "GET":
        msgs = []
        for message in Message.query.all():
            message_dict = message.to_dict()
            msgs.append(message_dict)

        response = make_response(msgs, 200)

    elif request.method == "POST":
        request_dict = request.get_json()
        new_message = Message(
            body=request_dict.get("body"), username=request_dict.get("username")
        )
        db.session.add(new_message)
        db.session.commit()

        dict = new_message.to_dict()

        response = make_response(dict, 201)

    return response


@app.route("/messages/<int:id>", methods=["GET", "PATCH", "DELETE"])
def messages_by_id(id):
    msg = Message.query.filter(Message.id == id).first()

    if request.method == "GET":
        serial = msg.to_dict()
        response = make_response(serial, 200)

    elif request.method == "PATCH":
        request_dict = request.get_json()

        for attr in request_dict:
            setattr(msg, attr, request_dict.get(attr))

        db.session.add(msg)
        db.session.commit()
        serial = msg.to_dict()

        response = make_response(serial, 200)

    elif request.method == "DELETE":
        db.session.delete(msg)
        db.session.commit()
        res_body = {"delete_successful": True, "Message": "Message Deleted"}
        response = make_response(res_body, 200)

    return response


if __name__ == "__main__":
    app.run(port=5555)