from datetime import date
from typing import List
from sqlmodel import Session, select
from app.models import (
    create_db_and_models,
    Subject,
    Difficulty,
    Organization,
    Grade,
    Course,
    CourseSubjectLink,
    CourseGradeLink,
    engine,
)


def create_subjects(session: Session) -> List[Subject]:
    """Create mock subjects and return them."""
    subjects_data = [
        {
            'id': 1,
            'type': 'ai',
            'label': 'ИИ',
            'icon': '<path d="M19.8 18.4 L14 10.67V6.5l1.35-1.69c.26-.33.03-.81-.39-.81H9.04c-.42 0-.65.48-.39.81L10 6.5v4.17L4.2 18.4c-.49.66-.02 1.6.8 1.6h14c.82 0 1.29-.94.8-1.6"></path>',
            'color': '#4caf50',
            'additional_description': [
                'Программа сочетает теоретическую подготовку с практическими экспериментами и исследованиями.',
                'Участники работают с современным научным оборудованием под руководством ученых-практиков.',
            ],
        },
        {
            'id': 2,
            'type': 'math',
            'label': 'Математика',
            'icon': '<path d="M12 4L4 20h8l4-8z"></path>',
            'color': '#2196f3',
            'additional_description': [
                'Курс охватывает основы алгебры и геометрии.',
                'Практические задания для развития аналитического мышления.',
            ],
        },
    ]
    subjects = []
    for data in subjects_data:
        # Check if subject already exists
        existing = session.exec(select(Subject).where(Subject.id == data['id'])).first()
        if not existing:
            subject = Subject(**data)
            session.add(subject)
            subjects.append(subject)
    session.commit()
    return subjects


def create_difficulties(session: Session) -> List[Difficulty]:
    """Create mock difficulties and return them."""
    difficulties_data = [
        {
            'id': 1,
            'type': 'intermediate',
            'label': 'Средний',
            'icon': '<path d="M13 8.57c-.79 0-1.43.64-1.43 1.43s.64 1.43 1.43 1.43 1.43-.64 1.43-1.43-.64-1.43-1.43-1.43"></path>',
            'color': '#f44336',
        },
        {
            'id': 2,
            'type': 'beginner',
            'label': 'Начальный',
            'icon': '<path d="M12 2L2 12h10l10-10z"></path>',
            'color': '#4caf50',
        },
    ]
    difficulties = []
    for data in difficulties_data:
        existing = session.exec(select(Difficulty).where(Difficulty.id == data['id'])).first()
        if not existing:
            difficulty = Difficulty(**data)
            session.add(difficulty)
            difficulties.append(difficulty)
    session.commit()
    return difficulties


def create_organizations(session: Session) -> List[Organization]:
    """Create mock organizations and return them."""
    organizations_data = [{'id': 1, 'name': 'Яндекс'}, {'id': 2, 'name': 'Coursera'}]
    organizations = []
    for data in organizations_data:
        existing = session.exec(select(Organization).where(Organization.id == data['id'])).first()
        if not existing:
            org = Organization(**data)
            session.add(org)
            organizations.append(org)
    session.commit()
    return organizations


def create_grades(session: Session) -> List[Grade]:
    """Create mock grades and return them."""
    grades_data = [{'id': 10, 'grade': 10}, {'id': 11, 'grade': 11}, {'id': 12, 'grade': 12}]
    grades = []
    for data in grades_data:
        existing = session.exec(select(Grade).where(Grade.id == data['id'])).first()
        if not existing:
            grade = Grade(**data)
            session.add(grade)
            grades.append(grade)
    session.commit()
    return grades


def create_courses(session: Session) -> List[Course]:
    """Create mock courses with relationships and return them."""
    courses_data = [
        {
            'id': 1,
            'title': 'Основы машинного обучения и нейронных сетей',
            'description': 'Ведут специалисты из Яндекса с реальными кейсами из индустрии.',
            'start_date': date(2025, 9, 15),
            'end_date': date(2026, 1, 20),
            'url': 'https://practicum.yandex.ru/',
            'organization_id': 1,
            'difficulty_id': 1,
            'subject_ids': [1],  # References 'ai'
            'grade_ids': [10, 11],
        },
        {
            'id': 2,
            'title': 'Введение в математику',
            'description': 'Основы алгебры и геометрии для начинающих.',
            'start_date': date(2025, 10, 1),
            'end_date': date(2026, 3, 1),
            'url': 'https://www.coursera.org/',
            'organization_id': 2,
            'difficulty_id': 2,
            'subject_ids': [2],  # References 'math'
            'grade_ids': [11, 12],
        },
    ]
    courses = []
    for data in courses_data:
        existing = session.exec(select(Course).where(Course.id == data['id'])).first()
        if not existing:
            # Extract relationship data
            subject_ids = data.pop('subject_ids')
            grade_ids = data.pop('grade_ids')
            course = Course(**data)
            session.add(course)
            # Add subject relationships
            for subject_id in subject_ids:
                session.add(CourseSubjectLink(course_id=course.id, subject_id=subject_id))
            # Add grade relationships
            for grade_id in grade_ids:
                session.add(CourseGradeLink(course_id=course.id, grade_id=grade_id))
            courses.append(course)
    session.commit()
    return courses


def populate_database():
    """Populate the database with mock data."""
    # Create database and tables
    create_db_and_models()

    with Session(engine) as session:
        print('Populating subjects...')
        subjects = create_subjects(session)
        print(f'Created {len(subjects)} subjects')

        print('Populating difficulties...')
        difficulties = create_difficulties(session)
        print(f'Created {len(difficulties)} difficulties')

        print('Populating organizations...')
        organizations = create_organizations(session)
        print(f'Created {len(organizations)} organizations')

        print('Populating grades...')
        grades = create_grades(session)
        print(f'Created {len(grades)} grades')

        print('Populating courses...')
        courses = create_courses(session)
        print(f'Created {len(courses)} courses')

        print('Database population completed.')


if __name__ == '__main__':
    populate_database()
