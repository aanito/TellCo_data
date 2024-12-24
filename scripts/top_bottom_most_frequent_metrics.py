from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
import pandas as pd

# Load environment variables from the .env file
load_dotenv()

def clean_env_var(var_name):
    """Cleans environment variable by removing comments and whitespace."""
    return os.getenv(var_name).split('#')[0].strip()

# Database connection details
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

# Ensure relevant columns are numeric
numeric_columns = ['TCP DL Retrans. Vol (Bytes)', 'Avg RTT DL (ms)', 'Avg Bearer TP DL (kbps)']
data[numeric_columns] = data[numeric_columns].apply(pd.to_numeric, errors='coerce')

# Handle missing values by replacing them with the mean of the respective column
data[numeric_columns] = data[numeric_columns].fillna(data[numeric_columns].mean())

# Compute top 10, bottom 10, and most frequent TCP retransmission values
tcp_top10 = data['TCP DL Retrans. Vol (Bytes)'].nlargest(10)
tcp_bottom10 = data['TCP DL Retrans. Vol (Bytes)'].nsmallest(10)
tcp_mode = data['TCP DL Retrans. Vol (Bytes)'].mode().iloc[0]

# Compute top 10, bottom 10, and most frequent RTT values
rtt_top10 = data['Avg RTT DL (ms)'].nlargest(10)
rtt_bottom10 = data['Avg RTT DL (ms)'].nsmallest(10)
rtt_mode = data['Avg RTT DL (ms)'].mode().iloc[0]

# Compute top 10, bottom 10, and most frequent throughput values
throughput_top10 = data['Avg Bearer TP DL (kbps)'].nlargest(10)
throughput_bottom10 = data['Avg Bearer TP DL (kbps)'].nsmallest(10)
throughput_mode = data['Avg Bearer TP DL (kbps)'].mode().iloc[0]

# Save results to CSV files
tcp_top10.to_csv('data/tcp_top10.csv', index=False)
tcp_bottom10.to_csv('data/tcp_bottom10.csv', index=False)
pd.DataFrame({'Mode': [tcp_mode]}).to_csv('data/tcp_mode.csv', index=False)

rtt_top10.to_csv('data/rtt_top10.csv', index=False)
rtt_bottom10.to_csv('data/rtt_bottom10.csv', index=False)
pd.DataFrame({'Mode': [rtt_mode]}).to_csv('data/rtt_mode.csv', index=False)

throughput_top10.to_csv('data/throughput_top10.csv', index=False)
throughput_bottom10.to_csv('data/throughput_bottom10.csv', index=False)
pd.DataFrame({'Mode': [throughput_mode]}).to_csv('data/throughput_mode.csv', index=False)

print("Top, Bottom, and Most Frequent metrics computed and saved successfully.")
