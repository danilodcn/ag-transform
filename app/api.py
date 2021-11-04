import os
import json
from flask_classful import FlaskView, route

from flask import Flask, jsonify, request
from flask_login import login_user, login_required, LoginManager, current_user
from sqlalchemy.engine import create_engine
from flask_sqlalchemy import SQLAlchemy

import pandas as pd
from app.genetic_algorithm.ag import AG
from app.genetic_algorithm.gene import Gene
from app.ag import (
    variations,
    n_generations,
    n_population,
    to_test_constraints,
    tables
)

from dotenv import load_dotenv


load_dotenv()
Gene.variations = variations

POSTGRES_URI = os.getenv("POSTGRES_URI")
SECRET_KEY = os.getenv("SECRET_KEY")

engine = create_engine(POSTGRES_URI)
app = Flask(__name__)
app.secret_key = SECRET_KEY

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////docker/test.db'
app.config['SQLALCHEMY_DATABASE_URI'] = POSTGRES_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.name

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email
        }

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


@app.get("/")
def index():
    data = pd.read_sql('select * from "Population"', engine)

    # import ipdb; ipdb.set_trace()
    return jsonify({
        "status": 1,
        "data": json.loads(data.to_json())
    })


@app.route('/login', methods=['POST'])
def login():
    info = json.loads(request.data)
    username = info.get('username', 'guest')
    password = info.get('password', '')

    # import ipdb; ipdb.set_trace()
    user = User.query.filter_by(
        name=username,
        password=password
    ).first()
    # user = User.objects(name=username,
    #                     password=password).first()

    if user:
        login_user(user)
        return jsonify(user.to_json())
    else:
        return jsonify({"status": 401,
                        "reason": "Username or Password Error"})


@app.post("/create-account")
def create_account():
    info = json.loads(request.data)
    username = info.get('username', 'guest')
    password = info.get('password', '')
    email = info.get("email", "")

    # print(username, password, email)
    try:
        db.session.add(User(name=username, password=password, email=email))
        db.session.commit()
        return jsonify("created")

    except Exception as error:

        return jsonify({
            "status": 405,
            "reason": "Not created the account",
            "error": str(error)
        })


class APIView(FlaskView):

    ag = AG(
        n_generations,
        n_population,
        int(n_population / 1.5),  # número de indivíduos para a mutação
        to_test_constraints,
        tables
    )
    ag = {}
    engine = create_engine(POSTGRES_URI)

    @route("create", methods=["POST"])
    @login_required
    def post(self):
        # import ipdb; ipdb.set_trace()
        record = json.loads(request.data)
        return jsonify({
            "user": current_user.id,
            "record": record
        })

    def get_data(self):
        return "get" + str(self.ag)


APIView.register(app, route_prefix="/")
