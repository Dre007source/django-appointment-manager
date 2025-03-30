from django.test import TestCase
from django.utils import timezone
from .models import Appointment
from django.core.exceptions import ValidationError
from datetime import timedelta


class AppointmentModelTest(TestCase):
    def test_valid_appointment_creation(self):
        appt = Appointment.objects.create(
            title="Doctor Visit",
            start_time=timezone.now(),
            end_time=timezone.now() + timedelta(hours=1),
        )
        self.assertEqual(Appointment.objects.count(), 1)
        self.assertEqual(appt.title, "Doctor Visit")

    def test_appointment_overlap(self):
        start = timezone.now()
        end = start + timedelta(hours=1)

        Appointment.objects.create(
            title="Existing Appt",
            start_time=start,
            end_time=end
        )

        # Attempt to create overlapping appointment
        appt2 = Appointment(
            title="Overlapping Appt",
            start_time=start + timedelta(minutes=30),
            end_time=end + timedelta(minutes=30)
        )

        # Should raise ValidationError if there's an overlap
        with self.assertRaises(ValidationError):
            appt2.full_clean()  # triggers model validation

        # The database still only has 1 appointment
        self.assertEqual(Appointment.objects.count(), 1)
