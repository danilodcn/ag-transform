import click
from unittest import TestLoader, runner
from app import app
from app.api import app as api

@click.group()
def c():
    ...

@c.command()
def rundash():
    app.run_server(debug=True)


@c.command()
def runapi():
    api.run(debug=True)

@c.command()
def ag():
    print("Starting ...")
    from app.ag import ag

@c.command()
def tests():
    loader = TestLoader()
    test = loader.discover("tests/")
    testrunner = runner.TextTestRunner(verbosity=3)
    testrunner.run(test)

c()
    
