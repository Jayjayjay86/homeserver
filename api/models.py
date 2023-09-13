from django.db import models

SUBJECT_CHOICES = [("n", "native"), ("g", "grammar")]
PURPOSE_CHOICES = [
    ("hm", "home"),
    ("tr", "travel"),
    ("fd", "food"),
    ("bl", "bills"),
    ("db", "debt"),
    ("cr", "car"),
    ("dg", "dogs"),
    ("wf", "wife"),
    ("hs", "husband"),
    ("sc", "social tax"),
    ("tl", "tutorland"),
    ("cj", "cjgrower"),
    ("ms", "misc"),
]


# Tutorland models here.
class Student(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    name = models.CharField(max_length=30)
    lessons_remaining_grammar_only = models.IntegerField(
        default=0, blank=True, null=True
    )
    lessons_remaining_native_only = models.IntegerField(
        default=0, blank=True, null=True
    )
    lessons_remaining = models.IntegerField(default=0, blank=True, null=True)
    created = models.TimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"


class Lesson(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    day = models.CharField(max_length=10)
    time = models.TimeField()
    subject = models.CharField(choices=SUBJECT_CHOICES, max_length=7)
    isonline = models.BooleanField(default=False)
    created = models.TimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.name} - {self.subject} - {self.day}"

    class Meta:
        verbose_name = "Lesson"
        verbose_name_plural = "Lessons"


class Register(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    created = models.TimeField(auto_now_add=True)
    date = models.DateField()
    entry = models.JSONField()
    submitted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.date}"

    class Meta:
        verbose_name = "The Register"
        verbose_name_plural = "Registries"


# Finance models here.
class Income(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    created = models.TimeField(auto_now_add=True)
    source = models.CharField(max_length=30)
    amount = models.IntegerField()
    date = models.DateField()

    def __str__(self):
        return f"{self.source}- {self.amount}"

    class Meta:
        verbose_name = "Income"
        verbose_name_plural = "Incomings"


class Expense(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    created = models.TimeField(auto_now_add=True)
    purpose = models.CharField(choices=PURPOSE_CHOICES, max_length=2)
    description = models.CharField(max_length=30)
    amount = models.IntegerField(default=0)
    is_monthly = models.BooleanField(default=False)
    is_debt = models.BooleanField(default=False)
    debt_amount = models.IntegerField(default=0)
    date = models.DateField()

    def __str__(self):
        return f"{self.purpose} - {self.description[0:10]}... - {self.date}"

    class Meta:
        verbose_name = "Expense"
        verbose_name_plural = "Expenses"


# Cj Grower models here.
class CuttingsBatch(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    created = models.TimeField(auto_now_add=True)
    strain = models.CharField(max_length=25)
    amount = models.IntegerField()
    date = models.DateField()

    def __str__(self):
        return f"{self.strain} - {self.amount}"

    class Meta:
        verbose_name = "Cuttings Batch"
        verbose_name_plural = "Cuttings"
