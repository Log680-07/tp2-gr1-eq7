
# --- Fichier Docker ----#

FROM python:3.7-alpine AS imagelab

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/ ./src

FROM python:3.7-alpine

COPY --from=imagelab /opt/venv /opt/venv
COPY --from=imagelab /app /app

WORKDIR /app

ENV PATH="/opt/venv/bin:$PATH"
ENTRYPOINT  ["python", "-u", "/app/src/main.py"]