Marc Holman
CIS 2531 Introduction To Python Programming
12 / 2 / 2019

Tkinter Password/Web Account Data Manager:

The app requires installation of passlib dependency for password encryption.
'pip install passlib'

Start the application by running controller.py.

I tried to implement MVC pattern and modules are named as such.
Supporting modules include dao.py for data acccess, encryption.py for encryption,
and components.py for view components.

Data is stored in sqlite database - pwmdatabase.db
ID for the last saved login is stored in pwm-config.txt

The application includes a help screen you can access by hitting 'help' on the
menubar.

Since the project includes several files plus the dependency passlib I've included
the virtual environment (venv) in the zip archive so you can load the whole folder
into pycharm as a project.

Some test users are already included in the database:
user: marcholman9323@gmail.com
password:  password

user: codstudent@cod.edu
password: samplepassword
