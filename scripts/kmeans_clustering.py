from dotenv import load_dotenv 
import os

import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sqlalchemy import create_engine

load_dotenv()

# **Retrieve the PostgreSQL connection details**
def clean_env_var(var_name):
    """Cleans environment variable by removing comments and whitespace."""
    return os.getenv(var_name).split('#')[0].strip()

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

# Aggregate engagement metrics by customer
user_engagement = data.groupby('MSISDN/Number').agg({
    'Dur. (ms)': 'sum',
    'Total DL (Bytes)': 'sum',
    'Total UL (Bytes)': 'sum',
    'MSISDN/Number': 'count'
}).rename(columns={'MSISDN/Number': 'Session Count'})

# Normalize the metrics
scaler = StandardScaler()
user_engagement_scaled = scaler.fit_transform(user_engagement[['Dur. (ms)', 'Total DL (Bytes)', 'Total UL (Bytes)', 'Session Count']])

# Perform K-Means clustering (k=3) with n_init explicitly set
kmeans = KMeans(n_clusters=3, n_init=10, random_state=42).fit(user_engagement_scaled)
user_engagement['Cluster'] = kmeans.labels_

# Save clustering results
user_engagement.to_csv('data/user_engagement_with_clusters.csv', index=False)

# Analyze cluster centers
cluster_centers = pd.DataFrame(kmeans.cluster_centers_, columns=user_engagement.columns[:-1])
cluster_centers.to_csv('data/cluster_centers.csv', index=False)

# Optional: Display cluster centers for manual inspection
print(cluster_centers)



# # Aggregate engagement metrics by customer
# user_engagement = data.groupby('MSISDN/Number').agg({
#     'Dur. (ms)': 'sum',
#     'Total DL (Bytes)': 'sum',
#     'Total UL (Bytes)': 'sum',
#     'MSISDN/Number': 'count'
# }).rename(columns={'MSISDN/Number': 'Session Count'})

# # Normalize the metrics
# scaler = StandardScaler()
# user_engagement_scaled = scaler.fit_transform(user_engagement[['Dur. (ms)', 'Total DL (Bytes)', 'Total UL (Bytes)', 'Session Count']])

# # Perform K-Means clustering (k=3)
# kmeans = KMeans(n_clusters=3, random_state=0).fit(user_engagement_scaled)
# user_engagement['Cluster'] = kmeans.labels_

# # Save clustering results
# user_engagement.to_csv('data/user_engagement_with_clusters.csv', index=False)

# # Analyze cluster centers
# cluster_centers = pd.DataFrame(kmeans.cluster_centers_, columns=user_engagement.columns[:-1])
# cluster_centers.to_csv('data/cluster_centers.csv', index=False)
