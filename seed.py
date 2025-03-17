from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from faker import Faker
from random import randint, choice
from models import Group, Student, Teacher, Subject, Grade
from datetime import datetime

engine = create_engine("postgresql://postgres:19092008Max@localhost/postgres")
Session = sessionmaker(bind=engine)
session = Session()
fake = Faker()

# Create Groups
groups = [Group(name=f"Group-{i}") for i in range(1, 4)]
session.add_all(groups)
session.commit()

# Cteate Teachers
teachers = [Teacher(fullname=fake.name()) for _ in range(5)]
session.add_all(teachers)
session.commit()

# Create Subjects
subjects = [Subject(name=fake.word(), teacher=choice(teachers)) for _ in range(8)]
session.add_all(subjects)
session.commit()

# Create Students
students = [Student(fullname=fake.name(), group=choice(groups)) for _ in range(40)]
session.add_all(students)
session.commit()

# Create Grades
for student in students:
    for _ in range(randint(10, 20)):
        grade = Grade(
            student=student,
            subject=choice(subjects),
            grade=randint(50, 100),
            date_received=fake.date_between_dates(date_start=datetime(2023, 1, 1), date_end=datetime(2023, 12, 31))
        )
        session.add(grade)
session.commit()


