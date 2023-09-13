from django.urls import path
from ..views.tutorland_views import (
    list_students,
    list_lessons,
    create_student,
    create_lesson,
    retrieve_lesson,
    retrieve_student,
    update_delete_student,
    update_delete_lesson,
    lessons_today,
    lessons_weekly,
    get_register_entry_by_date,
    list_register,
    create_register,
    print_grammar_timetable,
    print_native_timetable,
)

urlpatterns = [
    # Student URLs
    path("studentlist/", list_students, name="studentlist"),
    path("createstudent/", create_student, name="create"),
    path("getstudent/<int:pk>/", retrieve_student, name="getstudent"),
    path(
        "updatestudent/<int:pk>/",
        update_delete_student,
        name="updatestudent",
    ),
    # Lesson URLs
    path("lessonlist/", list_lessons, name="lessons"),
    path("lessonstoday/", lessons_today, name="lessonstoday"),
    path("lessonstimetable/", lessons_weekly, name="lessonstimetable"),
    path("createlesson/", create_lesson, name="createlesson"),
    path("getlesson/<int:pk>/", retrieve_lesson, name="getlesson"),
    path("updatelesson/<int:pk>/", update_delete_lesson, name="updatelesson"),
    # print URLs
    path(
        "lessonstimetable/print/grammar/",
        print_grammar_timetable,
        name="print_grammar_timetable",
    ),
    path(
        "lessonstimetable/print/native/",
        print_native_timetable,
        name="print_native_timetable",
    ),
    # Register URLs
    path(
        "tutorland/register/date/<str:date>/",
        get_register_entry_by_date,
        name="registerdate",
    ),
    path("registerlist/", list_register, name="registerlist"),
    path("register/submit", create_register, name="submitregister"),
]
