Step 1: Understanding the Dataset
Objective:
The dataset contains xDR records from telecom users, including session details, user activity, device information, and application-level usage. This will be used to analyze user behavior, handset popularity, and application trends.

Table Information:
The dataset is stored in a PostgreSQL table named public.xdr_data. It has 56 attributes, including:

User session details: Start, End, Dur. (ms)
User device details: Handset Manufacturer, Handset Type
Data usage details: Social Media DL (Bytes), Google DL (Bytes), etc.
Total usage metrics: Total DL (Bytes), Total UL (Bytes)

tep 2: Database Setup and Data Extraction
SQL File Analysis:

The provided SQL file includes the schema and a sample COPY command to populate the xdr_data table with raw data.
Database Initialization:

Installed PostgreSQL version 14.10.
Step 1: Install PostgreSQL
On Ubuntu/Debian:

bash
Copy code
sudo apt update
sudo apt install postgresql postgresql-contrib
On macOS:

Use Homebrew:
bash
Copy code
brew update
brew install postgresql
On Windows:

Download and install PostgreSQL from the official website:
https://www.postgresql.org/download/
Follow the installation wizard and remember the superuser password you set during installation.
Step 2: Verify PostgreSQL Installation
Check PostgreSQL version to confirm installation:

bash
Copy code
psql --version
Start the PostgreSQL service:

bash
Copy code
sudo service postgresql start # Ubuntu/Debian
brew services start postgresql # macOS
Step 3: Set Up the Database
Log in to the PostgreSQL command-line interface (CLI):

bash
Copy code
sudo -u postgres psql # Ubuntu/Debian
psql postgres # macOS/Windows
Create a new database for the project:

sql
Copy code
CREATE DATABASE telecom_db;
Exit the CLI:

bash
Copy code
\q
Step 4: Restore the SQL File
Use the psql command to restore the provided SQL dump file:

bash
Copy code
psql -U postgres -d telecom_db -f xdr_data_dump.sql
Replace xdr_data_dump.sql with the path to your SQL file.
If successful, you'll see a confirmation message for each SQL statement.

Step 5: Connect to the Database
Test the database connection:

bash
Copy code
psql -U postgres -d telecom_db
List tables to ensure xdr_data is loaded:

sql
Copy code
\dt
Preview the data:

sql
Copy code
SELECT \* FROM public.xdr_data LIMIT 10;
Step 6: Install Python Libraries
To connect and work with the PostgreSQL database in Python, install the following:

bash
Copy code
pip install psycopg2 pandas matplotlib seaborn
Step 7: Create a Connection Script
Write a script to connect to the database and extract data:

python
Copy code
import psycopg2

# Database connection

try:
conn = psycopg2.connect(
dbname="telecom_db",
user="postgres",
password="your_password",
host="localhost",
port="5432"
)
print("Connected to the database!")
except Exception as e:
print(f"Connection failed: {e}")
Step 8: Proceed with Data Analysis
Follow the project’s steps to aggregate, analyze, and visualize the data.
Automate queries with Python scripts.
Document each step and result for reporting purposes.

Restored the schema and data using the SQL file:
bash

psql -U postgres -d telecom_db -f xdr_data_dump.sql
Connection in Python:

Used psycopg2 to establish a database connection:
python

import psycopg2
conn = psycopg2.connect(
dbname="telecom_db",
user="postgres",
password="password",
host="localhost",
port="5432"
)
Sample Query:

Verified data loading by querying the first 10 rows:
sql
SELECT \* FROM public.xdr_data LIMIT 10;

Task 1: Data Extraction
Description: Extract the telecom data from the PostgreSQL database and save it in a CSV file for easier handling in Python.

Steps Taken:

Connected to the database using the psycopg2 library in Python.
Wrote a SQL query to extract all rows from the xdr_data table.
Exported the data to a CSV file.
Implementation: Create a Python script named extract_data.py in the src/ directory.

python
Copy code
import psycopg2
import csv

# Database connection details

conn = psycopg2.connect(
dbname="telecom_db",
user="postgres",
password="your_password",
host="localhost"
)

# Query to fetch data

query = "SELECT \* FROM public.xdr_data"

# Extract data

with conn.cursor() as cursor:
cursor.execute(query)
rows = cursor.fetchall()
headers = [desc[0] for desc in cursor.description]

# Write data to CSV

with open('../data/xdr_data.csv', 'w', newline='') as csvfile:
writer = csv.writer(csvfile)
writer.writerow(headers)
writer.writerows(rows)

print("Data extraction complete. Saved to '../data/xdr_data.csv'")
Run the Script:

bash
Copy code
python src/extract_data.py
Task 2: Exploratory Data Analysis (EDA)
Description: Perform EDA to understand the dataset structure, identify missing values, and check for outliers.

Steps Taken:

