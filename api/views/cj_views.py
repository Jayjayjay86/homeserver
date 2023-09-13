from .models import Expense, Income, Student, Lesson, Register
from django.shortcuts import HttpResponse
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from home_backend.serializers import (
    ExpenseSerializer,
    StudentSerializer,
    LessonSerializer,
    RegisterSerializer,
)
from datetime import datetime
import json
