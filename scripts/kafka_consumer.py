
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
    value_serializer = lambda x: eval(x.decode("utf-8")) # Convert bytes back to dictionary
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
    