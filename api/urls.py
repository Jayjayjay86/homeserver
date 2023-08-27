from django.urls import path
from .views import *

urlpatterns = [
    # path("loadstudents/", populate_database, name="populate-database"),
    path("loadexpenses/", populate_expense_records, name="populate-expenses"),
    # Tutorland URL's
    # Student URL's
    path("all-students/", list_students, name="list-students"),
    path("create-student/", create_student, name="create-student"),
    path("get-student/<int:pk>/", retrieve_student, name="retrieve-student"),
    path(
        "edit-student/<int:pk>/",
        update_delete_student,
        name="update-delete-student",
    ),
    # Lesson URL's
    path("all-lessons/", list_lessons, name="lessons"),
    path("lessons-today/", lessons_today, name="lessons-today"),
    path("lessons-weekly/", lessons_weekly, name="lessons-weekly"),
    path("create-lesson/", create_lesson, name="create-lesson"),
    path("get-lesson/<int:pk>/", retrieve_lesson, name="retrieve-lesson"),
    path("edit-lesson/<int:pk>/", update_delete_lesson, name="update-delete-lesson"),
    # Finass URL's
    # Expense URL's
    path("all-expenses/", list_expenses, name="all-expenses"),
    path("create-expense/", create_expense, name="create-expense"),
    path("get-expense/<int:pk>/", retrieve_expense, name="get-expense"),
    path(
        "edit-expense/<int:pk>/",
        update_delete_expense,
        name="edit-expense",
    ),
    #
    path("clear-all-expenses/", clear_database, name="clear_expense_database"),
    path("backup-expenses/", backup_database, name="backup_database"),
    path("backups/", list_backups, name="list-backup"),
    path("backup/<int:pk>/", delete_backup, name="delete-backup"),
    path("backups/clear/", clear_backups, name="clear_backups"),
]
