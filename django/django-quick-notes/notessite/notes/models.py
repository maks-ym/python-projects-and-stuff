from django.contrib import admin
from django.db import models


class Note(models.Model):
    title = models.CharField(max_length=300)
    content = models.TextField()
    update_date = models.DateTimeField(auto_now=True)
    # note_image = ?

    def __str__(self):
        return self.title


# admin.site.register(Note)
