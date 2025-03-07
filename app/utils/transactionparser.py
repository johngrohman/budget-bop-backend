import sys, csv
from datetime import datetime

def bulk_transaction_create(file, month_id):
    
    with open(file, newline='') as csvfile:
        transaction_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        next(transaction_reader, None)
        output = []
        for row in transaction_reader:
            transaction_object = {
                'date': row[2],
                'amount': row[4],
                'description': row[7],
                'category': row[8],
                'month_id': month_id
            }
            output.append(transaction_object)
        return output
    
def format_date(date_str):
    return datetime.strptime(date_str, "%m/%d/%Y").strftime("%Y-%m-%d")