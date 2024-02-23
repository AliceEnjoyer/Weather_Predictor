FROM python:3.10-slim

WORKDIR weather/

RUN mkdir api && mkdir scripts

COPY api ./api/
COPY scripts ./scripts/
COPY data ./data/
COPY redis ./redis/
COPY __init__.py ./__init__.py

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

ENV FLASK_APP=./api/app.py
EXPOSE 4000

CMD ["sh", "-c", "cd /weather/redis/ && python3 seed.py && cd /weather/ && flask run --host=0.0.0.0 --port=4000 --debug"]

