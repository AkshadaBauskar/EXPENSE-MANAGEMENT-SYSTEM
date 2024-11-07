from calendar import month

import mysql.connector
from contextlib import contextmanager
from backend.logging_setup import setup_logger

logger = setup_logger('db_helper')

@contextmanager
def get_db_cursor(commit=False):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Akshada13@",
        database="expense_manager"
    )

    cursor = connection.cursor(dictionary=True)
    yield cursor
    if commit:
        connection.commit()
    # print("Closing cursor")
    cursor.close()
    connection.close()


def fetch_all_records():
    query = "SELECT * from expenses"

    with get_db_cursor() as cursor:
        cursor.execute(query)
        expenses = cursor.fetchall()
        return expenses


def fetch_expenses_for_date(expense_date):
    logger.info(f"fetch_expenses_for_date called with {expense_date}")
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM expenses WHERE expense_date = %s", (expense_date,))
        expenses = cursor.fetchall()
        return expenses


def insert_expense(expense_date, amount, category, notes):
    logger.info(f"insert_expenses called with {expense_date}, {amount}, {category}, {notes}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(
            "INSERT INTO expenses (expense_date, amount, category, notes) VALUES (%s, %s, %s, %s)",
            (expense_date, amount, category, notes)
        )

def delete_expenses_for_date(expense_date):
    logger.info(f"delete_expenses_for_date called with {expense_date}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("DELETE FROM expenses WHERE expense_date = %s", (expense_date,))

def fetch_expense_summary(start_date, end_date):
    logger.info(f"fetch_expense_summary called with start:{start_date}, end:{end_date}")
    with get_db_cursor() as cursor:
        cursor.execute(
            '''SELECT category, SUM(amount) as total 
            FROM expenses 
            WHERE expense_date BETWEEN %s AND %s 
            GROUP BY category''',
            (start_date, end_date,))
        data = cursor.fetchall()
        return data

def fetch_monthly_summary():
    logger.info("fetch_monthly_summary called")
    with get_db_cursor() as cursor:
        cursor.execute(
            '''SELECT DATE_FORMAT(expense_date, '%M')as month , SUM(amount) as total
            FROM expenses
            GROUP BY month;
            '''
        )
        month_data= cursor.fetchall()
        return month_data



if __name__ == "__main__":
    # all_records= fetch_all_records()
    # records= fetch_expenses_for_date("2024-08-02")
    # for expense in records:
    #     print(expense)
    print(fetch_monthly_summary())
    # summary= fetch_expense_summary('2024-08-01', '2024-08-05')
    # for record in summary:
    #     print(record)
    # insert_expense("2024-08-20", 300, "Food", "Panipuri")
    # delete_expenses_for_date('2024-08-20')
