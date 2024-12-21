from dotenv import load_dotenv
import os
from sqlalchemy import create_engine

import pandas as pd

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

# Identify DL and UL columns
dl_columns = [col for col in data.columns if 'DL (Bytes)' in col]
ul_columns = [col for col in data.columns if 'UL (Bytes)' in col]

# Compute correlations with Total Data (Bytes) for DL and UL
dl_correlations = data[dl_columns].corrwith(data['Total DL (Bytes)'])
ul_correlations = data[ul_columns].corrwith(data['Total UL (Bytes)'])

# Save correlations to CSV
dl_correlations.to_csv('data/dl_correlations.csv', header=True)
ul_correlations.to_csv('data/ul_correlations.csv', header=True)

# Print results for review
print("Download (DL) Correlations:")
print(dl_correlations)
print("\nUpload (UL) Correlations:")
print(ul_correlations)

# # Columns for correlation analysis
# app_columns = ['Social Media DL (Bytes)', 'Google DL (Bytes)', 'Youtube DL (Bytes)', 'Email DL (Bytes)', 'Netflix DL (Bytes)', 'Gaming DL (Bytes)', 'Other DL (Bytes)']

# # Compute correlation with Total Data (Bytes)
# correlations = data[app_columns].corrwith(data['Total DL (Bytes)'])
# correlations.to_csv('data/app_data_correlations.csv')

# # Print correlation results
# print("Correlations with Total DL (Bytes):\n", correlations)