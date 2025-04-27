
import csv
import os
import random
import time
from datetime import datetime

EVENT_TYPES = ['view', 'purchase']


# Sample products for data generation
PRODUCTS = [
    {'product_id': 1, 'product_name': 'iPhone 15', 'product_category': 'Electronics'},
    {'product_id': 2, 'product_name': 'Running Shoes', 'product_category': 'Footwear'},
    {'product_id': 3, 'product_name': 'Bluetooth Headphones', 'product_category': 'Electronics'},
    {'product_id': 4, 'product_name': 'T-shirt', 'product_category': 'Apparel'},
    {'product_id': 5, 'product_name': 'Cooking Pan', 'product_category': 'Kitchen'},
]

def generate_event():
    product = random.choice(PRODUCTS)
    return {
        'user_id': random.randint(1, 1000),
        'event_type': random.choice(EVENT_TYPES),
        'product_id': product['product_id'],
        'product_name': product['product_name'],
        'product_category': product['product_category'],
        'event_time': datetime.utcnow().isoformat()
    }

