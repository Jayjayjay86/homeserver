from django.shortcuts import HttpResponse
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
import json
from ..models import Expense, Income
from ..serializers import ExpenseSerializer, IncomeSerializer


@api_view(["GET"])
def clear_database(request):
    Expense.objects.all().delete()
    print("database cleared")
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
def list_expenses(request):
    expenses = Expense.objects.order_by("-date")
    serializer = ExpenseSerializer(expenses, many=True)
    return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


@api_view(["GET"])
def list_income(request):
    income = Income.objects.order_by("-date")
    serializer = IncomeSerializer(expenses, many=True)
    return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


@api_view(["POST"])
def create_expense(request):
    # 1/8/23
    # 'date': '2023-08-01'
    request.data["date"] = datetime.strptime(request.data["date"], "%d/%m/%y").strftime(
        "%Y-%m-%d"
    )

    serializer = ExpenseSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    print(serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def retrieve_expense(request, pk):
    try:
        expense = Expense.objects.get(pk=pk)
    except Expense.DoesNotExist:
        return Response(
            {"error": "Expense not found"}, status=status.HTTP_404_NOT_FOUND
        )

    serializer = ExpenseSerializer(expense)
    return Response(serializer.data)


@api_view(["PUT", "DELETE"])
def update_delete_expense(request, pk):
    try:
        expense = Expense.objects.get(pk=pk)
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
