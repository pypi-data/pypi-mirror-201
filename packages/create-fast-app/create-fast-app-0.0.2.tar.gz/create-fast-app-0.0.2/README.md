# create-fast-app

`create-fast-app` is a Python package that helps you quickly create new FastAPI projects with basic templates. It includes a command-line interface (CLI) that lets you specify the type of project you want to create, as well as options to attach a machine learning directory.

## Installation
To use create-fastapi-app, you must have Python 3.7 or later installed on your system. You can install the package using pip:

```bash
pip install create-fast-app
```

## Usage
To create a new FastAPI project, run the following command:

```#000000
create-fast-app <project-name> --type=<project-type>
```

Replace `<project-name>` with the desired name for your new project. The `--type` option is used to specify the type of project you want to create. There are three options available:
- `microservice`: Creates a FastAPI microservice project.
- `monolith`: Creates a FastAPI monolith project.
- `ml_app`: Creates a FastAPI machine learning project.

By default, the --type option is set to microservice.


You can also include the --ml option to attach a machine learning directory to your project. This option is only available for microservice and monolith project types.


For example, to create a FastAPI monolith project with a machine learning directory attached, run:

```#000000
create-fast-app my-project --type=monolith --ml=True
```

After running the command, `create-fast-app` will create a new directory with your project name in the current working directory. It will then copy the appropriate FastAPI project template and install the required dependencies in a new virtual environment.

## Project Structure

The directory structure for each project type is as follows:
### Microservice
```
microservice-project-1/
├── requirements/
│   ├── base.txt
│   ├── dev.txt
│   └── prod.txt
├── src/
│   ├── internal/
│   │   └── ...
│   ├── __init__.py
│   ├── app.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── utils.py
├── tests
├── Dockerfile
├── README.md
├── Makefile
├── .env
├── .gitignore
└── venv
```
### Monolith
```
monolith-project-1/
├── requirements/
│   ├── base.txt
│   ├── dev.txt
│   └── prod.txt
├── src/
│   ├── package_one/
│   │   ├── config.py
│   │   ├── constants.py
│   │   ├── dependencies.py
│   │   ├── exceptions.py
│   │   ├── router.py
│   │   ├── schema.py
│   │   ├── service.py
│   │   └── utils.py
│   ├── internal/
│   │   └── ...
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   └── utils.py
├── tests
├── Dockerfile
├── README.md
├── Makefile
├── .env
├── .gitignore
└── venv
```
### Machine learning
```
ml-project-1/
├── data/
│   ├── raw
│   └── processed/
│       ├── train
│       └── test
├── models
├── notebooks
├── src/
│   ├── data/
│   │   └── make_dataset.py
│   ├── feature/
│   │   └── build_features.py
│   ├── models/
│   │   ├── predict.py
│   │   └── train.py
│   └── utils.py
├── Dockerfile
├── README.md
├── Makefile
├── .env
└── .gitignore
```
If attached to a monolith or a microservice project, this directory is mounted into the internal directory of the project.