FROM bitnami/python:3.10.13
WORKDIR /app
RUN apt update && apt install -y build-essential libpq-dev && apt-get clean
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY ./source source/
COPY ./main.py main.py
CMD python main.py