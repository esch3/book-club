from setuptools import find_packages, setup

setup(
    name='bookclub',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'pip3', 
        'flask',
        'flask_session', 
        'sqlalchemy', 
        'psycopg2-binary',
        'python-dotenv'
    ],
)
