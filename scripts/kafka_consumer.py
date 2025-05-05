
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
db_host = config["postgress"]["host"]