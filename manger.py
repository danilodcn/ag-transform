import click
from unittest import TestLoader, runner
from app import app

@click.group()
def c():
    ...

@c.command()
def runserver():
    app.run(debug=True)


@c.command()
def tests():
    loader = TestLoader()
    test = loader.discover("tests/")
    testrunner = runner.TextTestRunner(verbosity=3)
    testrunner.run(test)

c()
    
