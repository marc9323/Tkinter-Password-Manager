Marc Holman
CIS 2531 Introduction To Python Programming
12 / 2 / 2019

Tkinter Password/Web Account Data Manager:

This app allows multiple users sharing the same computer to store passwords and
other data related to accounts on the web - basic CRUD functionality for
web account data.

It requires installation of passlib dependency for password encryption:
'pip install passlib'

Since the project includes several files plus the dependency passlib I've included
the virtual environment (venv) in the zip archive so you can load the whole folder
into pycharm as a project.

Start the application by running controller.py.

I tried to implement MVC pattern and modules are named as such.
Supporting modules include dao.py for data acccess, encryption.py for encryption,
and components.py for view components.

Data is stored in sqlite database - pwmdatabase.db
ID for the last saved login is stored in pwm-config.txt

The application includes a help screen you can access by hitting 'help' on the
menubar.

Some test users are already included in the database:
user: marcholman9323@gmail.com
password:  password

user: codstudent@cod.edu
password: samplepassword

user:  cameljoe@hotmail.com
password: password

Potential Problems/unimplemented features:
1.)  It isn't really secure at this point - user passwords are encrypted but I haven't yet
implemented encryption for web account passwords.  Also the saved login has a
security flaw - the last saved user is always loaded upon startup and someone could alter the config file.
It would probably be best to eliminate this feature or just default to a sample user.
2.)  If the user intends to update an entry and hits 'add entry' instead a duplicate entry will appear.
The solution would be to a.) check for duplicates  b.)  update sql to require unique entries so that
a sql exception would be thrown upon attempt to add duplicate.
3.)  The GUI should be updated to allow resizing.
4.)  onListBoxSelect in controller.py throws IndexError sporadically when fields are cleared using backspace.
5.)  I used the sqlite shell inside PyCharm to create the database  -- Need to develop a way to initialize
a fresh database on very first startup.
