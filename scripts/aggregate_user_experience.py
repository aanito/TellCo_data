from dotenv import load_dotenv
import os
import pandas as pd
from sqlalchemy import create_engine

# Load environment variables
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

# Create an SQLAlchemy engine
engine = create_engine(connection_string)

# Query the dataset
data = pd.read_sql('SELECT * FROM xdr_data;', engine)

# Handle missing values by replacing with mean or mode
def handle_missing_values(df):
    numerical_cols = df.select_dtypes(include=['float64', 'int64']).columns
    categorical_cols = df.select_dtypes(include=['object']).columns

    for col in numerical_cols:
        df[col].fillna(df[col].mean(), inplace=True)

    for col in categorical_cols:
        df[col].fillna(df[col].mode()[0], inplace=True)

    return df

data = handle_missing_values(data)

# Aggregate metrics per customer (MSISDN/Number)
aggregated_data = data.groupby('MSISDN/Number').agg({
    'TCP DL Retrans. Vol (Bytes)': 'mean',
    'TCP UL Retrans. Vol (Bytes)': 'mean',
    'Avg RTT DL (ms)': 'mean',
    'Avg RTT UL (ms)': 'mean',
    'Avg Bearer TP DL (kbps)': 'mean',
    'Avg Bearer TP UL (kbps)': 'mean',
    'Handset Type': lambda x: x.mode()[0]  # Most frequent handset type
}).rename(columns={
    'TCP DL Retrans. Vol (Bytes)': 'Avg TCP DL Retrans',
    'TCP UL Retrans. Vol (Bytes)': 'Avg TCP UL Retrans',
    'Avg RTT DL (ms)': 'Avg RTT DL',
    'Avg RTT UL (ms)': 'Avg RTT UL',
    'Avg Bearer TP DL (kbps)': 'Avg Throughput DL',
    'Avg Bearer TP UL (kbps)': 'Avg Throughput UL'
})

# Calculate average throughput
aggregated_data['Avg Throughput'] = (aggregated_data['Avg Throughput DL'] + aggregated_data['Avg Throughput UL']) / 2

# Save aggregated data to CSV
aggregated_data.to_csv('data/aggregated_user_experience.csv', index=False)

print("Aggregated network parameter; data saved to 'output/aggregated_user_experience.csv'.")
