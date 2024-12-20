from dotenv import load_dotenv
import os
from sqlalchemy import create_engine

import pandas as pd
import numpy as np
import psycopg2


# Load environment variables from the .env file
load_dotenv()

# Retrieve the PostgreSQL connection details
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

# Create the connection string
connection_string = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

# Create an SQLAlchemy engine to connect to the database
engine = create_engine(connection_string)

# Connect to the PostgreSQL database
# engine = create_engine('postgresql://postgres:yourpassword@localhost:5432/telecom_db')

# Query the dataset
data = pd.read_sql('SELECT * FROM xdr_data;', engine)

# Save the original dataset
data.to_csv('data/xdr_data.csv', index=False)

# Handle missing values (replace with column mean)
data.fillna(data.mean(), inplace=True)

# Save data with missing values handled
data.to_csv('data/xdr_data_filled.csv', index=False)

# Create new variable: Total Data (DL + UL)
data['Total Data (Bytes)'] = data['Total DL (Bytes)'] + data['Total UL (Bytes)']

# Segment users into deciles based on total session duration
data['Decile'] = pd.qcut(data['Dur. (ms)'], 10, labels=False)

# Compute total data per decile class
decile_data = data.groupby('Decile')['Total Data (Bytes)'].sum()
decile_data.to_csv('data/decile_data.csv')

# Basic statistics
basic_stats = data.describe()
basic_stats.to_csv('data/basic_stats.csv')

# Dispersion (standard deviation)
dispersion_stats = data.std()
dispersion_stats.to_csv('data/dispersion_stats.csv')
