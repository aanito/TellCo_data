import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Retrieve the MySQL connection details
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

# Streamlit app
st.title('Engagement and EXperience Dashboard')

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Select a page", ["User Overview Analysis", "User Engagement Analysis", "Experience Analysis", "Satisfaction Analysis"])

if page == "User Overview Analysis":
    st.header("User Overview Analysis")
    st.write("This section includes user overview analysis.")
    # Example visualization
    st.bar_chart(data['Total DL (Bytes)'].head(10))

elif page == "User Engagement Analysis":
    st.header("User Engagement Analysis")
    st.write("This section includes user engagement analysis.")
    # Example visualization
    st.line_chart(data['Dur. (ms)'].head(10))

elif page == "Experience Analysis":
    st.header("Experience Analysis")
    st.write("This section includes experience analysis.")
    # Example visualization
    sns.scatterplot(x='Avg RTT DL (ms)', y='Avg Bearer TP DL (kbps)', data=data)
    st.pyplot()

elif page == "Satisfaction Analysis":
    st.header("Satisfaction Analysis")
    st.write("This section includes satisfaction analysis.")
    # Example visualization
    sns.scatterplot(x='EngagementScore', y='SatisfactionScore', data=data)
    st.pyplot()
