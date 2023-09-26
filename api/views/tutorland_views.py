from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
import json
from ..models import Student, Lesson, Register
from ..serializers import StudentSerializer, LessonSerializer, RegisterSerializer
from itertools import groupby


# Students
@api_view(["GET"])
def list_students(request):
    students = Student.objects.order_by("name")
    serializer = StudentSerializer(students, many=True)
    return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


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
        for lessondata in request.data["lessons"]:
            try:
                lesson = Lesson.objects.get(pk=lessondata["id"])
            except Lesson.DoesNotExist:
                return Response(
                    {"error": "Lesson not found"}, status=status.HTTP_404_NOT_FOUND
                )
            lesson.day = lessondata["day"]
            lesson.time = lessondata["time"]
            lesson.subject = lessondata["subject"]
            lesson.save()
            print("lesson saved")

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Lessons
@api_view(["GET"])
def list_lessons(request):
    lessons = Lesson.objects.order_by("student")
    serializer = LessonSerializer(lessons, many=True)
    return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


@api_view(["POST"])
def create_lesson(request):
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
    if native_day:
        Lesson.objects.create(
            student=student, isonline=is_online, day=native_day, time=native_time
        )
    print(response)
    return Response(status=status.HTTP_201_CREATED)


@api_view(["GET"])
def retrieve_lesson(request, pk):
    try:
        lesson = Lesson.objects.get(pk=pk)
    except Lesson.DoesNotExist:
        return Response({"error": "lesson not found"}, status=status.HTTP_404_NOT_FOUND)
    serializer = LessonSerializer(lesson)
    return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


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


def print_grammar_timetable(request):
    # Query your lessons and sort them by day and time
    lessons = Lesson.objects.all().filter(subject="grammar").order_by("day", "time")

    # Group lessons by day using itertools.groupby
    grouped_lessons = {
        day: list(group)
        for day, group in groupby(lessons, key=lambda lesson: lesson.day)
    }

    context = {"grouped_lessons": grouped_lessons}
    return render(request, "timetable_sheet.html", context)


def print_native_timetable(request):
    # Query your lessons and sort them by day and time
    lessons = Lesson.objects.all().filter(subject="native").order_by("day", "time")

    # Group lessons by day using itertools.groupby
    grouped_lessons = {
        day: list(group)
        for day, group in groupby(lessons, key=lambda lesson: lesson.day)
    }

    context = {"grouped_lessons": grouped_lessons}
    return render(request, "timetable_sheet.html", context)


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

    return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


@api_view(["GET"])
def lessons_weekly(request):
    lessons = Lesson.objects.all().select_related("student")
    serializer = LessonSerializer(
        lessons, many=True
    )  # Pass the queryset, not the model class

    return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


# register
@api_view(["GET"])
def get_register_entry_by_date(request, date):
    # Query the RegisterEntry model to retrieve entries for the given date
    register_entries = Register.objects.filter(date=date)
    serializer = RegisterSerializer(register_entries)
    return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


@api_view(["GET"])
def list_register(request):
    print("listing register")

    register = Register.objects.order_by("-created")
    serializer = RegisterSerializer(register, many=True)
    print("listregdata")
    return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


@api_view(["POST"])
def create_register(request):
    date = datetime.strptime(request.data.get("date"), "%m/%d/%Y")
    attendance = request.data.get("attendance", [])
    existing_entry = Register.objects.filter(date=date).first()

    if existing_entry:
        print("existing")
        existing_entry.entry = json.dumps(attendance)
        existing_entry.save()
        return JsonResponse({"message": "Attendance records updated successfully"})
    if len(attendance) < 1:
        return JsonResponse(
            {"error": "Attendance records are empty"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    Register.objects.create(
        date=date,
        entry=json.dumps(attendance),
    )
    return JsonResponse(
        {"message": "Attendance records created successfully"},
        status=status.HTTP_201_CREATED,
    )
