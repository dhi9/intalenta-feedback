from django.db import models

class Feedback(models.Model):
    customer_id = models.IntegerField()
    feedback_text = models.TextField()
    sentiment = models.TextField(null=True, blank=True)
    keywords = models.JSONField(null=True, blank=True)
    timestamp = models.DateTimeField()
    status = models.CharField(max_length=20, default='PENDING')

class FeedbackTask(models.Model):
    task_id = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=50, default='PENDING')
    result = models.JSONField(null=True, blank=True)

    def update_status(self, status):
        self.status = status
        self.save()
