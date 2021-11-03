import json
from collections import OrderedDict
# import os
from app.genetic_algorithm.ag import AG
from app.genetic_algorithm.gene import Gene
# from sqlalchemy import create_engine
from dotenv import load_dotenv
load_dotenv()


json_test_trafo_file_name = "tests/json/data_trafo.json"
with open(json_test_trafo_file_name) as file:
    json_test_trafo = json.load(file)

to_test = list(json_test_trafo[0].values())
to_test_variables = to_test[0]
to_test_constraints = to_test[1:-2]
to_test_result = to_test[-2:]

tables_file_name = "tests/json/tabelas.json"
with open(tables_file_name) as file:
    tables = json.load(file)
# import ipdb; ipdb.set_trace()

variations = OrderedDict({
    "Jbt": (1.2, 1.4),
    "Jat": (1.4, 1.6),
    "Bm": (1.5, 1.6),
    "Ksw": (6, 7),
    "kt": (0.45, 0.55),
    "Rjan": (3.4, 3.6),
    "rel": (1.1, 1.2),
    })

gene = Gene()
gene.variations = variations

n_population = 30
n_generations = 10

ag = AG(
    n_generations,
    n_population,
    int(n_population / 1.5),  # número de indivíduos para a mutação
    to_test_constraints,
    tables
)

# POSTGRES_URI=os.getenv("POSTGRES_URI")

# engine = create_engine(POSTGRES_URI)

# for i in range(n_generations):
#     ag.next()
#     ag.population.to_sql(f"Population", engine, if_exists="replace")
