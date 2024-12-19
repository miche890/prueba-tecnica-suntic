from django.db import models
from users.models import User


# Create your models here.
class Document(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING'
        APPROVED = 'APPROVED'
        REJECTED = 'REJECTED'

    title = models.CharField(max_length=255)
    description = models.TextField()
    file = models.FileField(upload_to='media/documents/')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_documents')
    approved_by = models.EmailField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def deactivate(self):
        self.active = False
        self.save()
