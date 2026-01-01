from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from scheduler_app.models import Section, Department, Instructor, Course

class TestSectionInstructorAssignment(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.department = Department.objects.create(name="Test Dept", code="TD")
        self.instructor1 = Instructor.objects.create(
            instructor_id="I101",
            name="John Doe",
            email="john.doe@example.com"
        )
        self.instructor2 = Instructor.objects.create(
            instructor_id="I102",
            name="Jane Smith",
            email="jane.smith@example.com"
        )
        self.course1 = Course.objects.create(
            course_id="C101",
            course_name="Test Course 1",
            department=self.department,
            year=1,
            semester=1
        )
        self.course2 = Course.objects.create(
            course_id="C102",
            course_name="Test Course 2",
            department=self.department,
            year=1,
            semester=1
        )
        self.section = Section.objects.create(
            section_id="S101",
            department=self.department,
            year=1,
            semester=1,
            num_students=50
        )
        self.section.courses.set([self.course1, self.course2])

    def test_create_section_with_instructor_assignments(self):
        """Test creating a section with instructor assignments returns updated data"""
        url = reverse('section-list')
        payload = {
            "section_id": "S102",
            "department": self.department.id,
            "year": 1,
            "semester": 1,
            "num_students": 40,
            "course_instructor_assignments": {
                str(self.course1.id): [self.instructor1.id],
                str(self.course2.id): [self.instructor2.id]
            }
        }
        response = self.client.post(url, payload, format='json')
        assert response.status_code == 201
        data = response.json()

        # Check that the response includes the updated instructor assignments
        courses_detail = data.get('courses_detail', [])
        assert len(courses_detail) == 2

        # Find the courses in the response
        course1_detail = next((c for c in courses_detail if c['id'] == self.course1.id), None)
        course2_detail = next((c for c in courses_detail if c['id'] == self.course2.id), None)

        assert course1_detail is not None
        assert course2_detail is not None

        # Check instructor assignments
        assert len(course1_detail['instructors']) == 1
        assert course1_detail['instructors'][0]['id'] == self.instructor1.id
        assert course1_detail['instructors'][0]['name'] == self.instructor1.name

        assert len(course2_detail['instructors']) == 1
        assert course2_detail['instructors'][0]['id'] == self.instructor2.id
        assert course2_detail['instructors'][0]['name'] == self.instructor2.name

        # Verify in database
        self.course1.refresh_from_db()
        self.course2.refresh_from_db()
        assert list(self.course1.instructors.all()) == [self.instructor1]
        assert list(self.course2.instructors.all()) == [self.instructor2]

    def test_update_section_with_instructor_assignments(self):
        """Test updating a section with instructor assignments returns updated data"""
        url = reverse('section-detail', args=[self.section.id])
        payload = {
            "section_id": self.section.section_id,
            "department": self.department.id,
            "year": self.section.year,
            "semester": self.section.semester,
            "num_students": self.section.num_students,
            "course_instructor_assignments": {
                str(self.course1.id): [self.instructor1.id],
                str(self.course2.id): [self.instructor2.id]
            }
        }
        response = self.client.put(url, payload, format='json')
        assert response.status_code == 200
        data = response.json()

        # Check that the response includes the updated instructor assignments
        courses_detail = data.get('courses_detail', [])
        assert len(courses_detail) == 2

        # Find the courses in the response
        course1_detail = next((c for c in courses_detail if c['id'] == self.course1.id), None)
        course2_detail = next((c for c in courses_detail if c['id'] == self.course2.id), None)

        assert course1_detail is not None
        assert course2_detail is not None

        # Check instructor assignments
        assert len(course1_detail['instructors']) == 1
        assert course1_detail['instructors'][0]['id'] == self.instructor1.id
        assert course1_detail['instructors'][0]['name'] == self.instructor1.name

        assert len(course2_detail['instructors']) == 1
        assert course2_detail['instructors'][0]['id'] == self.instructor2.id
        assert course2_detail['instructors'][0]['name'] == self.instructor2.name

        # Verify in database
        self.course1.refresh_from_db()
        self.course2.refresh_from_db()
        assert list(self.course1.instructors.all()) == [self.instructor1]
        assert list(self.course2.instructors.all()) == [self.instructor2]

    def test_create_section_without_instructor_assignments(self):
        """Test creating a section without instructor assignments works normally"""
        url = reverse('section-list')
        payload = {
            "section_id": "S103",
            "department": self.department.id,
            "year": 1,
            "semester": 1,
            "num_students": 30
        }
        response = self.client.post(url, payload, format='json')
        assert response.status_code == 201
        data = response.json()

        # Check that courses_detail is present but instructors are empty
        courses_detail = data.get('courses_detail', [])
        assert len(courses_detail) == 0  # No courses assigned to this section

    def test_update_section_clear_instructor_assignments(self):
        """Test updating a section to clear instructor assignments"""
        # First assign instructors
        self.course1.instructors.set([self.instructor1])
        self.course2.instructors.set([self.instructor2])

        url = reverse('section-detail', args=[self.section.id])
        payload = {
            "section_id": self.section.section_id,
            "department": self.department.id,
            "year": self.section.year,
            "semester": self.section.semester,
            "num_students": self.section.num_students,
            "course_instructor_assignments": {
                str(self.course1.id): [],
                str(self.course2.id): []
            }
        }
        response = self.client.put(url, payload, format='json')
        assert response.status_code == 200
        data = response.json()

        # Check that the response shows cleared instructors
        courses_detail = data.get('courses_detail', [])
        assert len(courses_detail) == 2

        course1_detail = next((c for c in courses_detail if c['id'] == self.course1.id), None)
        course2_detail = next((c for c in courses_detail if c['id'] == self.course2.id), None)

        assert len(course1_detail['instructors']) == 0
        assert len(course2_detail['instructors']) == 0

        # Verify in database
        self.course1.refresh_from_db()
        self.course2.refresh_from_db()
        assert list(self.course1.instructors.all()) == []
        assert list(self.course2.instructors.all()) == []

    def test_create_section_with_multiple_instructors_per_course(self):
        """Test assigning multiple instructors to a single course"""
        url = reverse('section-list')
        payload = {
            "section_id": "S104",
            "department": self.department.id,
            "year": 1,
            "semester": 1,
            "num_students": 45,
            "course_instructor_assignments": {
                str(self.course1.id): [self.instructor1.id, self.instructor2.id]
            }
        }
        response = self.client.post(url, payload, format='json')
        assert response.status_code == 201
        data = response.json()

        # Check that the response includes both instructors
        courses_detail = data.get('courses_detail', [])
        course1_detail = next((c for c in courses_detail if c['id'] == self.course1.id), None)
        assert course1_detail is not None
        assert len(course1_detail['instructors']) == 2

        instructor_ids = [i['id'] for i in course1_detail['instructors']]
        assert self.instructor1.id in instructor_ids
        assert self.instructor2.id in instructor_ids

        # Verify in database
        self.course1.refresh_from_db()
        instructors = list(self.course1.instructors.all())
        assert len(instructors) == 2
        assert self.instructor1 in instructors
        assert self.instructor2 in instructors
