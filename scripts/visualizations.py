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


# Aggregate traffic by application and find top 10 users per application
application_columns = [
    'Social Media DL (Bytes)', 'Social Media UL (Bytes)',
    'Google DL (Bytes)', 'Google UL (Bytes)',
    'Email DL (Bytes)', 'Email UL (Bytes)',
    'Youtube DL (Bytes)', 'Youtube UL (Bytes)',
    'Netflix DL (Bytes)', 'Netflix UL (Bytes)',
    'Gaming DL (Bytes)', 'Gaming UL (Bytes)',
    'Other DL (Bytes)', 'Other UL (Bytes)'
]

application_traffic = data.groupby('MSISDN/Number')[application_columns].sum()

for app in application_columns:
    top_users = application_traffic.sort_values(by=app, ascending=False).head(10)
    top_users.to_csv(f'data/top_users_by_{app}.csv', index=False)

# Plot the top 3 most-used applications
application_totals = data[application_columns].sum()
top_3_apps = application_totals.sort_values(ascending=False).head(3)
plt.figure(figsize=(10, 6))
top_3_apps.plot(kind='bar', color=['blue', 'orange', 'green'])
plt.title('Top 3 Most Used Applications')
plt.ylabel('Total Traffic (Bytes)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('data/top_3_apps_bar_chart.png')
plt.close()

# Session Duration Distribution
data['Dur. (ms)'].hist(bins=50, figsize=(10, 6))
plt.title('Session Duration Distribution')
plt.xlabel('Duration (ms)')
plt.ylabel('Frequency')
plt.savefig('data/session_duration_histogram.png')
plt.close()

# Data Usage Distribution
data['Total Data (Bytes)'].hist(bins=50, figsize=(10, 6))
plt.title('Total Data Usage Distribution')
plt.xlabel('Data (Bytes)')
plt.ylabel('Frequency')
plt.savefig('data/data_usage_histogram.png')
plt.close()

print("Visualization completed. Results are saved in the 'data' folder.")
