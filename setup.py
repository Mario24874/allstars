from setuptools import setup, find_packages

setup(
    name='allstars',
    version='1.0',  # Actualiza esto según sea necesario
    packages=find_packages(where='.', exclude=['tests']),  # Excluye los tests si están en el directorio raíz
    install_requires=[],
    # Agrega otros argumentos según sea necesario
)
