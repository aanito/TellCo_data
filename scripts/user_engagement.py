from dotenv import load_dotenv
import os
from sqlalchemy import create_engine

import pandas as pd


# Load environment variables from the .env file
load_dotenv()

# Retrieve the PostgreSQL connection details
DB_USER = os.getenv('DB_USER').strip()
DB_PASSWORD = os.getenv('DB_PASSWORD').strip()
DB_HOST = os.getenv('DB_HOST').strip()
DB_PORT = os.getenv('DB_PORT').strip()
DB_NAME = os.getenv('DB_NAME').strip()


print(f"DB_PORT={DB_PORT}")
# Create the connection string
connection_string = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'


# Create an SQLAlchemy engine to connect to the database
engine = create_engine(connection_string)

# Query the dataset
data = pd.read_sql('SELECT * FROM xdr_data;', engine)

# Aggregate engagement metrics by customer
user_engagement = data.groupby('MSISDN/Number').agg({
    'Dur. (ms)': 'sum',
    'Total DL (Bytes)': 'sum',
    'Total UL (Bytes)': 'sum',
    'MSISDN/Number': 'count'
}).rename(columns={'MSISDN/Number': 'Session Count'})

# Save aggregated user engagement metrics
user_engagement.to_csv('data/user_engagement.csv', index=False)

# Top 10 customers by session frequency
top_customers_by_sessions = user_engagement.sort_values(by='Session Count', ascending=False).head(10)
top_customers_by_sessions.to_csv('data/top_customers_by_sessions.csv', index=False)
