
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
