# PDF -> CBZ API

[![Tests](https://github.com/justinmstuart/pdf-to-cbz-api/actions/workflows/tests.yml/badge.svg)](https://github.com/justinmstuart/pdf-to-cbz-api/actions/workflows/tests.yml)

A Flask API that converts PDF files to CBZ format.

## License

[MIT](LICENSE)

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

Then install system dependencies:

**macOS:**

```bash
brew install poppler
```

**Ubuntu/Debian:**

```bash
sudo apt-get install poppler-utils
```

**Fedora/RHEL:**

```bash
sudo dnf install poppler-utils
```

Then install Python dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -r python-utils/requirements.txt
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

## Running with Docker

Ensure the submodule is initialised first:

```bash
git submodule update --init --recursive
```

Build the image:

```bash
docker build -t pdf-to-cbz-api .
```

Run the container. `API_SECRET` is required — all other variables are optional and fall back to defaults:

```bash
docker run -p 8000:8000 \
  -e API_SECRET=<your_secret> \
  -e GUNICORN_WORKERS=2 \
  -e GUNICORN_THREADS=4 \
  -e GUNICORN_TIMEOUT=120 \
  -e GUNICORN_WORKER_CLASS=gthread \
  -e MAX_CONTENT_LENGTH=1048576000 \
  -e MAX_FORM_MEMORY_SIZE=1048576000 \
  pdf-to-cbz-api
```

Or with Docker Compose. Create a `.env` file in the project root:

```env
# Required
API_SECRET=your_secret_here

# Optional — these values are the defaults
GUNICORN_WORKERS=2
GUNICORN_THREADS=4
GUNICORN_TIMEOUT=120
GUNICORN_WORKER_CLASS=gthread
MAX_CONTENT_LENGTH=1048576000
MAX_FORM_MEMORY_SIZE=1048576000
```

Then start the service:

```bash
docker compose up
```

To run in the background:

```bash
docker compose up -d
```

The app will be available at `http://localhost:8000`.

## Usage

Send a PDF file to the API and save the response as a CBZ file:

```bash
curl http://localhost:8000/pdf-to-cbz/ \
  -H "Authorization: Bearer ${API_SECRET}" \
  -F "file=@/path/to/file.pdf;type=application/pdf" \
  --output file.cbz
```

## Linting

To check code style and quality, use [pylint](https://pylint.org/). The configuration is in `.pylintrc`.

Install dependencies (if not already done):

```bash
pip install -r requirements.dev.txt
```

Run pylint on the codebase:

```bash
pylint src
```

You can adjust linting rules in the `.pylintrc` file.
