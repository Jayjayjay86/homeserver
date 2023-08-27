from .models import ExpenseRecord, RecordsBackup, Student, Lesson
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    ExpenseSerializer,
    StudentSerializer,
    LessonSerializer,
    RegisterSerializer,
)
from datetime import datetime
import json
from tutorland.tutorland_data import data as sd
from finass.data import data as fd
from django.shortcuts import HttpResponse
from django.http import JsonResponse


def populate_expense_records(request):
    for entry in fd["expense_details"]:
        description = entry["description"]
        purpose = entry["purpose"]
        amount = entry["amount"]
        is_debt = entry["is_debt"]
        is_monthly = entry["is_monthly"]
        is_weekly = entry["is_weekly"]
        is_income = entry["is_income"]
        debt_amount = entry["debt_amount"]
        date = entry["date"]
        expense = ExpenseRecord.objects.create(
            description=description,
            purpose=purpose,
            amount=amount,
            is_debt=is_debt,
            is_monthly=is_monthly,
            is_weekly=is_weekly,
            is_income=is_income,
            debt_amount=debt_amount,
            date=date,
        )

    return HttpResponse("COMPLETE")


def populate_database(request):
    for entry in sd:
        name = entry["name"]
        print(name)
        student = Student.objects.create(name=name, lessons_remaining=0)

        for data in entry["lesson_data"]:
            day = data["day"]
            time = data["time"]
            subject = data["subject"]
            isonline = data["isonline"]
            Lesson.objects.create(
                student=student, day=day, time=time, subject=subject, isonline=isonline
            )
    print("complete")
    return HttpResponse("COMPLETE")


@api_view(["GET"])
def list_students(request):
    students = Student.objects.order_by("name")
    serializer = StudentSerializer(students, many=True)
    return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


@api_view(["DELETE"])
def delete_student(request, pk):
    try:
        student = Student.objects.get(pk=pk)
    except Student.DoesNotExist:
        return Response(
            {"error": "student record not found"}, status=status.HTTP_404_NOT_FOUND
        )

        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["POST"])
def create_student(request):
    print(request.data)
    serializer = StudentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def retrieve_student(request, pk):
    try:
        student = Student.objects.get(pk=pk)
    except Student.DoesNotExist:
        return Response(
            {"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND
        )

    serializer = StudentSerializer(student)
    return Response(serializer.data)


@api_view(["PUT", "DELETE"])
def update_delete_student(request, pk):
    try:
        student = Student.objects.get(pk=pk)
    except Student.DoesNotExist:
        return Response(
            {"error": "Expense not found"}, status=status.HTTP_404_NOT_FOUND
        )

    if request.method == "PUT":
        serializer = StudentSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
def list_lessons(request):
    lessons = Lesson.objects.order_by("student")
    serializer = LessonSerializer(lessons, many=True)
    return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


@api_view(["DELETE"])
def delete_lesson(request, pk):
    try:
        lesson = Lesson.objects.get(pk=pk)
    except Lesson.DoesNotExist:
        return Response(
            {"error": "lesson record not found"}, status=status.HTTP_404_NOT_FOUND
        )

        lesson.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["POST"])
def create_lesson(request):
    print(request.data)

    student = Student.objects.get(id=request.data["student"])
    is_online = request.data["is_online"]
    grammar_day = request.data["grammarDay"]
    native_day = request.data["nativeDay"]
    grammar_time = request.data["grammarTime"]
    native_time = request.data["nativeTime"]
    if grammar_day:
        Lesson.objects.create(
            student=student, isonline=is_online, day=grammar_day, time=grammar_time
        )
        print("make my grammar day")
    if native_day:
        Lesson.objects.create(
            student=student, isonline=is_online, day=native_day, time=native_time
        )
        print("make my native day")
    return Response(status=status.HTTP_201_CREATED)


