from backend import db_helper


def test_fetch_expenses_for_date_aug_15():
    expenses= db_helper.fetch_expenses_for_date('2024-08-02')
    assert len(expenses) == 6

def test_fetch_expenses_for_invalid_date():
    expenses= db_helper.fetch_expenses_for_date('9999-08-15')
    assert len(expenses) == 0

def test_fetch_expense_summary_invalid_date():
    summary= db_helper.fetch_expense_summary('2099-01-01', '2099-12-12')
    assert len(summary) == 0

def test_fetch_all_records():
    records = db_helper.fetch_all_records()
    assert len(records) == 54

# def test_insert_expenses_for_date_single_expense():
#     initial_expense= db_helper.fetch_expenses_for_date('2024-08-17')
#     initial_count = len(initial_expense)
#
#     db_helper.insert_expense('2024-08-17', 500, 'Shopping', 'Bought tshirt')
#     updated_expense= db_helper.fetch_expenses_for_date('2024-08-17')
#     updated_count= len(updated_expense)
#     assert updated_count == initial_count + 1
