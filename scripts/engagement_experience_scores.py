from dotenv import load_dotenv
import os

import numpy as np
import pandas as pd
from scipy.spatial.distance import euclidean
from sqlalchemy import create_engine

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.cluster import KMeans

# Load environment variables from the .env file
load_dotenv()

# Retrieve the PostgreSQL connection details
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

# Assuming these are the coordinates for the cluster centroids
less_engaged_centroid = np.array([0.00691997, 0.08026765, -1.95877131])  # Replaced with values from centroid analysis
worst_experience_centroid = np.array([2.06958631, 1.38166782, 22.41821459])  # Replaced with values from centroid analysis

# Function to calculate Euclidean distance
def calculate_euclidean_distance(point1, point2):
    return euclidean(point1, point2)

# Calculate engagement and experience scores for each user
data['EngagementScore'] = data.apply(lambda row: calculate_euclidean_distance(row[['Avg RTT DL (ms)', 'Avg RTT UL (ms)', 'DL TP < 50 Kbps (%)']], less_engaged_centroid), axis=1)
data['ExperienceScore'] = data.apply(lambda row: calculate_euclidean_distance(row[['Avg Bearer TP DL (kbps)', 'Avg Bearer TP UL (kbps)', 'TCP DL Retrans. Vol (Bytes)']], worst_experience_centroid), axis=1)

# Calculate satisfaction score as the average of engagement and experience scores
data['SatisfactionScore'] = (data['EngagementScore'] + data['ExperienceScore']) / 2

# Report the top 10 satisfied customers
top_10_satisfied_customers = data.nlargest(10, 'SatisfactionScore')
print(top_10_satisfied_customers[['MSISDN/Number', 'SatisfactionScore']])

# Assuming data has features for the regression model
X = data[['EngagementScore', 'ExperienceScore']]
y = data['SatisfactionScore']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Build and train the regression model
regression_model = LinearRegression()
regression_model.fit(X_train, y_train)

# Predict satisfaction score for the test set
y_pred = regression_model.predict(X_test)

# Evaluate the model
print("MSE:", mean_squared_error(y_test, y_pred))
print("R^2:", r2_score(y_test, y_pred))

# K-Means clustering on the engagement and experience scores
kmeans = KMeans(n_clusters=2, random_state=42)
data['Cluster'] = kmeans.fit_predict(data[['EngagementScore', 'ExperienceScore']])

# Print cluster centers
print("Cluster Centers:", kmeans.cluster_centers_)

# Aggregate scores per cluster
cluster_aggregates = data.groupby('Cluster').agg({'SatisfactionScore': 'mean', 'ExperienceScore': 'mean'}).reset_index()
print(cluster_aggregates)


# Create table if not exists 
create_table_query = '''
CREATE TABLE IF NOT EXISTS user_scores ( 
    UserID VARCHAR(255), 
    EngagementScore FLOAT, 
    ExperienceScore FLOAT, 
    SatisfactionScore FLOAT 
) 
'''

engine.execute(create_table_query) # Insert data into the table data.to_sql('user_scores', engine, if_exists='replace', index=False)

# Verify the exported data 
query = 'SELECT * FROM user_scores' 
exported_data = pd.read_sql(query, engine)
print(exported_data)