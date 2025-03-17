import argparse
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, func
from models import Group, Student, Teacher, Subject, Grade

engine = create_engine("postgresql://postgres:19092008Max@localhost/postgres")
Session = sessionmaker(bind=engine)
session = Session()

MODELS = {
    "Group": Group,
    "Student": Student,
    "Teacher": Teacher,
    "Subject": Subject,
    "Grade": Grade,
}


def create_record(model, args):
    if model == "Grade":
        record = Grade(
            student_id=args.student_id,
            subject_id=args.subject_id,
            grade=args.grade,
            date_received=args.date_received,
        )
    elif model == "Subject":
        record_data = {"name": args.name, "teacher_id": args.teacher_id}
        record = MODELS[model](**record_data)
    else:
        record_data = (
            {"name": args.name} if model == "Group" else {"fullname": args.name}
        )
        record = MODELS[model](**record_data)

    session.add(record)
    session.commit()
    print(f"{model} created")


def update_record(model, args):
    record = session.query(MODELS[model]).filter(MODELS[model].id == args.id).first()
    if not record:
        print("Record not found")
        return

    if hasattr(record, "fullname"):
        record.fullname = args.name
    elif hasattr(record, "name"):
        record.name = args.name

    session.commit()
    print("Record updated")


def remove_record(model, args):
    record = session.query(MODELS[model]).filter(MODELS[model].id == args.id).first()
    if record:
        session.delete(record)
        session.commit()
        print("Record deleted")
    else:
        print("Record not found")


def list_records(model):
    records = session.query(MODELS[model]).all()
    for r in records:
        print(r.id, getattr(r, "name", getattr(r, "fullname", "")))


# Additional queries (Task 2)


def average_grade_teacher_student(teacher_id, student_id):
    avg_grade = (
        session.query(func.avg(Grade.grade))
        .join(Subject)
        .filter(Subject.teacher_id == teacher_id)
        .filter(Grade.student_id == student_id)
        .scalar()
    )
    print(
        f"Average grade given by teacher {teacher_id} to student {student_id}: {avg_grade}"
    )


def grades_last_lesson(group_id, subject_id):
    last_date = (
        session.query(func.max(Grade.date_received))
        .join(Student)
        .filter(Student.group_id == group_id, Grade.subject_id == subject_id)
        .scalar()
    )

    if last_date is None:
        print("No grades found for this subject and group.")
        return

    grades = (
        session.query(Student.fullname, Grade.grade)
        .join(Grade, Student.id == Grade.student_id)
        .filter(
            Student.group_id == group_id,
            Grade.subject_id == subject_id,
            Grade.date_received == last_date,
        )
        .all()
    )

    if not grades:
        print("No grades found on the last lesson.")
        return

    print(f"Grades on last lesson ({last_date}):")
    for fullname, grade in grades:
        print(fullname, grade)


def main():

    parser = argparse.ArgumentParser(description="CLI for CRUD operations")
    parser.add_argument(
        "-a",
        "--action",
        required=True,
        choices=[
            "create",
            "list",
            "update",
            "remove",
            "avg-grade-teacher-student",
            "last-grades",
        ],
        help="Action to perform",
    )
    parser.add_argument(
        "-m", "--model", choices=MODELS.keys(), help="Model to operate on"
    )
    parser.add_argument("--id", type=int, help="Record ID")
    parser.add_argument("-n", "--name", type=str, help="Name or fullname")

    parser.add_argument("--grade", type=float, help="Grade value")
    parser.add_argument("--date_received", help="Date YYYY-MM-DD")

    # Args for complex queries
    parser.add_argument("--teacher_id", type=int, help="Teacher ID for complex queries")
    parser.add_argument("--student_id", type=int, help="Student ID for complex queries")
    parser.add_argument("--group_id", type=int, help="Group ID for complex queries")
    parser.add_argument("--subject_id", type=int, help="Subject ID for complex queries")

    args = parser.parse_args()

    if args.action == "create":
        create_record(args.model, args)
    elif args.action == "list":
        list_records(args.model)
    elif args.action == "update":
        update_record(args.model, args)
    elif args.action == "remove":
        remove_record(args.model, args)
    # Complex queries
    elif args.action == "avg-grade-teacher-student":
        average_grade_teacher_student(args.teacher_id, args.student_id)
    elif args.action == "last-grades":
        grades_last_lesson(args.group_id, args.subject_id)


if __name__ == "__main__":
    main()
