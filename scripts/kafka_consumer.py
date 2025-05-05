
# Importing necessary libraries
import yaml
import logging
import psycopg2
from kafka import KafkaConsumer
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up logging to see what's happening
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Read the configuration from config.yaml
with open("config.yml", "r") as file:
    config = yaml.safe_load(file)

# Get Kafka settings from the config file
kafka_config = config["kafka"]
bootstrap_servers = kafka_config["bootstrap_servers"]
topic = kafka_config["topic"]

# Get PostgreSQL settings from environment variables
db_host = config["postgres"]["host"]
db_port = config["postgres"]["port"]
db_user = os.getenv("POSTGRESQL_USERNAME")
db_password = os.getenv("POSTGRESQL_PASSWORD")
db_name = os.getenv("POSTGRESQL_DATABASE")

# Create a Kafka consumer
consumer = KafkaConsumer(
    topic,
    bootstrap_servers = bootstrap_servers,
    group_id = "heartbeat_consumer_group", # Added group_id for offset tracking
    auto_offset_reset = "earliest",  
    enable_auto_commit = True,  # Automatically commit offsets
    value_deserializer = lambda x: eval(x.decode("utf-8")) # Convert bytes back to dictionary
)

# Connect to PostgreSQL
conn = psycopg2.connect(
    host = db_host,
    port = db_port,
    user = db_user,
    password = db_password,
    database = db_name
)
cursor = conn.cursor()


if __name__ == "__main__":
    logging.info("Starting consumer")
    try:
        for message in consumer:
            data = message.value # Get the heart beat data
            # Insert the data into PostgreSQL
            query = """
            INSERT INTO heartbeats (customer_id, timestamp, heart_rate)
            VALUES (%s, %s, %s)
            """
            cursor.execute(query, (data["customer_id"], data["timestamp"], data["heart_rate"]))
            conn.commit()  # Save the changes
            logging.info(f"Stored: {data}")
    except KeyboardInterrupt:
        logging.info("Stopping Consumer")
        cursor.close()
        conn.close()
    except Exception as e:
        logging.error(f"Error: {e}")
        cursor.close()
        conn.close()

       