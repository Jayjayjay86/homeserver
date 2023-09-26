from django.http import HttpResponse
from ..models import Expense, Income, Student, Lesson, Register
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
import json
from ..expense_data import data as ed
from ..student_data import data as sd


def load_student_database(request):
    for entry in sd:
        name = entry["name"]

        student = Student.objects.create(name=name, lessons_remaining=0)

        for data in entry["lesson_data"]:
            day = data["day"]
            time = data["time"]
            subject = data["subject"]
            isonline = data["isonline"]

            Lesson.objects.create(
                student=student,
                day=day,
                time=time,
                subject=subject,
                isonline=isonline,
            )

    return HttpResponse("COMPLETE")


def load_finance_database(request):
    for entry in ed["expense_details"]:
        Expense.objects.create(
            purpose=entry["purpose"],
            description=entry["description"],
            amount=entry["amount"],
            is_debt=entry["is_debt"],
            debt_amount=entry["debt_amount"],
            is_monthly=entry["is_monthly"],
            date=entry["date"],
        )
    return HttpResponse("COMPLETE")


# for backing up
@api_view(["GET"])
def backup_finance_database(request):
    expenses = Expense.objects.all()
    # Define a dictionary to store the data
    data = {"date": datetime.today().strftime("%Y-%m-%d"), "expense_details": []}

    # Loop through the Django objects and add them to the dictionary
    if expenses:
        for expense in expenses:
            expense = {
                "id": expense.id,
                "description": expense.description,
                "purpose": expense.purpose,
                "amount": expense.amount,
                "is_debt": expense.is_debt,
                "debt_amount": expense.debt_amount,
                "is_monthly": expense.is_monthly,
                "created": str(expense.created),
                "date": expense.date.strftime("%Y-%m-%d"),
            }

            data["expense_details"].append(expense)
        data["total_amount"] = len(expenses)
        print(data)
        # Save the data as a JSON file with the date and time in the filename
        now = datetime.now()
        date_string = now.strftime("%m-%d")
        filename = f"data_{date_string}.json"
        with open(filename, "w") as file:
            json.dump(data, file, indent=2)

    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
def list_expenses(request):
    expenses = Expense.objects.order_by("-date")
    serializer = ExpenseSerializer(expenses, many=True)
    return Response(serializer.data, status=status.HTTP_202_ACCEPTentry)


@api_view(["GET"])
def list_backups(request):
    backups = BackupRecords.objects.all()
    serializer = ExpenseSerializer(backups, many=True)
    return Response(serializer.data, status=status.HTTP_202_ACCEPTentry)


@api_view(["DELETE"])
def delete_backup(request, pk):
    try:
        backup = Expense.objects.get(pk=pk)
    except Expense.DoesNotExist:
        return Response(
            {"error": "backup record not found"}, status=status.HTTP_404_NOT_FOUND
        )

        backup.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
def clear_backups(request):
    BackupRecords.objects.all().delete()
    print("backups clearentry")
    return Response(status=status.HTTP_204_NO_CONTENT)
