
#Importing Libraries

import pandas as pd
from sqlalchemy import create_engine
import logging
import os
from dotenv import load_dotenv

#Load dotenv variable
load_dotenv()

# Configure logging with time format and handlers
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", 
                    handlers=[logging.FileHandler("/opt/airflow/logs/pipeline.log"),
                    logging.StreamHandler()])


