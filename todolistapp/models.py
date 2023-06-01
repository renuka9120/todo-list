from django.db import models

class Task(models.Model):
    STATUS_CHOICES = (
        ('OPEN', 'Open'),
        ('WORKING', 'Working'),
        ('DONE', 'Done'),
        ('OVERDUE', 'Overdue'),
    )

    timestamp = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    due_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='OPEN')

    def __str__(self):
        return self.title

class Tag(models.Model):
    value = models.CharField(max_length=50, unique=True)
    tasks = models.ManyToManyField(Task, related_name='tags')

    def __str__(self):
        return self.value
