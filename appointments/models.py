from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


class Appointment(models.Model):
    title = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    description = models.TextField(blank=True)

    def clean(self):
        """
        Custom validation for Appointment model.
        Ensures start_time < end_time and checks for overlapping appointments.
        Called automatically when model_instance.full_clean() is used
        or a ModelForm is validated (form.is_valid()).
        """

        # 1. Basic validation: start_time must be before end_time
        if self.start_time >= self.end_time:
            raise ValidationError("Start time must be before end time.")

        # 2. Overlap check: see if there's any appointment that intersects this one's time range
        overlapping = Appointment.objects.filter(
            start_time__lt=self.end_time,
            end_time__gt=self.start_time
            # Exclude the current appointment if editing an existing record
        ).exclude(pk=self.pk)

        if overlapping.exists():
            raise ValidationError(
                "This appointment overlaps with another existing appointment.")

    def __str__(self):
        return f"{self.title} ({self.start_time} - {self.end_time})"


class Contact(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20, blank=True)
    # etc.

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
