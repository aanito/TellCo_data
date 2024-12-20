import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sqlalchemy import create_engine

# Connect to the PostgreSQL database
engine = create_engine('postgresql://postgres:yourpassword@localhost:5432/telecom_db')

# Query the dataset
data = pd.read_sql('SELECT * FROM telecom_data;', engine)

# Select features for PCA
features = ['Social Media DL (Bytes)', 'Google DL (Bytes)', 'Email DL (Bytes)', 'Youtube DL (Bytes)', 'Netflix DL (Bytes)', 'Gaming DL (Bytes)', 'Other DL (Bytes)']
x = data[features]

# Standardize the data
scaler = StandardScaler()
x_scaled = scaler.fit_transform(x)

# Perform PCA
pca = PCA(n_components=2)
principal_components = pca.fit_transform(x_scaled)

# Create a DataFrame with PCA results
data_pca = pd.DataFrame(data=principal_components, columns=['PC1', 'PC2'])

# Save PCA results
data_pca.to_csv('data/pca_results.csv', index=False)

# Plot PCA results (optional)
import matplotlib.pyplot as plt
plt.scatter(data_pca['PC1'], data_pca['PC2'])
plt.title('PCA of Application Data Usage')
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.savefig('data/pca_plot.png')
plt.show()
