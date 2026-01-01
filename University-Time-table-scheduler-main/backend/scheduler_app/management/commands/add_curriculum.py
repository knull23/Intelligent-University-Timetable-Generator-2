from django.core.management.base import BaseCommand
from scheduler_app.models import Department, Course, Section
import json

class Command(BaseCommand):
    help = 'Add curriculum data to the database'

    def handle(self, *args, **kwargs):
        # Curriculum data
        curriculum_data = [
            {
                "program": "Data Science",
                "source_file": "syllabus ds.pdf",
                "curriculum": [
                    { "semester": 1, "course_code": "MAL101", "course_name": "Engineering Mathematics", "credits": 4, "type": "Theory", "hours_per_week": 4 },
                    { "semester": 1, "course_code": "SAP102", "course_name": "Health, Sports & Proficiency", "credits": 2, "type": "Theory", "hours_per_week": 2 },
                    { "semester": 1, "course_code": "BEL103", "course_name": "Fundamentals of Electrical Engineering", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 1, "course_code": "BSL104", "course_name": "Applied Sciences", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 1, "course_code": "UCS001", "course_name": "Computer Programming", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 1, "course_code": "ECL106", "course_name": "Analog Electronics", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 1, "course_code": "HUL107", "course_name": "Environmental Studies", "credits": 2, "type": "Theory", "hours_per_week": 2 },
                    { "semester": 1, "course_code": "BEL108", "course_name": "Fundamentals of Electrical Engineering Lab", "credits": 1, "type": "Lab", "hours_per_week": 2 },
                    { "semester": 1, "course_code": "BSL109", "course_name": "Applied Sciences Lab", "credits": 1, "type": "Lab", "hours_per_week": 2 },
                    { "semester": 1, "course_code": "UCS051", "course_name": "Computer Programming Lab", "credits": 1, "type": "Lab", "hours_per_week": 2 },
                    { "semester": 1, "course_code": "ECL111", "course_name": "Analog Electronics Lab", "credits": 1, "type": "Lab", "hours_per_week": 2 },
                    { "semester": 2, "course_code": "MAL201", "course_name": "Engineering Mathematics II", "credits": 4, "type": "Theory", "hours_per_week": 4 },
                    { "semester": 2, "course_code": "ECL202", "course_name": "Digital Electronics", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 2, "course_code": "UCS002", "course_name": "Data Structures", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 2, "course_code": "HUL204", "course_name": "Communication Skills", "credits": 2, "type": "Theory", "hours_per_week": 2 },
                    { "semester": 2, "course_code": "UCS003", "course_name": "Web Designing", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 2, "course_code": "UCS004", "course_name": "Object Oriented Programming", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 2, "course_code": "ECL207", "course_name": "Digital Electronics Lab", "credits": 1, "type": "Lab", "hours_per_week": 2 },
                    { "semester": 2, "course_code": "UCS052", "course_name": "Data Structures Lab", "credits": 1, "type": "Lab", "hours_per_week": 2 },
                    { "semester": 2, "course_code": "HUL209", "course_name": "Communication Skills Lab", "credits": 1, "type": "Lab", "hours_per_week": 2 },
                    { "semester": 2, "course_code": "UCS053", "course_name": "Web Designing Lab", "credits": 1, "type": "Lab", "hours_per_week": 2 },
                    { "semester": 2, "course_code": "UCS054", "course_name": "Object Oriented Programming Lab", "credits": 1, "type": "Lab", "hours_per_week": 2 },
                    { "semester": 3, "course_code": "UCS005", "course_name": "Discrete Mathematics", "credits": 4, "type": "Theory", "hours_per_week": 4 },
                    { "semester": 3, "course_code": "UCS006", "course_name": "Design and Analysis of Algorithms", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 3, "course_code": "UCS007", "course_name": "Computer Organization", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 3, "course_code": "UCS008", "course_name": "Object Oriented Programming II", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 3, "course_code": "UCS009", "course_name": "Automata and Formal Languages", "credits": 4, "type": "Theory", "hours_per_week": 4 },
                    { "semester": 3, "course_code": "UCS010", "course_name": "Database Management Systems", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 3, "course_code": "UCS056", "course_name": "Design and Analysis of Algorithms Lab", "credits": 1, "type": "Lab", "hours_per_week": 2 },
                    { "semester": 3, "course_code": "UCS057", "course_name": "Computer Organization Lab", "credits": 1, "type": "Lab", "hours_per_week": 2 },
                    { "semester": 3, "course_code": "UCS058", "course_name": "Object Oriented Programming II Lab", "credits": 1, "type": "Lab", "hours_per_week": 2 },
                    { "semester": 3, "course_code": "UCS060", "course_name": "Database Management Systems Lab", "credits": 1, "type": "Lab", "hours_per_week": 2 },
                    { "semester": 4, "course_code": "UCS011", "course_name": "Software Engineering", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 4, "course_code": "UCS012", "course_name": "Probability and Statistics", "credits": 4, "type": "Theory", "hours_per_week": 4 },
                    { "semester": 4, "course_code": "UCS013", "course_name": "Operating Systems", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 4, "course_code": "UCS014", "course_name": "Computer Networks", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 4, "course_code": "UCS015", "course_name": "Microprocessor and Assembly", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 4, "course_code": "UCS016", "course_name": "Compiler Design", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 4, "course_code": "UCS061", "course_name": "Software Engineering Lab", "credits": 1, "type": "Lab", "hours_per_week": 2 },
                    { "semester": 4, "course_code": "UCS063", "course_name": "Operating Systems Lab", "credits": 1, "type": "Lab", "hours_per_week": 2 },
                    { "semester": 4, "course_code": "UCS064", "course_name": "Computer Networks Lab", "credits": 1, "type": "Lab", "hours_per_week": 2 },
                    { "semester": 4, "course_code": "UCS065", "course_name": "Microprocessor Lab", "credits": 1, "type": "Lab", "hours_per_week": 2 },
                    { "semester": 4, "course_code": "UCS066", "course_name": "Compiler Design Lab", "credits": 1, "type": "Lab", "hours_per_week": 2 },
                    { "semester": 5, "course_code": "UDS001", "course_name": "Data Mining and Warehousing", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 5, "course_code": "UDS002", "course_name": "Introduction to Cryptography", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 5, "course_code": "UCS019", "course_name": "Mathematics for Machine Learning", "credits": 4, "type": "Theory", "hours_per_week": 4 },
                    { "semester": 5, "course_code": "XXXXX", "course_name": "Elective-V-I", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 5, "course_code": "UCS020", "course_name": "Professional Conduct", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 5, "course_code": "UCS021", "course_name": "Machine Learning", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 5, "course_code": "UDS051", "course_name": "Data Mining Lab", "credits": 1, "type": "Lab", "hours_per_week": 2 },
                    { "semester": 5, "course_code": "UDS052", "course_name": "Introduction to Cryptography Lab", "credits": 1, "type": "Lab", "hours_per_week": 2 },
                    { "semester": 5, "course_code": "UCS071", "course_name": "Machine Learning Lab", "credits": 1, "type": "Lab", "hours_per_week": 2 },
                    { "semester": 5, "course_code": "UCS201", "course_name": "Summer Internship", "credits": 0, "type": "Lab", "hours_per_week": 0 },
                    { "semester": 5, "course_code": "XXXXX", "course_name": "Elective-V-I Lab", "credits": 1, "type": "Lab", "hours_per_week": 2 },
                    { "semester": 6, "course_code": "UCS022", "course_name": "Artificial Intelligence", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 6, "course_code": "XXXXX", "course_name": "Management Elective", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 6, "course_code": "UDS004", "course_name": "Big Data Analytics", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 6, "course_code": "XXXXX", "course_name": "Elective VI-1", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 6, "course_code": "UCS023", "course_name": "Distributed Databases", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 6, "course_code": "UCS072", "course_name": "Artificial Intelligence Lab", "credits": 1, "type": "Lab", "hours_per_week": 2 },
                    { "semester": 6, "course_code": "UDS054", "course_name": "Big Data Analytics Lab", "credits": 1, "type": "Lab", "hours_per_week": 2 },
                    { "semester": 6, "course_code": "XXXXX", "course_name": "Elective VI-I Lab", "credits": 1, "type": "Lab", "hours_per_week": 2 },
                    { "semester": 6, "course_code": "UCS202", "course_name": "Minor Project-I", "credits": 2, "type": "Lab", "hours_per_week": 2 },
                    { "semester": 7, "course_code": "UCS205", "course_name": "Major Project", "credits": 5, "type": "Lab", "hours_per_week": 2 },
                    { "semester": 7, "course_code": "XXXXX", "course_name": "Elective I", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 7, "course_code": "XXXXX", "course_name": "Elective II", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 7, "course_code": "XXXXX", "course_name": "Elective III", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 7, "course_code": "UDS004", "course_name": "Advanced Data Analytics", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 7, "course_code": "UDS005", "course_name": "Advanced Deep Learning", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 7, "course_code": "UDS054", "course_name": "Advanced Data Analytics Lab", "credits": 1, "type": "Lab", "hours_per_week": 2 },
                    { "semester": 8, "course_code": "UCS206", "course_name": "Major Project", "credits": 5, "type": "Lab", "hours_per_week": 2 },
                    { "semester": 8, "course_code": "XXXXX", "course_name": "Elective I", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 8, "course_code": "XXXXX", "course_name": "Elective II", "credits": 4, "type": "Theory", "hours_per_week": 4 },
                    { "semester": 8, "course_code": "XXXXX", "course_name": "Elective III", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 8, "course_code": "UCS024", "course_name": "Data Analytics & Visualization", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 8, "course_code": "UDS005", "course_name": "Advanced Deep Learning", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 8, "course_code": "UCS074", "course_name": "Data Analytics & Visualization Lab", "credits": 1, "type": "Lab", "hours_per_week": 2 }
                ]
            },
            {
                "program": "Computer Science Engineering",
                "source_file": "syllabus cse.pdf",
                "curriculum": [
                    { "semester": 1, "course_code": "MAL101", "course_name": "Engineering Mathematics", "credits": 4, "type": "Theory", "hours_per_week": 4 },
                    { "semester": 1, "course_code": "SAP102", "course_name": "Health, Sports & Proficiency", "credits": 2, "type": "Theory", "hours_per_week": 2 },
                    { "semester": 1, "course_code": "BEL103", "course_name": "Fundamentals of Electrical Engineering", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 1, "course_code": "BSL104", "course_name": "Applied Sciences", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 1, "course_code": "UCS001", "course_name": "Computer Programming", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 1, "course_code": "ECL106", "course_name": "Analog Electronics", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 1, "course_code": "HUL107", "course_name": "Environmental Studies", "credits": 2, "type": "Theory", "hours_per_week": 2 },
                    { "semester": 1, "course_code": "BEL108", "course_name": "Fundamentals of Electrical Engineering Lab", "credits": 1, "type": "Lab", "hours_per_week": 2 },
                    { "semester": 1, "course_code": "BSL109", "course_name": "Applied Sciences Lab", "credits": 1, "type": "Lab", "hours_per_week": 2 },
                    { "semester": 1, "course_code": "UCS051", "course_name": "Computer Programming Lab", "credits": 1, "type": "Lab", "hours_per_week": 2 },
                    { "semester": 1, "course_code": "ECL111", "course_name": "Analog Electronics Lab", "credits": 1, "type": "Lab", "hours_per_week": 2 },
                    { "semester": 2, "course_code": "MAL201", "course_name": "Engineering Mathematics II", "credits": 4, "type": "Theory", "hours_per_week": 4 },
                    { "semester": 2, "course_code": "ECL202", "course_name": "Digital Electronics", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 2, "course_code": "UCS002", "course_name": "Data Structures", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 2, "course_code": "HUL204", "course_name": "Communication Skills", "credits": 2, "type": "Theory", "hours_per_week": 2 },
                    { "semester": 2, "course_code": "UCS003", "course_name": "Web Designing", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 2, "course_code": "UCS004", "course_name": "Object Oriented Programming", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 2, "course_code": "ECL207", "course_name": "Digital Electronics Lab", "credits": 1, "type": "Lab", "hours_per_week": 2 },
                    { "semester": 2, "course_code": "UCS052", "course_name": "Data Structures Lab", "credits": 1, "type": "Lab", "hours_per_week": 2 },
                    { "semester": 2, "course_code": "HUL209", "course_name": "Communication Skills Lab", "credits": 1, "type": "Lab", "hours_per_week": 2 },
                    { "semester": 2, "course_code": "UCS053", "course_name": "Web Designing Lab", "credits": 1, "type": "Lab", "hours_per_week": 2 },
                    { "semester": 2, "course_code": "UCS054", "course_name": "Object Oriented Programming Lab", "credits": 1, "type": "Lab", "hours_per_week": 2 },
                    { "semester": 3, "course_code": "UCS005", "course_name": "Discrete Mathematics", "credits": 4, "type": "Theory", "hours_per_week": 4 },
                    { "semester": 3, "course_code": "UCS006", "course_name": "Design and Analysis of Algorithms", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 3, "course_code": "UCS007", "course_name": "Computer Organization", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 3, "course_code": "UCS008", "course_name": "Object Oriented Programming II", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 3, "course_code": "UCS009", "course_name": "Automata and Formal Languages", "credits": 4, "type": "Theory", "hours_per_week": 4 },
                    { "semester": 3, "course_code": "UCS010", "course_name": "Database Management Systems", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 3, "course_code": "UCS056", "course_name": "Design and Analysis of Algorithms Lab", "credits": 1, "type": "Lab", "hours_per_week": 2 },
                    { "semester": 3, "course_code": "UCS057", "course_name": "Computer Organization Lab", "credits": 1, "type": "Lab", "hours_per_week": 2 },
                    { "semester": 3, "course_code": "UCS058", "course_name": "Object Oriented Programming Lab II", "credits": 1, "type": "Lab", "hours_per_week": 2 },
                    { "semester": 3, "course_code": "UCS060", "course_name": "Database Management Systems Lab", "credits": 1, "type": "Lab", "hours_per_week": 2 },
                    { "semester": 4, "course_code": "UCS011", "course_name": "Software Engineering", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 4, "course_code": "UCS012", "course_name": "Probability and Statistics", "credits": 4, "type": "Theory", "hours_per_week": 4 },
                    { "semester": 4, "course_code": "UCS013", "course_name": "Operating Systems", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 4, "course_code": "UCS014", "course_name": "Computer Networks", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 4, "course_code": "UCS015", "course_name": "Microprocessor and Assembly", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 4, "course_code": "UCS016", "course_name": "Compiler Design", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 4, "course_code": "UCS061", "course_name": "Software Engineering Lab", "credits": 1, "type": "Lab", "hours_per_week": 2 },
                    { "semester": 4, "course_code": "UCS063", "course_name": "Operating Systems Lab", "credits": 1, "type": "Lab", "hours_per_week": 2 },
                    { "semester": 4, "course_code": "UCS064", "course_name": "Computer Networks Lab", "credits": 1, "type": "Lab", "hours_per_week": 2 },
                    { "semester": 4, "course_code": "UCS065", "course_name": "Microprocessor Lab", "credits": 1, "type": "Lab", "hours_per_week": 2 },
                    { "semester": 4, "course_code": "UCS066", "course_name": "Compiler Design Lab", "credits": 1, "type": "Lab", "hours_per_week": 2 },
                    { "semester": 5, "course_code": "UCS017", "course_name": "Enterprise Java", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 5, "course_code": "UCS018", "course_name": "Information Security", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 5, "course_code": "UCS019", "course_name": "Mathematics for Machine Learning", "credits": 4, "type": "Theory", "hours_per_week": 4 },
                    { "semester": 5, "course_code": "XXXXX", "course_name": "Elective-V-I", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 5, "course_code": "UCS020", "course_name": "Professional Conduct", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 5, "course_code": "UCS021", "course_name": "Machine Learning", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 5, "course_code": "UCS067", "course_name": "Enterprise Java Lab", "credits": 1, "type": "Lab", "hours_per_week": 2 },
                    { "semester": 5, "course_code": "UCS068", "course_name": "Information Security Lab", "credits": 1, "type": "Lab", "hours_per_week": 2 },
                    { "semester": 5, "course_code": "UCS071", "course_name": "Machine Learning Lab", "credits": 1, "type": "Lab", "hours_per_week": 2 },
                    { "semester": 5, "course_code": "XXXXX", "course_name": "Elective-V-I Lab", "credits": 1, "type": "Lab", "hours_per_week": 2 },
                    { "semester": 6, "course_code": "UCS022", "course_name": "Artificial Intelligence", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 6, "course_code": "XXXXX", "course_name": "Management Elective", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 6, "course_code": "XXXXX", "course_name": "Elective II", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 6, "course_code": "XXXXX", "course_name": "Elective III", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 6, "course_code": "UCS023", "course_name": "Distributed Databases", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 6, "course_code": "UCS072", "course_name": "Artificial Intelligence Lab", "credits": 1, "type": "Lab", "hours_per_week": 2 },
                    { "semester": 6, "course_code": "XXXXX", "course_name": "Elective II Lab", "credits": 1, "type": "Lab", "hours_per_week": 2 },
                    { "semester": 6, "course_code": "XXXXX", "course_name": "Elective III Lab", "credits": 1, "type": "Lab", "hours_per_week": 2 },
                    { "semester": 6, "course_code": "UCS202", "course_name": "Minor Project-I", "credits": 2, "type": "Lab", "hours_per_week": 2 },
                    { "semester": 7, "course_code": "UCS205", "course_name": "Major Project", "credits": 5, "type": "Lab", "hours_per_week": 2 },
                    { "semester": 7, "course_code": "XXXXX", "course_name": "Elective I", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 7, "course_code": "XXXXX", "course_name": "Elective II", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 7, "course_code": "XXXXX", "course_name": "Elective III", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 7, "course_code": "UCS024", "course_name": "Data Analytics & Visualization", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 7, "course_code": "XXXXX", "course_name": "Elective IV", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 7, "course_code": "UCS074", "course_name": "Data Analytics & Visualization Lab", "credits": 1, "type": "Lab", "hours_per_week": 2 },
                    { "semester": 8, "course_code": "UCS206", "course_name": "Major Project", "credits": 5, "type": "Lab", "hours_per_week": 2 },
                    { "semester": 8, "course_code": "XXXXX", "course_name": "Elective I", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 8, "course_code": "XXXXX", "course_name": "Elective II", "credits": 4, "type": "Theory", "hours_per_week": 4 },
                    { "semester": 8, "course_code": "XXXXX", "course_name": "Elective III", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 8, "course_code": "UCS024", "course_name": "Data Analytics & Visualization", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 8, "course_code": "XXXXX", "course_name": "Elective IV", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 8, "course_code": "UCS074", "course_name": "Data Analytics & Visualization Lab", "credits": 1, "type": "Lab", "hours_per_week": 2 }
                ]
            },
            {
                "program": "Information Technology",
                "source_file": "syllabus it.pdf",
                "curriculum": [
                    { "semester": 1, "course_code": "MAL101", "course_name": "Engineering Mathematics", "credits": 4, "type": "Theory", "hours_per_week": 4 },
                    { "semester": 1, "course_code": "SAP102", "course_name": "Health, Sports & Proficiency", "credits": 2, "type": "Theory", "hours_per_week": 2 },
                    { "semester": 1, "course_code": "BEL103", "course_name": "Fundamentals of Electrical Engineering", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 1, "course_code": "BSL104", "course_name": "Applied Sciences", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 1, "course_code": "UCS001", "course_name": "Computer Programming", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 1, "course_code": "ECL106", "course_name": "Analog Electronics", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 1, "course_code": "HUL107", "course_name": "Environmental Studies", "credits": 2, "type": "Theory", "hours_per_week": 2 },
                    { "semester": 1, "course_code": "BEL108", "course_name": "Fundamentals of Electrical Engineering Lab", "credits": 1, "type": "Lab", "hours_per_week": 2 },
                    { "semester": 1, "course_code": "BSL109", "course_name": "Applied Sciences Lab", "credits": 1, "type": "Lab", "hours_per_week": 2 },
                    { "semester": 1, "course_code": "UCS051", "course_name": "Computer Programming Lab", "credits": 1, "type": "Lab", "hours_per_week": 2 },
                    { "semester": 1, "course_code": "ECL111", "course_name": "Analog Electronics Lab", "credits": 1, "type": "Lab", "hours_per_week": 2 },
                    { "semester": 2, "course_code": "MAL201", "course_name": "Engineering Mathematics II", "credits": 4, "type": "Theory", "hours_per_week": 4 },
                    { "semester": 2, "course_code": "ECL202", "course_name": "Digital Electronics", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 2, "course_code": "UCS002", "course_name": "Data Structures", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 2, "course_code": "HUL204", "course_name": "Communication Skills", "credits": 2, "type": "Theory", "hours_per_week": 2 },
                    { "semester": 2, "course_code": "UCS003", "course_name": "Web Designing", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 2, "course_code": "UCS004", "course_name": "Object Oriented Programming", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 2, "course_code": "ECL207", "course_name": "Digital Electronics Lab", "credits": 1, "type": "Lab", "hours_per_week": 2 },
                    { "semester": 2, "course_code": "UCS052", "course_name": "Data Structures Lab", "credits": 1, "type": "Lab", "hours_per_week": 2 },
                    { "semester": 2, "course_code": "HUL209", "course_name": "Communication Skills Lab", "credits": 1, "type": "Lab", "hours_per_week": 2 },
                    { "semester": 2, "course_code": "UCS053", "course_name": "Web Designing Lab", "credits": 1, "type": "Lab", "hours_per_week": 2 },
                    { "semester": 2, "course_code": "UCS054", "course_name": "Object Oriented Programming Lab", "credits": 1, "type": "Lab", "hours_per_week": 2 },
                    { "semester": 3, "course_code": "UCS005", "course_name": "Discrete Mathematics", "credits": 4, "type": "Theory", "hours_per_week": 4 },
                    { "semester": 3, "course_code": "UCS006", "course_name": "Design and Analysis of Algorithms", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 3, "course_code": "UCS007", "course_name": "Computer Organization", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 3, "course_code": "UCS008", "course_name": "Object Oriented Programming II", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 3, "course_code": "UCS009", "course_name": "Automata and Formal Languages", "credits": 4, "type": "Theory", "hours_per_week": 4 },
                    { "semester": 3, "course_code": "UCS010", "course_name": "Database Management Systems", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 3, "course_code": "UCS056", "course_name": "Design and Analysis of Algorithms Lab", "credits": 1, "type": "Lab", "hours_per_week": 2 },
                    { "semester": 3, "course_code": "UCS057", "course_name": "Computer Organization Lab", "credits": 1, "type": "Lab", "hours_per_week": 2 },
                    { "semester": 3, "course_code": "UCS058", "course_name": "Object Oriented Programming Lab II", "credits": 1, "type": "Lab", "hours_per_week": 2 },
                    { "semester": 3, "course_code": "UCS060", "course_name": "Database Management Systems Lab", "credits": 1, "type": "Lab", "hours_per_week": 2 },
                    { "semester": 4, "course_code": "UCS011", "course_name": "Software Engineering", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 4, "course_code": "UCS012", "course_name": "Probability and Statistics", "credits": 4, "type": "Theory", "hours_per_week": 4 },
                    { "semester": 4, "course_code": "UCS013", "course_name": "Operating Systems", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 4, "course_code": "UCS014", "course_name": "Computer Networks", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 4, "course_code": "UCS015", "course_name": "Microprocessor and Assembly", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 4, "course_code": "UCS016", "course_name": "Compiler Design", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 4, "course_code": "UCS061", "course_name": "Software Engineering Lab", "credits": 1, "type": "Lab", "hours_per_week": 2 },
                    { "semester": 4, "course_code": "UCS063", "course_name": "Operating Systems Lab", "credits": 1, "type": "Lab", "hours_per_week": 2 },
                    { "semester": 4, "course_code": "UCS064", "course_name": "Computer Networks Lab", "credits": 1, "type": "Lab", "hours_per_week": 2 },
                    { "semester": 4, "course_code": "UCS065", "course_name": "Microprocessor Lab", "credits": 1, "type": "Lab", "hours_per_week": 2 },
                    { "semester": 4, "course_code": "UCS066", "course_name": "Compiler Design Lab", "credits": 1, "type": "Lab", "hours_per_week": 2 },
                    { "semester": 5, "course_code": "UCS017", "course_name": "Enterprise Java", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 5, "course_code": "UCS018", "course_name": "Information Security", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 5, "course_code": "UCS019", "course_name": "Mathematics for Machine Learning", "credits": 4, "type": "Theory", "hours_per_week": 4 },
                    { "semester": 5, "course_code": "XXXXX", "course_name": "Elective-V-I", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 5, "course_code": "UCS020", "course_name": "Professional Conduct", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 5, "course_code": "UCS021", "course_name": "Machine Learning", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 5, "course_code": "UCS067", "course_name": "Enterprise Java Lab", "credits": 1, "type": "Lab", "hours_per_week": 2 },
                    { "semester": 5, "course_code": "UCS068", "course_name": "Information Security Lab", "credits": 1, "type": "Lab", "hours_per_week": 2 },
                    { "semester": 5, "course_code": "UCS071", "course_name": "Machine Learning Lab", "credits": 1, "type": "Lab", "hours_per_week": 2 },
                    { "semester": 5, "course_code": "XXXXX", "course_name": "Elective-V-I Lab", "credits": 1, "type": "Lab", "hours_per_week": 2 },
                    { "semester": 6, "course_code": "UCS022", "course_name": "Artificial Intelligence", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 6, "course_code": "XXXXX", "course_name": "Management Elective", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 6, "course_code": "XXXXX", "course_name": "Elective II", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 6, "course_code": "XXXXX", "course_name": "Elective III", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 6, "course_code": "UCS023", "course_name": "Distributed Databases", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 6, "course_code": "UCS072", "course_name": "Artificial Intelligence Lab", "credits": 1, "type": "Lab", "hours_per_week": 2 },
                    { "semester": 6, "course_code": "XXXXX", "course_name": "Elective II Lab", "credits": 1, "type": "Lab", "hours_per_week": 2 },
                    { "semester": 6, "course_code": "XXXXX", "course_name": "Elective III Lab", "credits": 1, "type": "Lab", "hours_per_week": 2 },
                    { "semester": 6, "course_code": "UCS202", "course_name": "Minor Project-I", "credits": 2, "type": "Lab", "hours_per_week": 2 },
                    { "semester": 7, "course_code": "UCS205", "course_name": "Major Project", "credits": 5, "type": "Lab", "hours_per_week": 2 },
                    { "semester": 7, "course_code": "XXXXX", "course_name": "Elective I", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 7, "course_code": "XXXXX", "course_name": "Elective II", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 7, "course_code": "XXXXX", "course_name": "Elective III", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 7, "course_code": "UCS024", "course_name": "Data Analytics & Visualization", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 7, "course_code": "XXXXX", "course_name": "Elective IV", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 7, "course_code": "UCS074", "course_name": "Data Analytics & Visualization Lab", "credits": 1, "type": "Lab", "hours_per_week": 2 },
                    { "semester": 8, "course_code": "UCS206", "course_name": "Major Project", "credits": 5, "type": "Lab", "hours_per_week": 2 },
                    { "semester": 8, "course_code": "XXXXX", "course_name": "Elective I", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 8, "course_code": "XXXXX", "course_name": "Elective II", "credits": 4, "type": "Theory", "hours_per_week": 4 },
                    { "semester": 8, "course_code": "XXXXX", "course_name": "Elective III", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 8, "course_code": "UCS024", "course_name": "Data Analytics & Visualization", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 8, "course_code": "XXXXX", "course_name": "Elective IV", "credits": 3, "type": "Theory", "hours_per_week": 3 },
                    { "semester": 8, "course_code": "UCS074", "course_name": "Data Analytics & Visualization Lab", "credits": 1, "type": "Lab", "hours_per_week": 2 }
                ]
            }
        ]

        # Create departments
        departments = {}
        for program_data in curriculum_data:
            program = program_data['program']
            code = program.replace(' ', '').upper()[:3]  # e.g., DAT for Data Science, COM for Computer Science Engineering, INF for Information Technology
            if program == "Data Science":
                code = "DS"
            elif program == "Computer Science Engineering":
                code = "CSE"
            elif program == "Information Technology":
                code = "IT"
            dept, created = Department.objects.get_or_create(
                code=code,
                defaults={'name': program}
            )
            departments[program] = dept
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created department: {dept}"))
            else:
                self.stdout.write(f"Department {dept} already exists.")

        # Create courses
        added_courses = 0
        for program_data in curriculum_data:
            program = program_data['program']
            dept = departments[program]
            for course_data in program_data['curriculum']:
                semester = course_data['semester']
                year = (semester + 1) // 2
                sem = semester % 2
                if sem == 0:
                    sem = 2
                duration = 1 if course_data['type'] == 'Theory' else 2
                # Set max_students based on department
                if dept.code == 'DS':
                    max_students = 60
                elif dept.code == 'IT':
                    max_students = 60
                elif dept.code == 'CSE':
                    max_students = 120
                else:
                    max_students = 120  # default

                course, created = Course.objects.get_or_create(
                    course_id=course_data['course_code'],
                    department=dept,
                    defaults={
                        'course_name': course_data['course_name'],
                        'course_type': course_data['type'],
                        'credits': course_data['credits'],
                        'max_students': max_students,
                        'duration': duration,
                        'year': year,
                        'semester': course_data['semester'],
                        'classes_per_week': course_data['credits']
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Added course: {course}"))
                    added_courses += 1
                else:
                    # Update max_students and semester for existing courses
                    updated = False
                    if course.max_students != max_students:
                        course.max_students = max_students
                        updated = True
                    if course.semester != course_data['semester']:
                        course.semester = course_data['semester']
                        updated = True
                    if updated:
                        course.save()
                        self.stdout.write(f"Updated course: {course}")
                    else:
                        self.stdout.write(f"Course {course} already exists.")

        self.stdout.write(self.style.SUCCESS(f"Total courses added: {added_courses}"))

        # Create sections
        added_sections = 0
        for dept in Department.objects.all():
            for year in range(1, 5):
                # Determine num_students based on department
                if dept.code == 'DS':
                    num_students = 30
                elif dept.code == 'IT':
                    num_students = 30
                elif dept.code == 'CSE':
                    num_students = 60
                else:
                    num_students = 60  # default

                for section_letter in ['A', 'B']:
                    section_id = f"{dept.code}-{year}{section_letter}"
                    for i in range(2):
                        sem = year * 2 - 1 + i
                        section, created = Section.objects.get_or_create(
                            section_id=section_id,
                            department=dept,
                            year=year,
                            semester=sem,
                            defaults={'num_students': num_students}
                        )
                        if created:
                            self.stdout.write(self.style.SUCCESS(f"Added section: {section}"))
                            added_sections += 1
                        else:
                            self.stdout.write(f"Section {section} already exists.")
        
        self.stdout.write(self.style.SUCCESS(f"Total sections added: {added_sections}"))