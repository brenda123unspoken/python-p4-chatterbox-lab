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

# @app.route('/messages')
# def messages():
#     return ''

# @app.route('/messages/<int:id>')
# def messages_by_id(id):
#     return ''

# if __name__ == '__main__':
#     app.run(port=5555)

@app.route('/messages', methods=['GET'])
def get_messages():
    messages = Message.query.order_by(Message.created_at.asc()).all()
    return jsonify([message.to_dict() for message in messages]), 200

# POST /messages - Creates a new message
@app.route('/messages', methods=['POST'])
def create_message():
    data = request.get_json()
    body = data.get('body')
    username = data.get('username')

    if not body or not username:
        return jsonify({"error": "Missing body or username"}), 400

    new_message = Message(body=body, username=username)
    db.session.add(new_message)
    db.session.commit()

    return jsonify(new_message.to_dict()), 201

# PATCH /messages/<int:id> - Updates a message
@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    data = request.get_json()
    message = Message.query.get(id)

    if not message:
        return jsonify({"error": "Message not found"}), 404

    body = data.get('body')
    if body:
        message.body = body
        db.session.commit()

    return jsonify(message.to_dict()), 200

# DELETE /messages/<int:id> - Deletes a message
@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = Message.query.get(id)

    if not message:
        return jsonify({"error": "Message not found"}), 404

    db.session.delete(message)
    db.session.commit()

    return jsonify({"message": "Message deleted"}), 200

# To run the app
if __name__ == '__main__':
    app.run(debug=True)