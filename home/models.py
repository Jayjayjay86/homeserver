from django.db import models


class TranslatedContent(models.Model):
    content = models.TextField()
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"Translated Content (ID: {self.id})"
