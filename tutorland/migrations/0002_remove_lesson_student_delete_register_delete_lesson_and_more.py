# Generated by Django 4.1.1 on 2023-08-10 05:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("tutorland", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="lesson",
            name="student",
        ),
        migrations.DeleteModel(
            name="Register",
        ),
        migrations.DeleteModel(
            name="Lesson",
        ),
        migrations.DeleteModel(
            name="Student",
        ),
    ]
