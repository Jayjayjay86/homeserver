from django.urls import path
from ..views.backup_views import (
    delete_backup,
    clear_backups,
    list_backups,
    load_student_database,
    load_finance_database,
)

urlpatterns = [
    path("students/load", load_student_database, name="load_student_database"),
    path("expenses/load", load_finance_database, name="load_expense_database"),
    path("backup/<int:pk>/", delete_backup, name="delete-backup"),
    path("backups/clear/", clear_backups, name="clear_backups"),
]
