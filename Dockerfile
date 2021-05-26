FROM python:3.8
WORKDIR /app
ENV PYTHONPATH /app

RUN apt update -q
RUN apt install -y python3.8 python3.8-venv python3.8-dev build-essential automake pkg-config libtool libffi-dev libgmp-dev libsecp256k1-dev libpython3.8-dev
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
