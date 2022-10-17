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

    def __init__(self, name, email, address, image):
        self.name = name
        self.email = email
        self.address = address
        self.image = image


db.create_all()
db.session.commit()

app.logger.info('App running successfully!')


# -- Users --
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
    # app.logger.info(user.id)

    new_user = User.query.get(user.id)                      # get newly inserted user
    del new_user.__dict__['_sa_instance_state']
    return jsonify(new_user.__dict__)


# if __name__ == '__main__':
#     app.run(debug=True)