Loaded the CSV file into a Pandas DataFrame.
Checked for null values and summarized each column.
Used statistical measures and visualizations to inspect data distributions.
Implementation: Create a Jupyter notebook in the notebooks/ directory named eda.ipynb.

python
Copy code
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data

data = pd.read_csv('../data/xdr_data.csv')

# Overview

print(data.info())
print(data.describe())

# Check for missing values

print(data.isnull().sum())

# Visualization

sns.heatmap(data.isnull(), cbar=False, cmap='viridis')
plt.title("Missing Values Heatmap")
plt.show()
Insights & Recommendations:

Provide a summary of key findings in the notebook, such as columns with many missing values, outliers in numerical columns, and trends in categorical data.
Task 3: Handset Analysis
Description: Identify the top 10 handsets, top 3 manufacturers, and top 5 handsets for each manufacturer.

Steps Taken:

Filtered relevant columns: Handset Manufacturer and Handset Type.
Used aggregation functions to rank the most popular handsets and manufacturers.
Implementation: Extend the eda.ipynb notebook.

python
Copy code

# Top 10 handsets

top_handsets = data['Handset Type'].value_counts().head(10)
print("Top 10 Handsets:\n", top_handsets)

# Top 3 manufacturers

top_manufacturers = data['Handset Manufacturer'].value_counts().head(3)
print("Top 3 Manufacturers:\n", top_manufacturers)

# Top 5 handsets per manufacturer

for manufacturer in top_manufacturers.index:
handsets = data[data['Handset Manufacturer'] == manufacturer]['Handset Type']
print(f"Top 5 Handsets for {manufacturer}:\n", handsets.value_counts().head(5))
Insights & Recommendations:

Summarize trends for the marketing team, highlighting opportunities for partnerships or campaigns.

Task 1.2 - Exploratory Data Analysis (EDA) Report

1. Data Description and Associated Data Types
   Variables and Data Types:

The dataset includes both numerical and categorical variables. Numerical variables include "Dur. (ms)", "IMSI", "Avg RTT DL (ms)", and others. Categorical variables include "Handset Manufacturer", "Handset Type", and "Last Location Name".
A Python script was used to load the dataset and inspect the columns and their types.
Code Example:

python
Copy code

# Display column names and types

print(data.dtypes) 2. Variable Transformations and Segmentation
Objective: Segment the users into deciles based on the total session duration and compute the total data (DL+UL) per decile class.

Steps Taken:

The "Dur. (ms)" column was used to segment users into decile classes.
The "Total DL (Bytes)" and "Total UL (Bytes)" columns were combined to compute the total data usage for each user.
Users were assigned to deciles based on total session duration.
Code Example:

python
Copy code

# Calculate total duration and total data for each user

data['Total Data (Bytes)'] = data['Total DL (Bytes)'] + data['Total UL (Bytes)']
data['Total Duration (ms)'] = data['Dur. (ms)']

# Segment into deciles based on total session duration

data['Decile'] = pd.qcut(data['Total Duration (ms)'], 10, labels=False)

# Compute total data per decile class

decile_data = data.groupby('Decile')['Total Data (Bytes)'].sum()
print(decile_data)
Findings:

Identified the most engaged deciles and observed patterns in data usage and session duration. 3. Basic Metrics Analysis (Mean, Median, etc.)
Metrics: The mean, median, and other statistical measures (e.g., standard deviation) were calculated for key columns.

Code Example:

python
Copy code

# Calculate basic metrics

basic_stats = data.describe()
print(basic_stats)
Findings:

The mean session duration was found to be high, indicating that users often engage in long sessions.
Variance was high in certain traffic-related columns, suggesting some users consume significantly more data than others. 4. Univariate Analysis: Non-Graphical
Objective: Compute dispersion parameters (variance, standard deviation, etc.) for quantitative variables.

Steps Taken:

Used Pandas' describe() and std() functions to compute dispersion metrics for variables like "Avg RTT DL (ms)", "Avg Bearer TP DL (kbps)", and others.
Code Example:

python
Copy code

# Compute dispersion parameters

dispersion_stats = data.std()
print(dispersion_stats)
Interpretation:

High standard deviation in some variables (e.g., RTT DL) indicates that the network performance varies greatly between users. 5. Univariate Analysis: Graphical
Objective: Visualize data distributions for key quantitative variables.

Steps Taken:

Used histograms and box plots to visualize distributions for session duration and data usage.
Code Example:

python
Copy code

# Visualize distribution of session duration

data['Dur. (ms)'].hist(bins=50)
plt.title('Session Duration Distribution')
plt.show()
Findings:

Session durations followed a skewed distribution, with a small number of long-duration sessions.
Data usage distributions were similarly skewed, suggesting a few heavy data users. 6. Bivariate Analysis: Application vs Total Data (DL+UL)
Objective: Explore the relationship between application usage (e.g., Social Media, YouTube) and total data consumption.

