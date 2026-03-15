# pdf-to-cbz

A Flask API that converts PDF files to CBZ format.

## Setup

Clone the repository with submodules:

```bash
git clone --recurse-submodules git@github.com:justinmstuart/pdf-to-cbz.git
```

Or, if you've already cloned the repository:

```bash
git submodule update --init --recursive
```

To pull the latest changes from the submodule:

```bash
git submodule update --remote python-utils
```

Then install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Running locally

```bash
cd src
flask --app app run --debug
```

The app will be available at `http://localhost:5000`.

## Running in production

```bash
gunicorn --config gunicorn.conf.py app:app
```

The app will be available at `http://localhost:8000`.

## Usage

## Linting

To check code style and quality, use [pylint](https://pylint.org/). The configuration is in `.pylintrc`.

Install dependencies (if not already done):

```bash
pip install -r requirements.txt
```

Run pylint on the codebase:

```bash
pylint src
```

You can adjust linting rules in the `.pylintrc` file.
