from django.contrib import admin
from api.models import ExpenseRecord, RecordsBackup


admin.site.register(ExpenseRecord)
admin.site.register(RecordsBackup)
