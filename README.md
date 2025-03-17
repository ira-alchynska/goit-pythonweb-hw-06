# goit-pythonweb-hw-06

## How to Test `crud.py`

To test the `crud.py` script, follow these steps:

run virtual env.
activate virtual env.
**run commands:**

1. python crud.py -a create -m Teacher -n "Teacher Name"
2. python crud.py -a list -m Teacher
3. python crud.py -a update -m Teacher --id 3 -n "Teacher Name"
4. python crud.py -a avg-grade-teacher-student --teacher_id 1 --student_id 5
5. python crud.py -a last-grades --group_id 2 --subject_id 4
