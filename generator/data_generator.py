
import csv
import os
import random
import time
from datetime import datetime
from faker import Faker
import logging
from dotenv import load_dotenv

#Logging 
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

#load environment variable from the .env file
load_dotenv()

#Initialize Faker instance
fake = Faker()

# Load generator settings from environment variables
EVENT_TYPES = os.getenv('EVENT_TYPES', 'view,purchase').split(',')
MIN_EVENTS = int(os.getenv('MIN_EVENTS', 100))  # Minimum events per file
MAX_EVENTS = int(os.getenv('MAX_EVENTS', 1000))  # Maximum events per file
SLEEP_INTERVAL = int(os.getenv('SLEEP_INTERVAL', 15))  # Seconds between file generation


# Sample products for data generation
PRODUCTS = [
    {'product_id': 1, 'product_name': 'iPhone 15', 'product_category': 'Electronics', 'product_price': 999.99},
    {'product_id': 2, 'product_name': 'Running Shoes', 'product_category': 'Footwear', 'product_price': 120.00},
    {'product_id': 3, 'product_name': 'Bluetooth Headphones', 'product_category': 'Electronics', 'product_price': 199.99},
    {'product_id': 4, 'product_name': 'T-shirt', 'product_category': 'Apparel', 'product_price': 25.50},
    {'product_id': 5, 'product_name': 'Cooking Pan', 'product_category': 'Kitchen', 'product_price': 45.00},
]

def generate_event():
    product = random.choice(PRODUCTS)
    return {
        'user_id': random.randint(1, 10000),
        'user_name': fake.name(),
        'user_email': fake.unique.email(),
        'event_type': random.choice(EVENT_TYPES),
        'product_id': product['product_id'],
        'product_name': product['product_name'],
        'product_category': product['product_category'],
        'product_price': product['product_price'],
        'event_time': datetime.utcnow().isoformat()
    }


def write_csv(filename, rows):
    """
    Write multiple events into a single CSV file
    """

    #Ensure the data directory exists
    os.makedirs('data', exist_ok=True)
    filepath = os.path.join('data', filename)
    try:
        with open(filepath, mode='w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=[
                'user_id', 'user_name', 'user_email', 'event_type',
                'product_id', 'product_name', 'product_category', 'product_price', 'event_time'
            ])
            writer.writeheader()
            writer.writerows(rows)
            logger.info(f"Successfully wrote {len(rows)} events to {filename}")
    except Exception as e:
        logger.error(f"Error writing {filename}: {e}")
        print(f"Error writing {filename}: {e}")


if __name__ == '__main__':
    logger.info("Starting data generator...")
    try:
        while True:
            # Generate a random number of events (5-15 events per file)
            events = [generate_event() for _ in range(random.randint(100, 1000))]
            #Filename with timestamp
            filename = f"events_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.csv"
            write_csv(filename, events)
            print(f"Generated {filename}")
            logger.info(f"Generated {filename} with {len(events)} events")
            time.sleep(15) #wait 15 seconds then create next file
    except KeyboardInterrupt:
        logger.info("Data generator stopped by user")
        print("Stopped by user")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        
