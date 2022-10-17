from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
# import logging
# logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    image = db.Column(db.String(120), nullable=False)
    audio_files = db.relationship('Audio', backref='user', lazy=True)

    def __init__(self, name, email, address, image):
        self.name = name
        self.email = email
        self.address = address
        self.image = image


class Audio(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    session_id = db.Column(db.Integer, nullable=False, unique=True)
    ticks = db.Column(db.String(1000), nullable=False)
    selected_tick = db.Column(db.Integer, nullable=False)
    step_count = db.Column(db.Integer, nullable=False)

    def __init__(self, user_id, session_id, ticks, selected_tick, step_count):
        self.user_id = user_id
        self.session_id = session_id
        self.ticks = ticks
        self.selected_tick = selected_tick
        self.step_count = step_count


db.create_all()
db.session.commit()

app.logger.info('App running successfully!')


# -- User Routes --
@app.route("/users", methods=['GET'])
def get_users():
    """ Get all users """
    users = []
    for user in db.session.query(User).all():
        del user.__dict__['_sa_instance_state']
        users.append(user.__dict__)
    return jsonify(users)


@app.route("/user/<id>", methods=['GET'])
def get_user(id):
    """ Get a user by id """
    user = User.query.get(id)
    del user.__dict__['_sa_instance_state']
    return jsonify(user.__dict__)


@app.route("/users", methods=['POST'])
def create_user():
    """ Create a user """
    body = request.get_json()

    # TODO: validate user

    user = User(
        name=body['name'],
        email=body['email'],
        address=body['address'],
        image=body['image']
    )

    db.session.add(user)
    db.session.commit()
    db.session.flush()

    new_user = User.query.get(user.id)                      # get newly inserted user
    del new_user.__dict__['_sa_instance_state']
    return jsonify(new_user.__dict__)


@app.route("/user/<id>", methods=['PUT'])
def update_user(id):
    """ Update a user by id """
    body = request.get_json()
    user_dict = dict(
        name=body['name'],
        email=body['email'],
        address=body['address'],
        image=body['image'],
    )
    db.session.query(User).filter_by(id=id).update(user_dict)
    db.session.commit()
    return "user updated"


@app.route("/user/<id>", methods=['DELETE'])
def delete_user(id):
    """ Delete a user by id """
    db.session.query(User).filter_by(id=id).delete()
    db.session.commit()
    return "user deleted"


@app.route("/search_user", methods=['GET'])
def search_user():
    """ Search user by id, name, email, or address """
    id = request.args.get('id')
    name = request.args.get('name')
    email = request.args.get('email')
    address = request.args.get('address')

    results = []

    if id:
        query_res = db.session.query(User).filter_by(id=id).first()
        del query_res.__dict__['_sa_instance_state']
        results.append(query_res.__dict__)
    elif name:
        query_res = db.session.query(User).filter(User.name.like("%" + name + "%")).all()
        for user in query_res:
            del user.__dict__['_sa_instance_state']
            results.append(user.__dict__)
    elif email:
        query_res = db.session.query(User).filter(User.email.like("%" + email + "%")).all()
        for user in query_res:
            del user.__dict__['_sa_instance_state']
            results.append(user.__dict__)
    elif address:
        query_res = db.session.query(User).filter(User.address.like("%" + address + "%")).all()
        for user in query_res:
            del user.__dict__['_sa_instance_state']
            results.append(user.__dict__)

    return jsonify(results)


# -- TODO: Audio Routes --
@app.route("/user/<id>/audio", methods=['GET'])
def get_audio(id):
    """ Get all a user's audio files """
    user = User.query.get(id)
    audio_files = []
    pass


@app.route("/user/<id>/audio", methods=['POST'])
def post_audio():
    """ Post a user's audio file """
    pass


@app.route("/user/<id>/audio", methods=['PUT'])
def post_audio():
    """ Update a user's audio file """
    pass


@app.route("/search_audio", methods=['GET'])
def search_sid():
    """ Search for audio file with session id """
    pass


# if __name__ == '__main__':
#     app.run(debug=True)
