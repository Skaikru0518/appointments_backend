from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

# Create your models here.
class Workers(models.Model):
    nev = models.CharField(max_length=200)
    added_at = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="worker_profile", null=True, blank=True)

    def __str__(self):
        return self.nev
    
    class Meta:
        verbose_name_plural = "Workers"

class Client(models.Model):
    nev = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    masseur = models.ForeignKey(
        Workers,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='clients'
    )

    def __str__(self):
        return self.nev
    
class Appointments(models.Model):
    STATUS_CHOICES = [
        ('EGYEZTETES', 'Egyeztetés alatt'),
        ('FOGLALT', 'Foglalt időpontot'),
        ('LEZART', 'Lezárt'),
        ('TOROLT', 'Törölt')
    ]
    nev = models.ForeignKey(Client, on_delete=models.CASCADE)
    date_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='EGYEZTETES')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.nev.nev} - {self.date_time}"
    
    class Meta:
        verbose_name_plural = 'Appointments'
    
