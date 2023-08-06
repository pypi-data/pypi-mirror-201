import sys

from setuptools import setup

sys.stderr.write(
    "sepup.py is deprecated. Use `python -m pip install .` instead\n"
)
sys.exit(1)

setup(
    name="pawapi",
    requires=[],
)
