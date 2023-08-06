from invoke import Program, Collection
from .__about__ import __version__
from . import tasks

# https://docs.pyinvoke.org/en/stable/concepts/library.html
program = Program(
    namespace=Collection.from_module(tasks),
    version=__version__)
