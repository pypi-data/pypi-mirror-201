from setuptools import setup, find_packages

# TODO: version & release management should be automatic
VERSION = "0.0.0.31"

# TODO: redo it with pyproject.toml an poetry -> use Poetry instead
setup(
    name="blazetest-beta",
    version=VERSION,
    author="Abrorjon Ruziboev",
    author_email="abror.ruzibayev@gmail.com",
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    package_data={
        "blazetest": [
            ".dockerignore",
            "Dockerfile",
            "scripts/install_dependencies.sh",
            "deployment/aws/__main__.py",
            "deployment/aws/.envignore",
            "deployment/aws/requirements.txt",
        ],
    },
    install_requires=[
        "click",
        "pytest",
        "PyYAML",
        "toml",
        "dacite",
        "boto3",
        "licensing",
        "pyopenssl>=23.0.0; python_version >= '3.7'",
        "python-logging-loki",
    ],
    entry_points={
        "console_scripts": [
            "blazetest=blazetest.runner:run_tests",
        ],
    },
)
