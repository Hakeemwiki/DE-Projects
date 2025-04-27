
import csv
import os
import random
import time
from datetime import datetime
from faker import Faker

#Initialize Faker instance
fake = Faker()

# Event types you can perform
EVENT_TYPES = ['view', 'purchase']


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
        'user_id': random.randint(1, 1000),
        'user_name': fake.name(),
        'user_email': fake.email(),
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
    filepath = os.path.join('data', filename)
    with open(filepath, mode='w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=[
            'user_id', 'user_name', 'user_email', 'event_type',
            'product_id', 'product_name', 'product_category', 'product_price', 'event_time'
        ])
        writer.writeheader()
        writer.writerows(rows)


if __name__ == '__main__':
    while True:
        # Generate a random number of events (5-15 events per file)
        events = [generate_event() for _ in range(random.randint(5, 15))]
        #Filename with timestamp
        filename = f"events_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.csv"
        write_csv(filename, events)
        print(f"Generated {filename}")
        time.sleep(10) #wait 5 seconds then create next file
        
