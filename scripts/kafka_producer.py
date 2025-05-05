
# Importing required libraries
import yaml
import logging
from kafka import KafkaProducer
from data_generator import generate_heartbeat
import time

# Set up logging to see what's happening
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Read the configuration from config.yaml
with open("config.yml", "r") as file:
    config = yaml.safe_load(file)
    # Opens and loads the YAML configuration into a Python dictionary

# Get Kafka settings from the config file
kafka_config = config["kafka"] # Accesses Kafka-related settings
bootstrap_servers = kafka_config["bootstrap_servers"] # Retrieves Kafka broker address: localhost:9093
topic = kafka_config["topic"] # Retrieves Kafka topic name

# Create a Kafka producer
producer = KafkaProducer(
    bootstrap_servers = bootstrap_servers, # Connects to the Kafka broker
    value_serializer = lambda v: str(v).encode("utf-8") # Converts message value to byte string
)

if __name__ == "__main__":
    logging.info(f"Starting producer for topic: {topic}")
    try:
        while True:
            # Generate a heart beat record
            data = generate_heartbeat()
            # Send the data to Kafka
            producer.send(topic, value=data)
            logging.info(f"Sent:{data}")
            producer.flush()  # Make sure the message is sent
            time.sleep(1) # Wait 1 second before sending the next message
    except KeyboardInterrupt:
        logging.info("Stopping Producer")
        producer.close()
    except Exception as e:
        logging.error(f"Error: {e}")
        producer.close()


