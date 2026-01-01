# backend/scheduler_app/views.py
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import get_object_or_404
import json
import logging
import uuid
import datetime

from .models import (
    Instructor, Room, MeetingTime, Department,
    Course, Section, Class, Timetable
)
from .serializers import *
from .genetic_algorithm import GeneticAlgorithm
from .utils import export_timetable_pdf, export_timetable_excel, check_instructor_conflicts, check_slot_conflicts

logger = logging.getLogger(__name__)


# ----------------------------------------
# ✅ User Profile (JWT-based authentication)
# ----------------------------------------
class UserProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """Return basic user info (used after JWT login)"""
        user = request.user
        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'is_staff': user.is_staff
        }, status=status.HTTP_200_OK)


# ----------------------------------------
# ✅ Change Password
# ----------------------------------------
class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request):
        user = request.user
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            old_password = serializer.data.get("old_password")
            if not user.check_password(old_password):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(serializer.data.get("new_password"))
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ----------------------------------------
# ✅ Scheduler App Endpoints
# ----------------------------------------
class InstructorViewSet(viewsets.ModelViewSet):
    queryset = Instructor.objects.all()
    serializer_class = InstructorSerializer
    permission_classes = [permissions.IsAuthenticated]


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [permissions.IsAuthenticated]


class MeetingTimeViewSet(viewsets.ModelViewSet):
    queryset = MeetingTime.objects.all().order_by('day', 'start_time')
    serializer_class = MeetingTimeSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None  # no pagination for meeting-times listing

    @action(detail=False, methods=['post'])
    def populate_default_slots(self, request):
        """
        Populate default meeting time slots (Mon-Fri).
        Call this endpoint to ensure your DB has the standard slots including the lunch break.
        """
        try:
            created = MeetingTime.generate_default_slots()
            total = MeetingTime.objects.count()
            return Response({'message': 'Default meeting times generated', 'created': created, 'total_slots': total})
        except Exception as e:
            logger.exception("Failed to populate default meeting times")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = []


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = []

    def get_queryset(self):
        """
        Optionally filter by department (id) and year.
        Example: /api/courses/?department=1&year=2
        """
        queryset = Course.objects.all()
        department = self.request.query_params.get('department')
        year = self.request.query_params.get('year')
        if department:
            queryset = queryset.filter(department_id=department)
        if year:
            try:
                year_int = int(year)
                queryset = queryset.filter(year=year_int)
            except ValueError:
                # Invalid year query parameter; return empty queryset or all courses
                queryset = queryset.none()
        return queryset

    @action(detail=False, methods=['get'])
    def get_all_courses(self, request):
        """
        Get all courses without pagination.
        """
        queryset = Course.objects.all()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='assign-instructors')
    def assign_instructors(self, request, pk=None):
        """
        Assign instructors to a course.
        Expects: { "instructors": [instructor_ids] }
        """
        logger.info(f"Attempting to assign instructors to course with pk={pk}")
        course = self.get_object()
        instructor_ids = request.data.get('instructors', [])

        try:
            instructors = Instructor.objects.filter(id__in=instructor_ids)
            course.instructors.set(instructors)
            course.save()

            serializer = self.get_serializer(course)
            return Response({
                'message': 'Instructors assigned successfully',
                'course': serializer.data
            })
        except Exception as e:
            logger.exception("Failed to assign instructors to course")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    permission_classes = []

    def get_queryset(self):
        queryset = Section.objects.all()
        department = self.request.query_params.get('department')
        year = self.request.query_params.get('year')
        if department:
            queryset = queryset.filter(department_id=department)
        if year:
            queryset = queryset.filter(year=year)
        return queryset

    def create(self, request, *args, **kwargs):
        """
        Create a Section. Accepts optional
        `course_instructor_assignments` dict in payload to set instructors for courses.
        """
        data = request.data.copy()
        course_instructor_assignments = data.pop('course_instructor_assignments', {})

        # Collect course IDs from course_instructor_assignments to ensure they are linked to the section
        course_ids = []
        if isinstance(course_instructor_assignments, dict):
            course_ids = [int(k) for k in course_instructor_assignments.keys() if k.isdigit()]

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        section = serializer.save()

        # Update course-instructor assignments if provided
        self._update_course_instructors(course_instructor_assignments)

        # Ensure courses from course_instructor_assignments are linked to the section
        if course_ids:
            courses = Course.objects.filter(id__in=course_ids)
            section.courses.add(*courses)

        # Re-serialize to include updated instructor assignments
        serializer = self.get_serializer(section)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        """
        Update a Section; supports same `course_instructor_assignments`.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        data = request.data.copy()
        course_instructor_assignments = data.pop('course_instructor_assignments', {})

        # Collect course IDs from course_instructor_assignments to ensure they are linked to the section
        course_ids = []
        if isinstance(course_instructor_assignments, dict):
            course_ids = [int(k) for k in course_instructor_assignments.keys() if k.isdigit()]

        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        section = serializer.save()

        self._update_course_instructors(course_instructor_assignments)

        # Ensure courses from course_instructor_assignments are linked to the section
        if course_ids:
            courses = Course.objects.filter(id__in=course_ids)
            section.courses.add(*courses)

        # Re-serialize to include updated instructor assignments
        serializer = self.get_serializer(section)
        return Response(serializer.data)

    def _update_course_instructors(self, course_instructor_assignments):
        """Update instructor assignments for courses.

        Accepts several shapes:
        - {"97": 3, "98": [4, 5]}
        - [{"course": 97, "instructors": [3, 4]}, ...]
        - JSON string of either of the above
        """

        if not course_instructor_assignments:
            logger.info("No course_instructor_assignments provided, skipping.")
            return

        # If it comes as ['{"97": 3, "98": 4}'] from a QueryDict
        if isinstance(course_instructor_assignments, list):
            # Case 1: list with a single JSON string from form-data
            if len(course_instructor_assignments) == 1 and isinstance(course_instructor_assignments[0], str):
                try:
                    course_instructor_assignments = json.loads(course_instructor_assignments[0])
                except json.JSONDecodeError:
                    logger.warning(
                        "Invalid JSON for course_instructor_assignments: %r",
                        course_instructor_assignments[0]
                    )
                    return
            else:
                # Case 2: list of objects:
                #   [{"course": 1, "instructors": [1,2]}, ...]
                normalized = {}
                for item in course_instructor_assignments:
                    if not isinstance(item, dict):
                        continue
                    c_id = (
                        item.get("course")
                        or item.get("course_id")
                        or item.get("courseId")
                        or item.get("id")
                    )
                    inst_val = (
                        item.get("instructors")
                        or item.get("instructor_ids")
                        or item.get("instructorIds")
                        or item.get("instructor")
                    )
                    if c_id is not None:
                        normalized[str(c_id)] = inst_val
                course_instructor_assignments = normalized

        # Handle stringified JSON
        if isinstance(course_instructor_assignments, str):
            try:
                course_instructor_assignments = json.loads(course_instructor_assignments)
            except json.JSONDecodeError:
                logger.warning(
                    "Invalid JSON for course_instructor_assignments string: %r",
                    course_instructor_assignments
                )
                return

        if not isinstance(course_instructor_assignments, dict):
            logger.warning(
                "Unsupported type for course_instructor_assignments: %s",
                type(course_instructor_assignments)
            )
            return

        for raw_course_id, instructor_value in course_instructor_assignments.items():
            # Allow unassigning by sending null / [] / "" / 0
            if not instructor_value:
                try:
                    course = Course.objects.get(id=int(raw_course_id))
                    course.instructors.clear()
                    logger.info("Cleared instructors for course %s", raw_course_id)
                except (Course.DoesNotExist, ValueError):
                    logger.warning("Course %r does not exist while clearing.", raw_course_id)
                continue

            # Normalize instructor ids to list
            if not isinstance(instructor_value, (list, tuple)):
                instructor_ids = [instructor_value]
            else:
                instructor_ids = instructor_value

            # Convert to ints and drop invalid values
            clean_ids = []
            for val in instructor_ids:
                try:
                    clean_ids.append(int(val))
                except (TypeError, ValueError):
                    logger.warning("Invalid instructor id %r for course %r", val, raw_course_id)

            if not clean_ids:
                continue

            try:
                course = Course.objects.get(id=int(raw_course_id))
            except (Course.DoesNotExist, ValueError):
                logger.warning("Course %r does not exist, skipping.", raw_course_id)
                continue

            instructors = Instructor.objects.filter(id__in=clean_ids)
            course.instructors.set(instructors)  # M2M save
            # course.save()  # not required for m2m, but safe if you want
            logger.info(
                "Assigned instructors %s to course %s",
                list(instructors.values_list("id", flat=True)),
                raw_course_id,
            )
            
    @action(detail=True, methods=['get'])
    def instructors(self, request, pk=None):
        """Get instructors who teach courses assigned to this section"""
        section = self.get_object()
        instructors = Instructor.objects.filter(courses_teaching__sections=section).distinct()
        serializer = InstructorSerializer(instructors, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def update_course_instructors(self, request, pk=None):
        """
        Update instructor assignments for courses in this section.
        Expects: { "course_instructor_assignments": { course_id: [instructor_ids] } }
        """
        section = self.get_object()
        course_instructor_assignments = request.data.get('course_instructor_assignments', {})
        self._update_course_instructors(course_instructor_assignments)
        return Response({'message': 'Course instructors updated successfully'})

    @action(detail=True, methods=['post'])
    def auto_assign_courses(self, request, pk=None):
        """
        Assign year, department, and semester matching courses to this section.
        Useful to quickly populate sections with their standard course lists.
        """
        section = self.get_object()
        try:
            # Determine if the section's semester is odd or even
            if section.semester % 2 == 0:
                semesters_to_include = [2, 4, 6, 8]
            else:
                semesters_to_include = [1, 3, 5, 7]

            # Assign courses for the year, department, and all relevant semesters
            year_courses = Course.objects.filter(
                year=section.year,
                department=section.department,
                semester__in=semesters_to_include
            )
            section.courses.set(year_courses)
            return Response({
                'message': 'Courses auto-assigned to section',
                'section': section.section_id,
                'assigned_count': year_courses.count()
            })
        except Exception as e:
            logger.exception("Failed to auto-assign courses to section")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ClassViewSet(viewsets.ModelViewSet):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'class_id'  # Use class_id instead of pk for URL lookups

    @action(detail=False, methods=['patch'])
    def update_slot(self, request):
        """
        Update the meeting time slot for a specific class.
        Expected payload: { "class_id": "class_id_here", "day": "Monday", "time_slot": "09:00-10:00" }
        """
        class_id = request.data.get('class_id')
        if not class_id:
            return Response(
                {'error': 'class_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            class_obj = Class.objects.get(class_id=class_id)
        except Class.DoesNotExist:
            return Response(
                {'error': f'Class with class_id {class_id} not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        day = request.data.get('day')
        time_slot = request.data.get('time_slot')

        if not day or not time_slot:
            return Response(
                {'error': 'Both day and time_slot are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Parse the time slot to find the matching MeetingTime
            start_time_str, end_time_str = time_slot.split('-')
            logger.info(f"Parsing time_slot: {time_slot}, start_time_str: {start_time_str}")

            # Try parsing with seconds first, then fallback to minutes only
            try:
                start_time = datetime.datetime.strptime(start_time_str.strip(), '%H:%M:%S').time()
            except ValueError:
                # Fallback to HH:MM format
                start_time = datetime.datetime.strptime(start_time_str.strip(), '%H:%M').time()

            # Find the meeting time that matches the day and start time
            meeting_time = MeetingTime.objects.get(
                day=day,
                start_time=start_time
            )

            # Check for conflicts before updating
            conflicts = check_slot_conflicts(
                timetable=class_obj.timetables.first(),  # Get the timetable this class belongs to
                new_day=day,
                new_start_time=start_time,
                instructor_id=class_obj.instructor_id,
                room_id=class_obj.room_id,
                section_id=class_obj.section_id,
                exclude_class_id=class_obj.class_id
            )

            if conflicts:
                # Group conflicts by type
                conflict_messages = []
                for conflict in conflicts:
                    conflict_messages.append(
                        f"{conflict['type'].title()} conflict: {conflict['course']} "
                        f"({conflict['section']}) at {conflict['day']} {conflict['time']}"
                    )

                return Response(
                    {
                        'error': 'Cannot move class due to conflicts',
                        'conflicts': conflicts,
                        'conflict_messages': conflict_messages
                    },
                    status=status.HTTP_409_CONFLICT
                )

            # Update the class with the new meeting time
            class_obj.meeting_time = meeting_time
            class_obj.save()

            return Response({
                'message': 'Class slot updated successfully',
                'class_id': class_obj.class_id,
                'new_day': day,
                'new_time_slot': time_slot
            })

        except MeetingTime.DoesNotExist:
            return Response(
                {'error': f'No meeting time found for {day} at {start_time_str}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except ValueError as e:
            return Response(
                {'error': f'Invalid time format: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.exception("Failed to update class slot")
            return Response(
                {'error': f'Failed to update class slot: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class TimetableViewSet(viewsets.ModelViewSet):
    queryset = Timetable.objects.all()
    serializer_class = TimetableSerializer
    permission_classes = []

    def get_queryset(self):
        queryset = Timetable.objects.all()
        department = self.request.query_params.get('department')
        year = self.request.query_params.get('year')
        if department:
            queryset = queryset.filter(department_id=department)
        if year:
            queryset = queryset.filter(year=year)
        return queryset

    # ----------------------------------------
    # Generate Timetable (Genetic Algorithm)
    # ----------------------------------------
    @action(detail=False, methods=['post'], permission_classes=[])
    def generate(self, request):
        """
        Expected POST JSON shape (examples):
        1) Single-department single-year:
           { "department_id": 1, "years": [1], "semester": 1, ... }

        2) Combined multiple depts/years:
           { "department_ids": [1,2], "years": [1,2], "semester": 1, ... }

        The GeneticAlgorithm implementation must accept the args used below.
        """
        serializer = TimetableGenerationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        data = serializer.validated_data

        # normalize inputs to the GA interface used here
        department_ids = data.get('department_ids') or ([data['department_id']] if data.get('department_id') else [])
        years = data.get('years') or ([data['year']] if data.get('year') else [])

        if not department_ids or not years:
            return Response({'error': 'department_ids and years (or department_id/year) are required'}, status=status.HTTP_400_BAD_REQUEST)

        semester_param = data.get('semester')
        if semester_param == 'odd':
            semesters = [1, 3, 5, 7]
        elif semester_param == 'even':
            semesters = [2, 4, 6, 8]
        else:
            try:
                semesters = [int(semester_param)]
            except (ValueError, TypeError):
                return Response({'error': 'Invalid semester format. Use "odd", "even", or a number.'}, status=status.HTTP_400_BAD_REQUEST)

        # Auto-assign courses to sections if not already assigned
        departments = Department.objects.filter(id__in=department_ids)
        sections = Section.objects.filter(
            department__in=departments,
            year__in=years,
            semester__in=semesters
        )
        for section in sections:
            if section.courses.count() == 0:
                # Assign courses for the year, department, and semester to match section
                year_courses = Course.objects.filter(year=section.year, department=section.department, semester=section.semester)
                section.courses.set(year_courses)

        try:
            logger.info(f"Starting GA with department_ids={department_ids}, years={years}, semesters={semesters}")

            ga = GeneticAlgorithm(
                department_ids=department_ids,
                years=years,
                semesters=semesters,  # Pass list of semesters
                population_size=data.get('population_size', 100),
                mutation_rate=data.get('mutation_rate', 0.1),
                elite_rate=data.get('elite_rate', 0.1),
                generations=data.get('generations', 1000)
            )
            logger.info(f"GA initialized with {len(ga.all_classes)} classes")
            best_solution, fitness, fitness_progression = ga.evolve()
            logger.info(f"GA completed with fitness {fitness}, best_solution length: {len(best_solution) if best_solution else 0}")

            # Log details about generated classes for troubleshooting
            logger.info(f"Number of classes in best_solution: {len(best_solution) if best_solution else 0}")

            missing_assignments = 0
            if best_solution:
                for class_obj in best_solution:
                    keys = ('instructor', 'room', 'meeting_time', 'course', 'section')
                    if not all(k in class_obj and class_obj[k] is not None for k in keys):
                        missing_assignments += 1

            logger.info(f"Classes skipped due to missing assignments: {missing_assignments}")

            # naming metadata
            departments_qs = Department.objects.filter(id__in=department_ids)
            department_names = [d.name for d in departments_qs]
            year_names = [f"Year {y}" for y in sorted(years)]
            timetable_name = f"Combined Timetable - {', '.join(department_names)} - {', '.join(year_names)} - Semesters {semester_param} - {uuid.uuid4().hex[:8]}"

            primary_department = departments_qs.first()

            with transaction.atomic():
                timetable = Timetable.objects.create(
                    name=timetable_name,
                    department=primary_department,
                    year=min(years),
                    semester=semesters[0],  # Use the first semester for the record
                    fitness=fitness,
                    fitness_progression=fitness_progression,
                    created_by=request.user.username if request.user.is_authenticated else "admin"
                )

                if best_solution:
                    for class_data in best_solution:
                        keys = ('instructor', 'room', 'meeting_time', 'course', 'section')
                        if not all(k in class_data and class_data[k] is not None for k in keys):
                            continue

                        class_id = f"{class_data['id']}_{uuid.uuid4().hex[:4]}"
                        class_obj = Class.objects.create(
                            class_id=class_id,
                            course=class_data['course'],
                            instructor=class_data['instructor'],
                            meeting_time=class_data['meeting_time'],
                            room=class_data['room'],
                            section=class_data['section']
                        )
                        timetable.classes.add(class_obj)

                if fitness >= 80:
                    timetable.is_active = True
                    timetable.save()

            return Response({
                'message': 'Combined timetable generated successfully',
                'timetable_id': timetable.id,
                'fitness': fitness,
                'total_classes': len(best_solution) if best_solution else 0,
                'departments': department_names,
                'years': sorted(years),
                'semester': semester_param
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.exception("Timetable generation failed")
            return Response({'error': f'Failed to generate timetable: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # ----------------------------------------
    # View Timetable Schedule
    # ----------------------------------------
    @action(detail=True, methods=['get'])
    def view_schedule(self, request, pk=None):
        timetable = self.get_object()
        classes = timetable.classes.all().select_related('course', 'instructor', 'room', 'meeting_time', 'section')

        sections_data = {}

        for cls in classes:
            if not all([cls.section, cls.meeting_time, cls.course, cls.instructor, cls.room]):
                continue

            section_id = cls.section.section_id
            if section_id not in sections_data:
                sections_data[section_id] = {
                    'section_id': section_id,
                    'section_name': cls.section.section_id,
                    'schedule': {day: {} for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']},
                    'courses': {},
                    'instructors': {}
                }

            # Populate schedule
            day = cls.meeting_time.day
            duration_hours = getattr(cls.course, 'duration', 1)
            start_time = cls.meeting_time.start_time
            for i in range(duration_hours):
                slot_start = (datetime.datetime.combine(datetime.date.today(), start_time) + datetime.timedelta(hours=i)).time()
                slot_end = (datetime.datetime.combine(datetime.date.today(), slot_start) + datetime.timedelta(hours=1)).time()
                time_slot = f"{slot_start.strftime('%H:%M:%S')}-{slot_end.strftime('%H:%M:%S')}"
                is_start = (i == 0)

                schedule_for_section = sections_data[section_id]['schedule']
                schedule_for_section.setdefault(day, {})
                schedule_for_section[day].setdefault(time_slot, [])
                if not any(c['class_id'] == cls.class_id for c in schedule_for_section[day][time_slot]):
                    schedule_for_section[day][time_slot].append({
                        'class_id': cls.class_id, 'course': cls.course.course_name, 'course_id': cls.course.course_id,
                        'instructor': cls.instructor.name, 'room': cls.room.room_number, 'section': cls.section.section_id,
                        'course_type': cls.course.course_type, 'duration': duration_hours, 'is_start': is_start,
                        'colspan': duration_hours if is_start else 1
                    })

            # Populate courses and instructors
            course_key = cls.course.course_id
            instructor_obj = cls.instructor
            if course_key not in sections_data[section_id]['courses']:
                sections_data[section_id]['courses'][course_key] = {'course_code': cls.course.course_id, 'course_name': cls.course.course_name, 'instructors': set()}
            sections_data[section_id]['courses'][course_key]['instructors'].add(instructor_obj.name)

            if instructor_obj.id not in sections_data[section_id]['instructors']:
                sections_data[section_id]['instructors'][instructor_obj.id] = {'name': instructor_obj.name, 'email': instructor_obj.email, 'courses': set()}
            sections_data[section_id]['instructors'][instructor_obj.id]['courses'].add(cls.course.course_name)

        # Finalize data structure
        final_sections = []
        for section_id, data in sorted(sections_data.items()):
            courses_list = [{'course_code': c['course_code'], 'course_name': c['course_name'], 'instructors': sorted(list(c['instructors']))} for c in sorted(data['courses'].values(), key=lambda x: x['course_code'])]
            instructors_list = [{'name': i['name'], 'email': i['email'], 'courses': sorted(list(i['courses']))} for i in sorted(data['instructors'].values(), key=lambda x: x['name'])]
            
            data['courses'] = courses_list
            data['instructors'] = instructors_list
            final_sections.append(data)

        return Response({
            'timetable_name': timetable.name, 'fitness': timetable.fitness,
            'sections': final_sections, 'is_active': timetable.is_active, 'created_at': timetable.created_at
        })

    # ----------------------------------------
    # Export Functions
    # ----------------------------------------
    @action(detail=True, methods=['get'])
    def export_pdf(self, request, pk=None):
        timetable = self.get_object()
        pdf_content = export_timetable_pdf(timetable)
        response = HttpResponse(pdf_content, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{timetable.name}.pdf"'
        return response

    @action(detail=True, methods=['get'])
    def export_excel(self, request, pk=None):
        timetable = self.get_object()
        excel_content = export_timetable_excel(timetable)
        response = HttpResponse(
            excel_content,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename="{timetable.name}.xlsx"'
        return response

    # ----------------------------------------
    # Activate Timetable
    # ----------------------------------------
    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        timetable = self.get_object()

        # Determine semester parity
        if timetable.semester % 2 == 0:
            semesters_to_deactivate = [2, 4, 6, 8]
        else:
            semesters_to_deactivate = [1, 3, 5, 7]

        # Deactivate all other timetables for the same department, year, and semester parity
        Timetable.objects.filter(
            department=timetable.department,
            year=timetable.year,
            semester__in=semesters_to_deactivate
        ).update(is_active=False)

        # Activate the selected timetable
        timetable.is_active = True
        timetable.save()
        return Response({'message': 'Timetable activated successfully'})


# ----------------------------------------
# ✅ JWT /auth/user/ endpoint for frontend
# ----------------------------------------
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_user(request):
    user = request.user
    return Response({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'is_staff': user.is_staff,
    })
