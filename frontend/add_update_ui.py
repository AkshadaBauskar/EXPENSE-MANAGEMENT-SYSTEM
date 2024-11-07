import streamlit as st
from datetime import datetime
import requests

API_URL = 'http://localhost:8000'

def add_update_tab():
    selected_date = st.date_input('Enter date: ', datetime(2024, 8, 2), label_visibility='collapsed')

    # Retrieve existing expenses for the selected date
    response = requests.get(f"{API_URL}/expense/{selected_date}")
    if response.status_code == 200:
        existing_expenses = response.json()

    else:
        st.error("Failed to retrieve expenses")
        existing_expenses = []

    # Categories dropdown options
    categories = ['Rent', 'Food', 'Shopping', 'Entertainment', 'Other']

    # Form to input expenses
    with st.form(key='expense_form'):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.subheader('Amount')
        with col2:
            st.subheader('Category')
        with col3:
            st.subheader('Notes')


        expenses= []
        for i in range(6):
            if i < len(existing_expenses):
                amount= existing_expenses[i]['amount']
                category = existing_expenses[i]['category']
                notes = existing_expenses[i]['notes']
            else:
                amount = 0.0
                category ='Shopping'
                notes =''
            col1, col2, col3 = st.columns(3)

            with col1:
                amount_input= st.number_input('Amount', min_value=0.0, step=1.0, value=amount, key=f'amount_{i}', label_visibility='collapsed')
            with col2:
                category_input= st.selectbox('Category', options=categories,index= categories.index(category), key=f'categories_{i}', label_visibility='collapsed')
            with col3:
                notes_input= st.text_input('Notes', value=notes, key=f'notes_{i}', label_visibility='collapsed')

            expenses.append({
                'amount': amount_input,
                'category':category_input,
                'notes': notes_input})
        # Submit button
        submit_button = st.form_submit_button(label="Submit")
        if submit_button:
            filtered_expenses = [expense for expense in expenses if expense['amount']>0]
            requests.post(f'{API_URL}/expense/{selected_date}', json=filtered_expenses)

            if response.status_code == 200:
                st.success("Expenses updated successfully")
            else:
                st.error("Failed to update expenses.")