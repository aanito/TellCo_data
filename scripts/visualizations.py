import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

# Connect to the PostgreSQL database
engine = create_engine('postgresql://postgres:yourpassword@localhost:5432/telecom_db')

# Query the dataset
data = pd.read_sql('SELECT * FROM telecom_data;', engine)

# Session Duration Distribution
data['Dur. (ms)'].hist(bins=50)
plt.title('Session Duration Distribution')
plt.xlabel('Duration (ms)')
plt.ylabel('Frequency')
plt.savefig('data/session_duration_histogram.png')
plt.show()

# Data Usage Distribution
data['Total Data (Bytes)'].hist(bins=50)
plt.title('Total Data Usage Distribution')
plt.xlabel('Data (Bytes)')
plt.ylabel('Frequency')
plt.savefig('data/data_usage_histogram.png')
plt.show()
