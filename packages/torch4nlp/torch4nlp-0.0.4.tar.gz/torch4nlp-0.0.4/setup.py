from setuptools import setup
from setuptools import find_packages


print(find_packages())

# pkgs = [p for p in find_packages(exclude=['doc', 'tests', 'tutorials']) if p.startswith('src')]
# print(pkgs)

setup(
    name='youngnlp',
    version='0.0.1',
    description='training and deployment framework for natural language processing',
    package=find_packages('youngnlp'),
    zip_safe=False,
)
