from setuptools import setup

with open("README.md", "r") as fh:
   long_description = fh.read()

setup(
    name='izypack4class10',
    version='1.0',
    description='Why not to add 10?',
    author='Who cares?',
    author_email='name.surname@gmail.com',
    py_modules=["izypack4class10"],
    package_dir={'': 'src'},
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    url="http://meteo.lt",
)
