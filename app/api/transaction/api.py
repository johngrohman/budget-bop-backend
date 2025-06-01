#!/usr/bin/env python3

import csv
from ninja import Query, Router, Schema, FilterSchema, File, Form
from ninja.files import UploadedFile
from typing import List
from .models import Transaction
from ..month.schemas import MonthSchema
from datetime import date, datetime
from uuid import UUID
from django.shortcuts import get_object_or_404
from typing import Optional
from .utils.transactionparser import format_date
from django.db.models.functions import Abs
from .utils.transactionparser import sync_vars_trans

api = Router()


class UploadFileSchema(Schema):
    month_id: UUID


class TransactionInSchema(Schema):
    date: date
    amount: float
    description: str
    category: str


class TransactionOutSchema(Schema):
    id: UUID
    date: date
    amount: float
    description: str
    category: str
    month: MonthSchema


class TransactionFilterSchema(FilterSchema):
    date: Optional[datetime] = None
    amount: Optional[float] = None
    description: Optional[str] = None
    category: Optional[str] = None
    month_id: Optional[UUID] = None


@api.post("/upload")
def upload_transaction_list(
    request, month_id: UUID = Form(...), file: UploadedFile = File(...)
):
    """
    Upload CSV file with transactions.

    1. Parses transactions, inserting them into the database.\n
    2. Creates or updates corresponding variable expenses.
    """

    # Decode file using utf-8
    decoded_file = file.read().decode("utf-8").splitlines()
    reader = csv.reader(decoded_file)

    # Skip the header row
    next(reader, None)

    # Create a list of transaction objects
    transactions = []
    for row in reader:
        try:
            transaction = Transaction(
                date=format_date(row[2]),
                amount=Abs(float(row[4])),
                description=row[7],
                category=row[8],
                month_id=month_id,
            )
            transactions.append(transaction)
        except (IndexError, ValueError) as e:
            print(f"Skipping invalid row {row}: {e}")

    Transaction.objects.bulk_create(transactions, ignore_conflicts=False)

    return {"message": f"Inserted {len(transactions)} transactions successfully."}


# Get transaction and filter by date, amount, description, category, month, year
@api.get("/list", response=List[TransactionOutSchema])
def list_transactions(request, filters: TransactionFilterSchema = Query(...)):
    transactions = Transaction.objects.all()
    transactions = filters.filter(transactions)
    return transactions


# Get transaction by id
@api.get("/{transaction_id}", response=TransactionOutSchema)
def get_transaction_by_id(request, transaction_id: UUID):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    return transaction

@api.get("/month/{month_id}")
def get_transaction_summary(request, month_id: UUID):
    variable_expenses = sync_vars_trans(month_id=month_id)
    return variable_expenses

# Post new transaction
@api.post("/", response=TransactionOutSchema)
def post_transaction(request, payload: TransactionInSchema):
    return Transaction.objects.create(**payload.dict())


# Patch transaction
@api.patch("/{transaction_id}", response=TransactionOutSchema)
def patch_transaction(request, transaction_id: UUID, payload: TransactionInSchema):
    transaction = get_object_or_404(Transaction, id=transaction_id)

    for attr in TransactionInSchema:
        if attr in payload:
            setattr(transaction, str(attr), payload[attr])

    transaction.save()
    return transaction


# Delete Transaction
@api.delete("/{transaction_id}")
def delete_transaction(request, transaction_id: UUID):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    transaction.delete()
    return {"success": True}


# Get total transactions by date, amount, description, category, month, year
# Get trends over time
# Post bulk upload transactions
# Delete multiple transactions
# Post transaction refund
# Post transaction pending
# Post transaction cancellation
