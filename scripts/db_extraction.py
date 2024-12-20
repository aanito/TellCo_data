import psycopg2
import csv

# Database connection details
conn = psycopg2.connect(
    dbname="telecom_db",
    user="postgres",
    password="your_new_password",
    host="localhost"
)

# Query to fetch data
query = "SELECT * FROM public.xdr_data"

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
