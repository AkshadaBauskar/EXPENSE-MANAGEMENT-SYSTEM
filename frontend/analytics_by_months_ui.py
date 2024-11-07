import streamlit as st
import requests
import pandas as pd

API_URL = 'http://localhost:8000'

def analytics_by_months():
    st.subheader("Monthly Analytics")

    #Fetch data from /analytics/monthly endpoint
    response = requests.get(f"{API_URL}/analytics/monthly")

    if response.status_code == 200:
        monthly_data = response.json()

    df = pd.DataFrame(monthly_data)

    months ={
        'January':1,'February':2,'March':3,'April':4,
        'May':5,'June':6,'July':7,'August':8,'September':9,
        'October':10,'November':11,'December':12
    }

    df['total'] = df['total'].round(2).apply(lambda x: f"{x:,.2f}")
    df['month_number'] = df['month'].map(months)
    df_sorted= df.sort_values('month_number').drop(columns=['month_number'])

    df_sorted['total'] = pd.to_numeric(df_sorted['total'].str.replace(',', ''))  # Convert total back to float
    st.bar_chart(data=df_sorted.set_index("month")['total'], width=0, height=0)

    st.table(df_sorted)