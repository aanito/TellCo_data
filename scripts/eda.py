import pandas as pd
import numpy as np
import psycopg2
from sqlalchemy import create_engine

# Connect to the PostgreSQL database
engine = create_engine('postgresql://postgres:yourpassword@localhost:5432/telecom_db')

# Query the dataset
data = pd.read_sql('SELECT * FROM telecom_data;', engine)

# Save the original dataset
data.to_csv('data/telecom_data.csv', index=False)

# Handle missing values (replace with column mean)
data.fillna(data.mean(), inplace=True)

# Save data with missing values handled
data.to_csv('data/telecom_data_filled.csv', index=False)

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
