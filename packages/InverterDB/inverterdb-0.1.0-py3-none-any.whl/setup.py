from setuptools import find_packages, setup
setup(
    name='InverterDB',
    packages=find_packages(),
    install_requires=["SQLAlchemy",'paho_mqtt'],
    version='0.1.0',
    description='Data base and the functions realted to the data base for the inverters',
    author='Jacobo',
    license='IST',
)