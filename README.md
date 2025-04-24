# Agri Training Web App

## Burair - B00138007
## Topic : Agriculture – Training (Module – Students)

Web Framework Development - H3037
Lecturer : Anh Duong Trinh

This is my submission of a  Django web app to manage agricultural training modules. Admins can create modules, assign trainers, and manage student enrollments.

## Features:
- Admin, trainer and student roles
- Add, edit and delete modules
- Student enrollments
- Trainer assignments
- Upload weekly module files

## Setup Instructions:

Requirements:
- Python 
- Django installed (pip install django)

Steps to run:

1. Clone the repo
2. Open a terminal in the folder with manage.py
3. Run these:

python manage.py makemigrations
python manage.py migrate

4. Load data into the database:

python manage.py loaddata training/fixtures/users.json
python manage.py loaddata training/fixtures/modules.json
python manage.py loaddata training/fixtures/enrollments.json
python manage.py loaddata training/fixtures/trainerassignments.json
python manage.py loaddata training/fixtures/modulefiles.json

5. Start the server:

python manage.py runserver

6. Use these test accounts:

Admin - username: admin, password: password  
Trainer - username: trainer1, password: password  
Student - username: student1, password: password

Testing:

To run all tests:

python manage.py test training

Image/Gif credits are listed in public/sources.txt
