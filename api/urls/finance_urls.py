from django.urls import path
from ..views.finance_views import (
    list_expenses,
    create_expense,
    retrieve_expense,
    update_delete_expense,
    clear_database,
)

urlpatterns = [
    path("expenselist", list_expenses, name="expenselist"),
    path("createexpense/", create_expense, name="createexpense"),
    path("getexpense/<int:pk>/", retrieve_expense, name="getexpense"),
    path(
        "updateexpense/<int:pk>/",
        update_delete_expense,
        name="updateexpense",
    ),
    path("clearall/", clear_database, name="clearallexpenses"),
]
