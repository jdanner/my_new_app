from setuptools import setup, find_packages

setup(
    name="my_new_app",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask',
        'flask-sqlalchemy',
        'flask-login',
        'flask-bcrypt',
        'flask-wtf',
        'email-validator',
    ],
)