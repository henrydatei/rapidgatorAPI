from setuptools import setup

setup(
    name='rapidgatorAPI',
    version='1.0.0',
    description='Rapidgator API Wrapper',
    author='henrydatei',
    author_email='henrydatei@web.de',
    url='https://github.com/henrydatei/rapidgatorAPI',
    packages=['rapidgatorAPI'],
    install_requires=[
        "requests",
        "dacite"
    ],
)