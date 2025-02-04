from dotenv import load_dotenv
import os
from sqlalchemy import create_engine

import pandas as pd
import matplotlib.pyplot as plt

# Load environment variables from the .env file
load_dotenv()

# Retrieve the PostgreSQL connection details
DB_USER = os.getenv('DB_USER').split('#')[0].strip()
DB_PASSWORD = os.getenv('DB_PASSWORD').split('#')[0].strip()
DB_HOST = os.getenv('DB_HOST').split('#')[0].strip()
# DB_HOST = os.getenv('DB_HOST').strip()
DB_PORT = os.getenv('DB_PORT').split('#')[0].strip()
# DB_PORT = os.getenv('DB_PORT').strip()
DB_NAME = os.getenv('DB_NAME').split('#')[0].strip()

# Create the connection string
connection_string = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

# Create an SQLAlchemy engine to connect to the database
engine = create_engine(connection_string)

# Query the dataset
data = pd.read_sql('SELECT * FROM xdr_data;', engine)

# Calculate total traffic
data['Total Data (Bytes)'] = data['Total DL (Bytes)'] + data['Total UL (Bytes)']

# Aggregate engagement metrics by customer
user_engagement = data.groupby('MSISDN/Number').agg({
    'Dur. (ms)': 'sum',
    'Total DL (Bytes)': 'sum',
    'Total UL (Bytes)': 'sum',
    'Total Data (Bytes)': 'sum',
    'MSISDN/Number': 'count'
}).rename(columns={'MSISDN/Number': 'Session Count'})

# Save aggregated user engagement metrics
user_engagement.to_csv('data/user_engagement.csv', index=False)


# Top 10 customers by engagement metrics
metrics = ['Dur. (ms)', 'Total DL (Bytes)', 'Total UL (Bytes)', 'Session Count']
for metric in metrics:
    top_customers = user_engagement.sort_values(by=metric, ascending=False).head(10)
    top_customers.to_csv(f'data/top_customers_by_{metric}.csv', index=False)


# Generate bar charts for top customers
for metric in metrics:
    top_customers = user_engagement.sort_values(by=metric, ascending=False).head(10)
    plt.figure(figsize=(10, 6))
    top_customers[metric].plot(kind='bar')
    plt.title(f'Top 10 Customers by {metric}')
    plt.xlabel('Customer ID')
    plt.ylabel(metric)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f'data/top_customers_by_{metric}_bar_chart.png')
    plt.close()