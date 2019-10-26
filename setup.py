from setuptools import setup, find_packages


def read_requirements_file(requirements_file):
    with open(requirements_file) as f:
        requirements = [
            line.strip()
            for line in f
        ]

    return requirements


setup(
    name="classifier",
    version="0.7.0",
    packages=find_packages(),
    install_requires=read_requirements_file("requirements.txt"),
    test_suite='nose.collector',
    tests_require=read_requirements_file("requirements-test.txt"),
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts': ['classifier-cli=classifier.cli:main'],
    },
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    )
)
