import pandas as pd
from sqlalchemy import create_engine

# Connect to the PostgreSQL database
engine = create_engine('postgresql://postgres:yourpassword@localhost:5432/telecom_db')

# Query the dataset
data = pd.read_sql('SELECT * FROM telecom_data;', engine)

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
