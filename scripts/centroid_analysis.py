from dotenv import load_dotenv
import os

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sqlalchemy import create_engine


# Load environment variables from the .env file
load_dotenv()

# Retrieve the postgresql connection details
DB_USER = os.getenv('DB_USER').split('#')[0].strip()
DB_PASSWORD = os.getenv('DB_PASSWORD').split('#')[0].strip()
DB_HOST = os.getenv('DB_HOST').split('#')[0].strip()
DB_PORT = os.getenv('DB_PORT').split('#')[0].strip()
DB_NAME = os.getenv('DB_NAME').split('#')[0].strip()

# Create the connection string
connection_string = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

# Create an SQLAlchemy engine to connect to the database
engine = create_engine(connection_string)

# Query the dataset
data = pd.read_sql('SELECT * FROM xdr_data;', engine)

# Ensure relevant columns are numeric and handle missing values
numeric_columns = ['Avg RTT DL (ms)', 'Avg RTT UL (ms)', 'DL TP < 50 Kbps (%)', 'Avg Bearer TP DL (kbps)', 'Avg Bearer TP UL (kbps)', 'TCP DL Retrans. Vol (Bytes)']
data[numeric_columns] = data[numeric_columns].apply(pd.to_numeric, errors='coerce')
data[numeric_columns] = data[numeric_columns].fillna(data[numeric_columns].mean())

# Select relevant columns for clustering
engagement_data = data[['Avg RTT DL (ms)', 'Avg RTT UL (ms)', 'DL TP < 50 Kbps (%)']]
experience_data = data[['Avg Bearer TP DL (kbps)', 'Avg Bearer TP UL (kbps)', 'TCP DL Retrans. Vol (Bytes)']]

# Standardize the data if needed (optional)
scaler = StandardScaler()
engagement_data = scaler.fit_transform(engagement_data)
experience_data = scaler.fit_transform(experience_data)

# Perform K-Means clustering to identify less engaged cluster
kmeans_engagement = KMeans(n_clusters=3, random_state=42)
data['EngagementCluster'] = kmeans_engagement.fit_predict(engagement_data)
less_engaged_centroid = kmeans_engagement.cluster_centers_[np.argmin(kmeans_engagement.cluster_centers_.sum(axis=1))]

# Perform K-Means clustering to identify worst experience cluster
kmeans_experience = KMeans(n_clusters=3, random_state=42)
data['ExperienceCluster'] = kmeans_experience.fit_predict(experience_data)
worst_experience_centroid = kmeans_experience.cluster_centers_[np.argmax(kmeans_experience.cluster_centers_.sum(axis=1))]

print("Less Engaged Centroid:", less_engaged_centroid)
print("Worst Experience Centroid:", worst_experience_centroid)
