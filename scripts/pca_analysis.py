from dotenv import load_dotenv
import os
from sqlalchemy import create_engine

import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# Load environment variables from the .env file
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
# # Retrieve the PostgreSQL connection details
# DB_USER = os.getenv('DB_USER').split('#')[0].strip()
# DB_PASSWORD = os.getenv('DB_PASSWORD').split('#')[0].strip()
# DB_HOST = os.getenv('DB_HOST').split('#')[0].strip()
# # DB_HOST = os.getenv('DB_HOST').strip()
# DB_PORT = os.getenv('DB_PORT').split('#')[0].strip()
# # DB_PORT = os.getenv('DB_PORT').strip()
# DB_NAME = os.getenv('DB_NAME').split('#')[0].strip()

# Create the connection string
connection_string = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

# Create an SQLAlchemy engine to connect to the database
engine = create_engine(connection_string)
# Query the dataset
data = pd.read_sql('SELECT * FROM xdr_data;', engine)


# **Select features for PCA**
features = [
    'Social Media DL (Bytes)', 'Google DL (Bytes)', 'Email DL (Bytes)',
    'Youtube DL (Bytes)', 'Netflix DL (Bytes)', 'Gaming DL (Bytes)', 'Other DL (Bytes)'
]

# Check if features exist in the dataset
missing_features = [f for f in features if f not in data.columns]
if missing_features:
    print(f"Missing features in dataset: {missing_features}")
    exit()

x = data[features]

# **Standardize the data**
scaler = StandardScaler()
try:
    x_scaled = scaler.fit_transform(x)
except Exception as e:
    print(f"Error during scaling: {e}")
    exit()

# **Perform PCA**
pca = PCA(n_components=2)  # Use 2 components for visualization and simplicity
try:
    principal_components = pca.fit_transform(x_scaled)
except Exception as e:
    print(f"Error during PCA: {e}")
    exit()

# **Create a DataFrame with PCA results**
data_pca = pd.DataFrame(data=principal_components, columns=['PC1', 'PC2'])

# **Save PCA results**
output_dir = 'data'
os.makedirs(output_dir, exist_ok=True)  # Ensure the directory exists
data_pca.to_csv(f'{output_dir}/pca_results.csv', index=False)

# **Plot PCA results**
plt.figure(figsize=(8, 6))
plt.scatter(data_pca['PC1'], data_pca['PC2'], alpha=0.6, c='blue')
plt.title('PCA of Application Data Usage')
plt.xlabel('Principal Component 1 (PC1)')
plt.ylabel('Principal Component 2 (PC2)')
plt.grid(True)
plt.savefig(f'{output_dir}/pca_plot.png')
plt.show()
# # Select features for PCA
# features = ['Social Media DL (Bytes)', 'Google DL (Bytes)', 'Email DL (Bytes)', 'Youtube DL (Bytes)', 'Netflix DL (Bytes)', 'Gaming DL (Bytes)', 'Other DL (Bytes)']
# x = data[features]

# # Standardize the data
# scaler = StandardScaler()
# x_scaled = scaler.fit_transform(x)

# # Perform PCA
# pca = PCA(n_components=2)
# principal_components = pca.fit_transform(x_scaled)

# # Create a DataFrame with PCA results
# data_pca = pd.DataFrame(data=principal_components, columns=['PC1', 'PC2'])

# # Save PCA results
# data_pca.to_csv('data/pca_results.csv', index=False)

# # Plot PCA results (optional)
# import matplotlib.pyplot as plt
# plt.scatter(data_pca['PC1'], data_pca['PC2'])
# plt.title('PCA of Application Data Usage')
# plt.xlabel('PC1')
# plt.ylabel('PC2')
# plt.savefig('data/pca_plot.png')
# plt.show()

# **Explain PCA Variance**
explained_variance = pca.explained_variance_ratio_
print(f"Explained Variance by Components: {explained_variance}")
print(f"Total Variance Explained by PCA: {sum(explained_variance):.2%}")