from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from models import Group, Student, Teacher, Subject, Grade

engine = create_engine("postgresql://postgres:19092008Max@localhost/postgres")
Session = sessionmaker(bind=engine)
session = Session()


# Query 1: TOP-5 students by average grade
def select_1():
    return (
        session.query(Student.fullname, func.avg(Grade.grade))
        .join(Grade)
        .group_by(Student.id)
        .order_by(func.avg(Grade.grade).desc())
        .limit(5)
        .all()
    )


# Query 2 - the best student in a specific subject
def select_2(subject_id):
    return (
        session.query(Student.fullname, func.avg(Grade.grade))
        .join(Grade)
        .filter(Grade.subject_id == subject_id)
        .group_by(Student.id)
        .order_by(func.avg(Grade.grade).desc())
        .first()
    )


# Query 3 - average grade in groups by subject
def select_3(subject_id):
    return (
        session.query(Group.name, func.avg(Grade.grade))
        .select_from(Group)
        .join(Student, Student.group_id == Group.id)
        .join(Grade, Grade.student_id == Student.id)
        .filter(Grade.subject_id == subject_id)
        .group_by(Group.id)
        .all()
    )


# Query 4 - average grade on the entire stream
def select_4():
    return session.query(func.avg(Grade.grade)).scalar()


# Query 5 - subjects of a specific teacher
def select_5(teacher_id):
    return session.query(Subject.name).filter(Subject.teacher_id == teacher_id).all()


# Query 6 - list of students in a group
def select_6(group_id):
    return session.query(Student.fullname).filter(Student.group_id == group_id).all()


# Query 7 - grades of students in a group for a specific subject
def select_7(group_id, subject_id):
    return (
        session.query(Student.fullname, Grade.grade)
        .join(Grade)
        .filter(Student.group_id == group_id, Grade.subject_id == subject_id)
        .all()
    )


# Query 8 - average grade given by a teacher
def select_8(teacher_id):
    return (
        session.query(func.avg(Grade.grade))
        .join(Subject)
        .filter(Subject.teacher_id == teacher_id)
        .scalar()
    )


# Query 9 - list of courses attended by a student
def select_9(student_id):
    return (
        session.query(Subject.name)
        .join(Grade)
        .filter(Grade.student_id == student_id)
        .group_by(Subject.id)
        .all()
    )


# Query 10 - courses taught by a specific teacher to a specific student
def select_10(student_id, teacher_id):
    return (
        session.query(Subject.name)
        .join(Grade)
        .filter(Grade.student_id == student_id, Subject.teacher_id == teacher_id)
        .group_by(Subject.name)
        .all()
    )


# Additional complex query #1
def avg_grade_teacher_to_student(teacher_id, student_id):
    return (
        session.query(func.avg(Grade.grade))
        .join(Subject)
        .filter(Subject.teacher_id == teacher_id, Grade.student_id == student_id)
        .scalar()
    )


# Additional complex query #2
def grades_last_lesson(group_id, subject_id):
    last_date = (
        session.query(func.max(Grade.date_received))
        .join(Student)
        .filter(Student.group_id == group_id, Grade.subject_id == subject_id)
        .scalar()
    )

    if not last_date:
        return []

    return (
        session.query(Student.fullname, Grade.grade)
        .join(Grade)
        .filter(
            Student.group_id == group_id,
            Grade.subject_id == subject_id,
            Grade.date_received == last_date,
        )
        .all()
    )


if __name__ == "__main__":
    Session = sessionmaker(bind=engine)
    session = Session()

    def print_results():
        print("\n--- Top 5 students by average grade ---")
        for fullname, avg_grade in select_1():
            print(f"Student: {fullname:<30} | Avg grade: {avg_grade:.2f}")

        best_student = select_2(1)
        print("\n--- Best student in subject 1 ---")
        print(f"Student: {best_student[0]:<30} | Avg grade: {best_student[1]:.2f}")

        print("\n--- Average grades in groups by subject 1 ---")
        for group, avg_grade in select_3(1):
            print(f"Group: {group:<30} | Avg grade: {avg_grade:.2f}")

        avg_stream = select_4()
        print("\n--- Average grade on entire stream ---")
        print(f"Stream avg grade: {avg_stream:.2f}")

        print("\n--- Subjects taught by teacher 1 ---")
        for subject in select_5(1):
            print(f"- {subject[0]}")

        print("\n--- Students in group 1 ---")
        for student in select_6(1):
            print(f"- {student[0]}")

        print("\n--- Grades of students in group 1 for subject 1 ---")
        for student, grade in select_7(1, 1):
            print(f"Student: {student:<30} | Grade: {grade:.2f}")

        teacher_avg = select_8(1)
        print("\n--- Average grade given by teacher 1 ---")
        print(f"Teacher avg grade: {teacher_avg:.2f}")

        print("\n--- Courses attended by student 1 ---")
        for course in select_9(1):
            print(f"- {course[0]}")

        print("\n--- Courses taught by teacher 1 to student 1 ---")
        for course in select_10(1, 1):
            print(f"- {course[0]}")

        avg_teacher_student = avg_grade_teacher_to_student(1, 1)
        print("\n--- Average grade given by teacher 1 to student 1 ---")
        print(f"Avg grade: {avg_teacher_student:.2f}")

        print("\n--- Grades on last lesson (group 1, subject 1) ---")
        last_grades = grades_last_lesson(1, 1)
        if last_grades:
            for student, grade in last_grades:
                print(f"Student: {student:<30} | Grade: {grade:.2f}")
        else:
            print("No grades found for the last lesson.")

if __name__ == "__main__":
    print_results()
