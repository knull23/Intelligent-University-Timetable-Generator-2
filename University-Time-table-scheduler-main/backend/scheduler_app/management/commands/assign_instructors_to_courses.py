from django.core.management.base import BaseCommand
from scheduler_app.models import Course, Instructor
import random

class Command(BaseCommand):
    help = 'Assign instructors to courses randomly'

    def handle(self, *args, **kwargs):
        # Get all courses and instructors
        courses = Course.objects.all()
        instructors = list(Instructor.objects.all())

        if not instructors:
            self.stdout.write(self.style.ERROR('No instructors found. Please create instructors first.'))
            return

        assigned_count = 0

        for course in courses:
            # Skip if course already has instructors
            if course.instructors.exists():
                continue

            # Randomly assign 1-3 instructors to each course
            num_instructors = random.randint(1, min(3, len(instructors)))
            selected_instructors = random.sample(instructors, num_instructors)

            course.instructors.set(selected_instructors)
            assigned_count += 1

            self.stdout.write(f"Assigned {len(selected_instructors)} instructors to {course.course_name}")

        self.stdout.write(self.style.SUCCESS(f'Successfully assigned instructors to {assigned_count} courses'))
