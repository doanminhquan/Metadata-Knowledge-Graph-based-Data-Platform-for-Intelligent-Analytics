## 1. Run the `insert_data.py` file to insert data into MySQL

```bash
# Add your command here
python insert_data.py
```

---

## 2. Start the Debezium Producer via command line

```bash
curl -i -X POST -H "Accept:application/json" -H "Content-Type:application/json" localhost:8083/connectors/ -d '{
  "name": "school-connector",
  "config": {
    "connector.class": "io.debezium.connector.mysql.MySqlConnector",
    "tasks.max": "1",
    "database.hostname": "mysql",
    "database.port": "3306",
    "database.user": "root",
    "database.password": "123456",
    "database.server.id": "184054",
    "topic.prefix": "dbserver1",
    "database.include.list": "school",
    "schema.history.internal.kafka.bootstrap.servers": "kafka:9092",
    "schema.history.internal.kafka.topic": "schema-changes.school"
  }
}'
```

---

## 3. Run 15 python files correspoding to topics/tables name to start the Consumers that listen to the Producer

```bash
# Run each consumer script one by one
python staff.py
python program.py
# ...
python term.py
```

---

## 4. Activate the DAG on Airflow UI

Run script in terminal:
```bash
airflow webserver -p 6777
airflow scheduler
```
- Open Airflow UI at: `http://localhost:6777`
- Find the target DAG
  - Toggle it **On**
  - Click **Trigger DAG** to start it manually

---

## 5. Add a database connection in Metabase UI

- Open Metabase UI at: `http://localhost:3000`
- Go to **Admin Settings** > **Databases** > **Add a Database**
- Select the database type and fill in connection details (host, port, username, password, database name)

---

## 6. Launch the Chatbot module
```bash
cd /data/prompt_service/back_end/ & uvincorn main:app --reload --port 5000
cd /data/prompt_service/front_end/ & npm run dev
```

---

## 7. Create a dashboard by sending a request in the Chatbot UI

- Open the Chatbot UI
- Input a prompt such as:

- Wait for the chatbot to generate the dashboard based on your data in Metabase

---

## 8. Run DataHub ingestion for each tool via UI and command line

### Through the UI:
- Open DataHub UI at: `http://localhost:9002`
- Navigate to **Ingestion**
- Select the source (Kafka, MySQL) and fill in the connection settings
- Run ingestion directly via the interface

### Via command line:

```bash
datahub ingest -c trino-ingest.yml
datahub ingest -c metabase-ingest.yml
```