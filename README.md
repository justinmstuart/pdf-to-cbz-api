# pdf-to-cbz

A Flask API that converts PDF files to CBZ format.

## Setup

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

Send a `POST` request to `/` with a PDF file:

```bash
curl -X POST http://localhost:8000/ -F "file=@your-file.pdf"
```
