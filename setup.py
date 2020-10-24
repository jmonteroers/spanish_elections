from setuptools import setup

setup(
    name='spanish_elections',
    version='0.1',
    packages=['spanish_elections'],
    license='MIT',
    author='Juan Antonio Montero de Espinosa',
    description='tools to analyse and predict Spanish elections results',
    python_requires='>=3.6',
    install_requires=[
        'pandas >= 1.1.3',
        'xlrd >= 1.0.0'
    ]
)
