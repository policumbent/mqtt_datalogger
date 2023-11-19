import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import time

# Connect to SQLite database
conn = sqlite3.connect('test.db')

# List of columns in table
topics_miriam_csv = [
    "latitude",
    "longitude",
    "altitude",
    "distance_gps",
    "speed_gps",
    "timestamp",
    "CO2",
    "temp",
    "TVOC",
    "power",
    "heartrate",
    "rpm_wheel",
    "rpm_pedal",
    "distance_hall",
    "speed_hall",
    "gear",
    "receiver",
    "error",
    "limit_switch"
]

# Create a dropdown menu for the user to select a column
option = st.selectbox(
    'Which column do you want to visualize?',
    topics_miriam_csv
)

# Query the database for the selected column
query = f"SELECT timestamp, {option} FROM Miriam"
df = pd.read_sql_query(query, conn)
query2 = f"SELECT {option} FROM Miriam ORDER BY timestamp DESC LIMIT 30"
df2 = pd.read_sql_query(query2, conn)
# Plot the data
st.write(f'## Plot of {option} over time')
fig, ax = plt.subplots()
ax.plot(df['timestamp'], df[option])
st.pyplot(fig)
'''------'''
#df2 = df2.sort_values('timestamp', ascending=True)
'''------'''
st.line_chart(df2[option].head(30))
st.line_chart(df[option])
# Rerun the app every 1 second to update the graph
'''------'''

time.sleep(1)
st.experimental_rerun()
