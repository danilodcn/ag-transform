import os
import json
from flask import Flask, jsonify
from sqlalchemy.engine import create_engine
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

ag = AG(
    n_generations,
    n_population,
    int(n_population / 1.5),  # número de indivíduos para a mutação
    to_test_constraints,
    tables
)

POSTGRES_URI = os.getenv("POSTGRES_URI")

app = Flask(__name__)
app.register_blueprint(ag.ag_bp)

global execute
execute = True

engine = create_engine(POSTGRES_URI)


@app.get("/")
def index():
    data = pd.read_sql('select * from "Population"', engine)

    # import ipdb; ipdb.set_trace()
    return jsonify({
        "status": 1,
        "data": json.loads(data.to_json())
    })