Steps Taken:

Calculated correlations between "Social Media DL (Bytes)", "Google DL (Bytes)", and other application data columns with the total data usage.
Code Example:

python
Copy code

# Correlation of application data usage with total data

data['Total Data (Bytes)'] = data['Total DL (Bytes)'] + data['Total UL (Bytes)']
app_columns = ['Social Media DL (Bytes)', 'Google DL (Bytes)', 'YouTube DL (Bytes)', 'Email DL (Bytes)']
correlations = data[app_columns].corrwith(data['Total Data (Bytes)'])
print(correlations)
Findings:

Strong correlation between total data usage and apps like YouTube and Netflix. 7. Correlation Analysis
Objective: Compute a correlation matrix for specific application data columns.

Steps Taken:

A correlation matrix was created for columns like "Social Media DL", "Google DL", "YouTube DL", and other app-related columns.
Code Example:

python
Copy code

# Compute correlation matrix

correlation_matrix = data[['Social Media DL (Bytes)', 'Google DL (Bytes)', 'Email DL (Bytes)', 'Youtube DL (Bytes)', 'Netflix DL (Bytes)', 'Gaming DL (Bytes)', 'Other DL (Bytes)']].corr()
print(correlation_matrix)
Interpretation:

Strong correlations between similar applications (e.g., Social Media and Google traffic). 8. Dimensionality Reduction: PCA
Objective: Perform Principal Component Analysis (PCA) to reduce data dimensions and interpret results.

Steps Taken:

Used PCA from sklearn to reduce dimensions of the dataset and analyze the most important features.
Code Example:

python
Copy code
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# Standardize the data

features = ['Social Media DL (Bytes)', 'Google DL (Bytes)', 'Email DL (Bytes)', 'Youtube DL (Bytes)', 'Netflix DL (Bytes)', 'Gaming DL (Bytes)', 'Other DL (Bytes)']
x = data[features]
x_scaled = StandardScaler().fit_transform(x)

# Perform PCA

pca = PCA(n_components=2)
principal_components = pca.fit_transform(x_scaled)
data_pca = pd.DataFrame(data=principal_components, columns=['PC1', 'PC2'])

# Plot PCA results

plt.scatter(data_pca['PC1'], data_pca['PC2'])
plt.title('PCA of Application Data Usage')
plt.show()

print(f"Explained variance ratio: {pca.explained*variance_ratio*}")
Findings:

Two principal components explained most of the variance in application data usage, highlighting the importance of traffic from major apps like YouTube and Netflix.
Task 2 - User Engagement Analysis
2.1 - Aggregate Engagement Metrics
Objective: Aggregate metrics (sessions frequency, session duration, total traffic) per customer ID (MSISDN) and report top 10 customers.

Steps Taken:

Aggregated the engagement metrics for each customer.
Used groupby() to compute the total session duration and data usage per customer.
Code Example:

python
Copy code

# Aggregate metrics per customer

user_engagement = data.groupby('MSISDN/Number').agg({
'Dur. (ms)': 'sum',
'Total DL (Bytes)': 'sum',
'Total UL (Bytes)': 'sum',
'MSISDN/Number': 'count'
}).rename(columns={'MSISDN/Number': 'Session Count'})

# Top 10 customers by session frequency

top_customers_by_sessions = user_engagement.sort_values(by='Session Count', ascending=False).head(10)
print(top_customers_by_sessions)
Interpretation:

Found that the top 10 customers had significantly higher session counts and data usage compared to others.
2.2 - Normalization and K-Means Clustering
Objective: Normalize the metrics and perform k-means clustering (k=3) for customer engagement.

Steps Taken:

Normalized the engagement metrics and performed k-means clustering.
Code Example:

python
Copy code
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# Normalize metrics

scaler = StandardScaler()
user_engagement_scaled = scaler.fit_transform(user_engagement[['Dur. (ms)', 'Total DL (Bytes)', 'Total UL (Bytes)', 'Session Count']])

# Perform k-means clustering

kmeans = KMeans(n*clusters=3, random_state=0).fit(user_engagement_scaled)
user_engagement['Cluster'] = kmeans.labels*

# Analyze cluster centers

cluster*centers = pd.DataFrame(kmeans.cluster_centers*, columns=user_engagement.columns[:-1])
print(cluster_centers)
Findings:

Identified three distinct customer clusters based on engagement metrics.
Visualized clusters and interpreted the differences in engagement levels.
2.3 - Top Engaged Users per Application
Objective: Aggregate total traffic per application and identify the top 10 most engaged users for each application.

Steps Taken:

Aggregated data for applications (e.g., Social Media, YouTube) and computed total traffic.
Findings:

The top users for each application were identified, highlighting key customers who drive traffic.
