
# Importing required libraries
import yaml
import logging
from kafka import KafkaProducer
from data_generator import generate_heartbeat

# Set up logging to see what's happening
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Read the configuration from config.yaml
with open("config.yml", "r") as file:
    config = yaml.safe_load(file)

# Get Kafka settings from the config file
kafka_config = config["kafka"]
bootstrap_servers = kafka_config["bootstrap_servers"] # localhost:9093
topic = kafka_config["topic"] #heartbeats

# Create a Kafka producer
producer = KafkaProducer(
    bootstrap_servers = bootstrap_servers,
    value_serializer = lambda v: str(v).encode("utf-8")
)

