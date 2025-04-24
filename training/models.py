# models for users, modules, enrollments and uploads
# this file defines all the database tables


from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

# extend user model to include roles
# custom user with roles
class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('trainer', 'Trainer'),
        ('student', 'Student'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

# training module model
class Module(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

# student enrollment model
class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)

# trainer-module assignment model
class TrainerAssignment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)

#weekly lab docs etc for the trainer to add
class ModuleFile(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    week = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to='module_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.module.title} - Week {self.week}: {self.title}"