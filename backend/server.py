from fastapi import FastAPI, HTTPException
from datetime import date
from . import db_helper
from typing import List
from pydantic import BaseModel

from backend.db_helper import fetch_expense_summary

app = FastAPI()

class Expense(BaseModel):
    amount: float
    category: str
    notes: str

class DateRange(BaseModel):
    start_date: date
    end_date: date

# @app.get('/')
# def get_expenses():
#     return "Received call"

@app.get('/expense/{expense_date}', response_model=List[Expense])
def get_expenses(expense_date: date):
    expenses = db_helper.fetch_expenses_for_date(expense_date)
    # Ensure expenses are returned as JSON-friendly data
    return expenses


@app.post('/expense/{expense_date}')
def add_or_update_expenses(expense_date: date, expenses: List[Expense]):
    db_helper.delete_expenses_for_date(expense_date)
    for expense in expenses:
        db_helper.insert_expense(expense_date, expense.amount, expense.category, expense.notes)

    return {"message: Expense updated successfully."}

@app.get('/analytics/monthly')
def get_monthly_expenses():
    monthly_summary= db_helper.fetch_monthly_summary()
    return  monthly_summary

@app.post('/analytics/')
def get_analytics(date_range: DateRange):
    summary= fetch_expense_summary(date_range.start_date, date_range.end_date)
    if summary is None:
        raise HTTPException(status_code= 500, detail='Failed to retrieve expense summary')

    total = sum([row['total'] for row in summary])

    breakdown= {}
    for row in summary:
        percentage = round((row['total']/total)*100 if total != 0 else 0, 2)
        breakdown[row['category']] ={
            'total': row['total'],
            'percentage': percentage
        }
    return breakdown


# { "Rent": {'total': 7888, 'percentage': 54}}
# { "Shopping": {'total': 415, 'percentage': 21}}


