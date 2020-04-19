from django.db import models
from django.utils import timezone
from ussd.models import Volunteer

class Update(models.Model):
    message = models.TextField(max_length=80)
    time = models.DateTimeField(default = timezone.now)

    def __str__(self):
        return str(self.id)