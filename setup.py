from setuptools import setup, find_packages


setup(
    name = "classifier",
    version = "0.0.1",
    packages = find_packages(),
    install_requires=[
        "scikit-learn==0.17.1",
        "scipy==0.18.0",
        "numpy==1.11.1",
        "Flask==0.11.1",
        "Flask-RESTful==0.3.5",
        "requests==2.11.1",
        "beautifulsoup4==4.5.1",
        "Flask-JWT==0.3.2",
        "Flask-SQLAlchemy==2.1",
        "psycopg2==2.6.2",
        "alembic==0.8.8",
        "Flask-Script==2.0.5",
        "uWSGI==2.0.14"
    ],
    test_suite = 'nose.collector',
    tests_require =[
        "nose==1.3.7"
    ],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts': ['classifier-cli=classifier.cli:main'],
    }
)
