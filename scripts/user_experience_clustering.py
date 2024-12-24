from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns

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

# Select relevant columns for clustering
clustering_data = data[['TCP DL Retrans. Vol (Bytes)', 'Avg RTT DL (ms)', 'Avg Bearer TP DL (kbps)']]

# Standardize the data
scaler = StandardScaler()
scaled_data = scaler.fit_transform(clustering_data)

# Apply k-means clustering
kmeans = KMeans(n_clusters=3, random_state=42)
data['Cluster'] = kmeans.fit_predict(scaled_data)

# Save clustering results to CSV
data[['TCP DL Retrans. Vol (Bytes)', 'Avg RTT DL (ms)', 'Avg Bearer TP DL (kbps)', 'Cluster']].to_csv('data/user_experience_clusters.csv', index=False)

# Analyze and describe each cluster
cluster_summary = data.groupby('Cluster')[numeric_columns].mean()
cluster_summary.to_csv('data/cluster_summary.csv')

# Visualization
plt.figure(figsize=(8, 6))
sns.scatterplot(
    x=data['Avg RTT DL (ms)'], 
    y=data['Avg Bearer TP DL (kbps)'], 
    hue=data['Cluster'], 
    palette='viridis', 
    style=data['Cluster']
)
plt.title('User Experience Clustering')
plt.xlabel('Average RTT DL (ms)')
plt.ylabel('Average Throughput DL (kbps)')
plt.legend(title='Cluster')
plt.tight_layout()
plt.savefig('data/clustering_visualization.png')
plt.show()

print("K-means clustering completed and visualizations saved successfully.")
