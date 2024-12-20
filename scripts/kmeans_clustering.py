import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
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

# Normalize the metrics
scaler = StandardScaler()
user_engagement_scaled = scaler.fit_transform(user_engagement[['Dur. (ms)', 'Total DL (Bytes)', 'Total UL (Bytes)', 'Session Count']])

# Perform K-Means clustering (k=3)
kmeans = KMeans(n_clusters=3, random_state=0).fit(user_engagement_scaled)
user_engagement['Cluster'] = kmeans.labels_

# Save clustering results
user_engagement.to_csv('data/user_engagement_with_clusters.csv', index=False)

# Analyze cluster centers
cluster_centers = pd.DataFrame(kmeans.cluster_centers_, columns=user_engagement.columns[:-1])
cluster_centers.to_csv('data/cluster_centers.csv', index=False)
