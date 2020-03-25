# covid19-backend-br

This application aims to help out people on knowing if they met someone with covid19.

[![CircleCI](https://circleci.com/gh/benmezger/covid19-backend-br/tree/dev.svg?style=svg&circle-token=bac59254d41e1efa1be5c97fc7545faf0257c186)](https://circleci.com/gh/benmezger/covid19-backend-br/tree/dev)
[![Black - Formatter](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


## Setup the Project from Scratch

First of all, make sure you have this:
- `Docker`
- `local.env` file
- `python` 3.7

Then you are ready to start:

1. Clone the repo and get in the right branch
```bash
git clone https://github.com/benmezger/covid19-backend-br.git
git checkout dev
```

2. Docker containers:

2.1. If you want to launch both db and web containers:
```bash
docker-compose up --build
```

2.2. If you want to launch just the db container instance and use the web locally:
```bash
docker-compose up -d db
```

3. If you took the `2.2` option you'll need to install the project requirements:

```bash
python3.7 -m venv venv
source venv/bin/activate
pip install -r requirements/dev.txt -r requirements.txt
```

4. On another panel:
```bash
python src/manage.py runserver
```

That's it! You can open your application [here](localhost:8000/admin/).

## Testing

We have tests for the Python code. The steps to run them are:

* Activate your virtual environment with your preferred tool. In case you're using pipenv:
```bash
source venv/bin/activate
```

* Install the requirements with pip
```bash
pip install -r requirements/test.txt
```

* Run the tests
```bash
pytest
```

You can learn more about pytest features [here]([https://docs.pytest.org/en/latest/](https://docs.pytest.org/en/latest/)).

## Linting

```bash
black .
```
