FROM python:3.13-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
COPY python-utils/requirements.txt python-utils/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir -r python-utils/requirements.txt

COPY gunicorn.conf.py .
COPY src/ src/
COPY python-utils/scripts/ python-utils/scripts/

RUN useradd --no-create-home appuser && chown -R appuser /app
USER appuser

EXPOSE 8000

CMD ["gunicorn", "--config", "gunicorn.conf.py", "app:app"]
