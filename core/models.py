from django.db import models
from userauths.models import User

# Create your models here.

class Team(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(User)

    def __str__(self):
        return self.name

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]

    CATEGORY_CHOICES = [
        ('New', 'New'),
        ('Progress', 'Progress'),
        ('Hold', 'Hold'),
        ('Pending', 'Pending'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    due_date = models.DateField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    assignee = models.ForeignKey(User, related_name='assgned_tasks', on_delete=models.CASCADE, blank=True, null=True)
    assignee_team = models.ForeignKey(Team, related_name='assgned_tasks', on_delete=models.CASCADE, blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    labels = models.ManyToManyField('label', blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
class Label(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class FileAttachment(models.Model):
    task = models.ForeignKey(Task, related_name='attachments', on_delete=models.CASCADE, blank=True)
    file = models.FileField(upload_to='task_attachments')

    def __str__(self):
        return self.task.title
    
class Comment(models.Model):
    task = models.ForeignKey(Task, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on '{self.task.title}'"
    
