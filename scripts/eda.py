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

# Query the dataset
data = pd.read_sql('SELECT * FROM xdr_data;', engine)

# Save the original dataset
data.to_csv('data/xdr_data.csv', index=False)

# Convert relevant columns to numeric to avoid errors
data['Total DL (Bytes)'] = pd.to_numeric(data['Total DL (Bytes)'], errors='coerce')
data['Total UL (Bytes)'] = pd.to_numeric(data['Total UL (Bytes)'], errors='coerce')
data['Dur. (ms)'] = pd.to_numeric(data['Dur. (ms)'], errors='coerce')

# Handle missing values: Replace non-numeric columns with mean of numeric columns only
data.fillna(data.select_dtypes(include=[np.number]).mean(), inplace=True)

# Save data with missing values handled
data.to_csv('data/xdr_data_filled.csv', index=False)

# Create new variable: Total Data (DL + UL)
data['Total Data (Bytes)'] = data['Total DL (Bytes)'] + data['Total UL (Bytes)']

# Segment users into deciles based on total session duration ('Dur. (ms)')
# Use the 'duplicates' parameter to drop duplicate edges
data['Decile'] = pd.qcut(data['Dur. (ms)'], 10, labels=False, duplicates='drop') + 1  # Deciles are typically 1-based

# # Segment users into deciles based on total session duration ('Dur. (ms)')
# data['Decile'] = pd.qcut(data['Dur. (ms)'], 10, labels=False) + 1  # Deciles are typically 1-based

# Compute total data per decile class
decile_data = data.groupby('Decile')['Total Data (Bytes)'].sum()

# Save decile data to CSV
decile_data.to_csv('data/decile_data.csv')

# Basic statistics
basic_stats = data.describe()
basic_stats.to_csv('data/basic_stats.csv')

# Compute standard deviation (dispersion stats) only on numeric columns
numeric_data = data.select_dtypes(include=[np.number])
dispersion_stats = numeric_data.std()
dispersion_stats.to_csv('data/dispersion_stats.csv')

# # Dispersion (standard deviation) for each column
# dispersion_stats = data.std()
# dispersion_stats.to_csv('data/dispersion_stats.csv')
