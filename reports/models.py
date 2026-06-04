from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class ResidentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    suburb = models.CharField(max_length=100, help_text="e.g., Pinetown, Westville")

    def __str__(self):
        return f"{self.user.username} Profile"

class WaterFaultReport(models.Model):
    SEVERITY_CHOICES = [
        ('LOW', 'Low - Minor drip or puddle'),
        ('MED', 'Medium - Steady leak'),
        ('HIGH', 'High - Burst pipe / Flooding'),
    ]

    reporter = models.ForeignKey(ResidentProfile, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200, help_text="Short description of the issue")
    description = models.TextField()
    
    # Location tracking
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    street_address = models.CharField(max_length=250, blank=True, null=True)
    
    # Media
    evidence_image = models.ImageField(upload_to='fault_images/', blank=True, null=True)
    
    # Meta
    severity = models.CharField(max_length=4, choices=SEVERITY_CHOICES, default='LOW')
    date_reported = models.DateTimeField(default=timezone.now)
    is_duplicate = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} - {self.get_severity_display()}"

class WorkOrder(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending Review'),
        ('DISPATCHED', 'Team Dispatched'),
        ('IN_PROGRESS', 'Work in Progress'),
        ('RESOLVED', 'Resolved'),
    ]

    report = models.OneToOneField(WaterFaultReport, on_delete=models.CASCADE, related_name='work_order')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='PENDING')
    assigned_team = models.CharField(max_length=100, blank=True, null=True)
    resolution_notes = models.TextField(blank=True, null=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order for {self.report.title} - {self.get_status_display()}"
    
class CommunityMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    suburb = models.CharField(max_length=100, db_index=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"[{self.suburb}] {self.sender.username}: {self.content[:20]}"