@api_view(["GET"])
def retrieve_lesson(request, pk):
    try:
        lesson = Lesson.objects.get(pk=pk)
    except Lesson.DoesNotExist:
        return Response({"error": "lesson not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = LessonSerializer(lesson)
    return Response(serializer.data)


@api_view(["PUT", "DELETE"])
def update_delete_lesson(request, pk):
    try:
        lesson = Lesson.objects.get(pk=pk)
    except Lesson.DoesNotExist:
        return Response({"error": "lesson not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "PUT":
        serializer = LessonSerializer(lesson, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        lesson.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
def list_lessons(request):
    lessons = Lesson.objects.all()
    serializer = LessonSerializer(lessons, many=True)
    return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


@api_view(["GET"])
def lessons_today(request):
    time_now = datetime.now()
    todays_day = time_now.strftime("%A").lower()

    lessons = (
        Lesson.objects.filter(day=todays_day).select_related("student").order_by("time")
    )
    serializer = LessonSerializer(
        lessons, many=True
    )  # Pass the queryset, not the model class

    return Response(serializer.data)


@api_view(["GET"])
def lessons_weekly(request):
    lessons = Lesson.objects.all().select_related("student")

    serializer = LessonSerializer(
        lessons, many=True
    )  # Pass the queryset, not the model class

    return Response(serializer.data)


@api_view(["GET"])
def backup_database(request):
    expenses = ExpenseRecord.objects.all()
    serializer = ExpenseSerializer(expenses, many=True)

    # Define a dictionary to store the data
    data = {"date": datetime.today().strftime("%Y-%m-%d"), "expense_details": []}

    # Loop through the Django objects and add them to the dictionary
    if expenses:
        try:
            for expense in expenses:
                expense = {
                    "id": expense.id,
                    "description": expense.description,
                    "purpose": expense.purpose,
                    "amount": expense.amount,
                    "is_debt": expense.is_debt,
                    "debt_amount": expense.debt_amount,
                    "is_weekly": expense.is_weekly,
                    "is_monthly": expense.is_monthly,
                    "is_income": expense.is_income,
                    "created": str(expense.created),
                    "date": expense.date.strftime("%Y-%m-%d"),
                }

                data["expense_details"].append(expense)

            # Save the data as a JSON file with the date and time in the filename
            now = datetime.now()
            date_string = now.strftime("%m-%d")
            filename = f"data_{date_string}.json"
            with open(filename, "w") as file:
                json.dump(data, file, indent=2)
                RecordsBackup.objects.create(records=str(data))

        except Exception as e:
            return Response(serializer.errors, status=status.HTTP_418_IM_A_TEAPOT)

    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
def clear_database(request):
    ExpenseRecord.objects.all().delete()
    print("database cleared")
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
def list_expenses(request):
    expenses = ExpenseRecord.objects.order_by("-date")
    serializer = ExpenseSerializer(expenses, many=True)
    return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


@api_view(["GET"])
def list_backups(request):
    backups = BackupRecords.objects.all()
    serializer = ExpenseSerializer(backups, many=True)
    return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


@api_view(["DELETE"])
def delete_backup(request, pk):
    try:
        backup = ExpenseRecord.objects.get(pk=pk)
    except Expense.DoesNotExist:
        return Response(
            {"error": "backup record not found"}, status=status.HTTP_404_NOT_FOUND
        )

        backup.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
def clear_backups(request):
    BackupRecords.objects.all().delete()
    print("backups cleared")
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["POST"])
def create_expense(request):
    serializer = ExpenseSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def retrieve_expense(request, pk):
    try:
        expense = ExpenseRecord.objects.get(pk=pk)
    except Expense.DoesNotExist:
        return Response(
            {"error": "Expense not found"}, status=status.HTTP_404_NOT_FOUND
        )

    serializer = ExpenseSerializer(expense)
    return Response(serializer.data)


@api_view(["PUT", "DELETE"])
def update_delete_expense(request, pk):
    try:
        expense = ExpenseRecord.objects.get(pk=pk)
    except Expense.DoesNotExist:
        return Response(
            {"error": "Expense not found"}, status=status.HTTP_404_NOT_FOUND
        )

    if request.method == "PUT":
        serializer = ExpenseSerializer(expense, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        expense.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
