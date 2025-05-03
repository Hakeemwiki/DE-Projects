
# Import required libraries
import random
from faker import Faker
from datetime import datetime
import time

# Initialize Faker for generating realistic fake data
fake = Faker()

# Generate a list of 1000 unique customer IDs using Faker
# Faker creates realistic names, formatted as customer IDs
CUSTOMERS = []

for i in range(1000):
    name = fake.name().replace(' ', '_') # Replace spaces with underscores
    customer_id = f"cust_{name}_{str(i).zfill(3)}" # Format: cust_FirstName_LastName_XXX
    CUSTOMERS.append(customer_id)

# Print the first few customer IDs to verify
print(f"Generated {len(CUSTOMERS)} customers IDs. First few: {CUSTOMERS[:5]}")

def generate_heartbeat():
    """
    Generate one heart beat record for a random customer.
    Returns a dictionary with customer_id, timestamp, and heart_rate.
    """

    # Pick a random customer from the list
    customer_id = random.choice(CUSTOMERS)

    # Get the current timestamp in ISO format (e.g., 2025-05-03T12:00:00.123Z)
    timestamp = datetime.utcnow().isoformat() + 'Z'

    # Generate a heart rate between 50 and 120 beats per minute
    # 90% normal range (60-100), 10% outliers (50-59 or 101-120)
    if random.random() < 0.9:
        heart_rate = random.randint(60, 100) #Normal range
    else:
        heart_rate = random.choice([random.randint(50,59), random.randint(101, 120)])

    return {
        "customer_id": customer_id,
        "timestamp": timestamp,
        "heart_rate": heart_rate
    }

if __name__ == "__main__":
    """
    Main loop to generate a large amount of heart beat data.
    Generates 10,000 records by default, with a 0.1-second delay between each.
    """