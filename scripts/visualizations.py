from dotenv import load_dotenv
import os

import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

load_dotenv()

# **Retrieve the PostgreSQL connection details**
def clean_env_var(var_name):
    """Cleans environment variable by removing comments and whitespace."""
    return os.getenv(var_name).split('#')[0].strip()

DB_USER = clean_env_var('DB_USER')
DB_PASSWORD = clean_env_var('DB_PASSWORD')
DB_HOST = clean_env_var('DB_HOST')
DB_PORT = clean_env_var('DB_PORT')
DB_NAME = clean_env_var('DB_NAME')

# Create the connection string
connection_string = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

# Create an SQLAlchemy engine to connect to the database
engine = create_engine(connection_string)

# Query the dataset
data = pd.read_sql('SELECT * FROM xdr_data;', engine)

# Session Duration Distribution
data['Dur. (ms)'].hist(bins=50)
plt.title('Session Duration Distribution')
plt.xlabel('Duration (ms)')
plt.ylabel('Frequency')
plt.savefig('data/session_duration_histogram.png')
plt.show()

# Data Usage Distribution
data['Total Data (Bytes)'].hist(bins=50)
plt.title('Total Data Usage Distribution')
plt.xlabel('Data (Bytes)')
plt.ylabel('Frequency')
plt.savefig('data/data_usage_histogram.png')
plt.show()
