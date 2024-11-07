import streamlit as st
from analytics_by_category_ui import analytics_tab
from add_update_ui import add_update_tab
from analytics_by_months_ui import analytics_by_months

API_URL = 'http://localhost:8000'

st.title('Expense Management System')

tab1, tab2, tab3 = st.tabs(['Add/Update', 'Analytics By category', 'Analytics By Months'])

with tab1:
    add_update_tab()
with tab2:
    analytics_tab()
with tab3:
    analytics_by_months()


