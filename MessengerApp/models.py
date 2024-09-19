from django.db import models

class UsersDatabase(models.Model):
    Name = models.CharField(max_length=100, unique=True)
    username = models.CharField(max_length=100, blank=True, null=True)
    Date = models.DateField()
    Note = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.Name