# from tcc import app
# from tcc.api import app as api
import time
from unittest import TestLoader, runner

import click


@click.group()
def c():
    ...


@c.command()
def rundash():
    app.run_server(debug=True)  # flake8: noqa


@c.command()
def runapi():
    while True:
        try:
            api.run(debug=True)
        except SyntaxError as error:
            print(f"Reestarting the server .... Error = {error}")
            time.sleep(1)


@c.command()
def ag():
    print("Starting ...")
    from app.ag import ag


@c.command()
def tests():
    loader = TestLoader()
    test = loader.discover("tests/core")
    testrunner = runner.TextTestRunner(verbosity=3)
    testrunner.run(test)


c()
