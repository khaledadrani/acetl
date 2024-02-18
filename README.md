# acetl

Another CSV Extract-Transform-Load Application!

## Technical details

* Python: 3.10.13
* database: Postgres

## Usage example (Locally)

Assuming you have cloned the repository,
use the docker-compose to launch a database instance:

```commandline
docker compose up
```

Generate some dummy_data using the script in data/:

```commandline
cd data 
python generate_dummy_data.py
cd -
```

Use the cli application to do ETL

```commandline
python cli.py etl-single-file data/retail_data_medium.csv
python cli.py etl-multiple-files /data
```

Note: make sure to install these dependencies if you are working locally (linux)
```commandline
#for postgres psycopg2 driver
apt update && apt install -y build-essential libpq-dev
```

You can run the web application and check it at `http://localhost:8000/docs`

```commandline
python main.py
```

## Kubernetes Architecture Diagram

![Alt Text](./docs/acetl_kubernetes_diagram.drawio.png)


## Done

* ETL “Extract – Transform – Load” pipeline that ingests 1 or multiple CSV files into a Database
* A simple REST API that exposes the recently ingested data:
  •Description: Returns the first 10 lines from Database
  •Request: Get /read/first-chunck
  •Response: 200 OK
  •Response Body: JSON
  •Response Body Description: A list of 10 JSON objects

## TODO

* unit tests (runnable locally)
* a system diagram of your solution deployed to Kubernetes
* improve logging/tracing
* improve Kubernetes Architecture Diagram
