FROM python:3.11-slim-buster

WORKDIR /opt/app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY requirements.txt .

RUN mkdir -p /opt/app/static/ && \
    mkdir -p /opt/app/media/ && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

RUN addgroup --gid 1001 --system app && \
    adduser --no-create-home \
    --shell /bin/false --disabled-password \
    --uid 1001 --system --group app && \
    chown -R app:app /opt/app


USER app

ENTRYPOINT ["sh", "entrypoint.sh"]
