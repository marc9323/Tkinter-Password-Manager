"""
Marc D. Holman
CIS 2531 - Introduction to Python Programming

Term Project:  Password Manager Application

This file consists of the data access module for the application,
Model and Database/File access.

Class includes functions for reading/writing users/links to the database
and for reading the saved login from and writing a report to text files.
"""

from sqlite3 import *
from model import UserTuple, LinkTuple
from encryption import Encryption
from datetime import date
from tkinter import messagebox

#  decorator will simplify exception handling for repetitive db transactions
#  instead of a try, catch block in each function, use decorator
#  A database error will cause the application to shut down after notifying the user
#  and displaying the error inside tkinter messagebox
def db_try_catch(func):
    #  func is the function the decorator wraps
    def func_wrapper(*args, **kwargs):
        try:
            #  try returning the function
           return func(*args, **kwargs)
        except Exception as ex:
            #  if exception thrown display it in messagebox and terminate application
            messagebox.showerror("DATABASE ERROR", f"Fatal Exception Thrown. \nApplication Terminating.\n{ex}")
            exit()
            # return None

    return func_wrapper

#  NOTE:  sqlite does not enforce types, i.e. you can insert an integer value into a text column!
#  NOTE:  sqlite a column with type Integer primary key is an alias for the rowid,
#  hence use of lastrowid below in saveLink and saveUser
class DataAccessClass:
    """ This class sets up a database connection and contains methods
    for reading and writing to the database and closing the connection.
    It also contains methods for reading/writing to the config file which
    stores last saved login user id and for generating a report containing
    all of the web accounts data for a single user"""

    # class constants
    #  this file simply stores a user id #
    CONFIG_FILE = 'pwm-config.txt'
    #  database file which holds users and links (web accounts)
    DATABASE_FILE = 'pwmdatabase.db'
    #  used for generating a text file containing all the accounts for the user
    USER_REPORT = 'password-report.txt'

    def __init__(self):
        #  gets a reference to class with passlib encryption methods
        self.encryption = Encryption()
        try:
            #  connect, get db cursor
            self.conn = connect(DataAccessClass.DATABASE_FILE)
            #  cursor is a generator, a type of iterable that generates next value each time used.
            self.cursor = self.conn.cursor()
        except Error as exc:
            print(exc)

    #  closes db connection
    def closeConnection(self):
        self.conn.close()

    #  fetches the last user (saved login) from the database based on the
    #  stored user id
    @db_try_catch
    def getLastUser(self):
        user_id = self.getLastUserIdFromFile()
        #  sql statement
        sql = f'SELECT id, email, password FROM users WHERE id={user_id}'
        # executes sql
        self.cursor.execute(sql)
        # fetchone returns a single record
        user = self.cursor.fetchone()
        user = UserTuple(*user)
        return user

    #  saves the id of last user if save login box is checked
    @db_try_catch
    def saveLogin(self, userId):
        with open(DataAccessClass.CONFIG_FILE, 'w') as config:
            config.write(str(userId))
            config.close()

    #  retrieves the id of the last saved user from config file
    @db_try_catch
    def getLastUserIdFromFile(self):
        with open(DataAccessClass.CONFIG_FILE, 'r') as config:
            user_id = config.readline().rstrip('/n')
            config.close()
        return user_id

    #  checks if a user with that email/username exists
    @db_try_catch
    def userExists(self, username):
        #  '?' is query parameter
        sql = f'SELECT rowid FROM USERS WHERE email = ?'
        #  pass tuple containing query params along with sql to execute method
        self.cursor.execute(sql, ((username, )))
        #  fetchall returns all records for the select stmt
        data = self.cursor.fetchall()
        #  if no data is returned...
        if len(data) == 0:
            return False
        return True

    #  fetches a user and checks to see if the password passed is a match
    @db_try_catch
    def getUserCheckPw(self, email, password):
        # get the user info by email
        sql = f'SELECT * FROM users WHERE email = ?'
        self.cursor.execute(sql, (email, ))
        user = self.cursor.fetchone()
        user = UserTuple(*user)

        # is the pw valid?
        passwordValid = self.encryption.check_encrypted_password(password, user.password)

        #  refactor - better when methods don't return different types like this?
        if passwordValid:
            return user
        else:
            return False

    #  get all the links (web accounts) for a user by id
    @db_try_catch
    def getLinks(self, userId):
        sql = f"SELECT * FROM links WHERE user_id = ?"
        links = self.cursor.execute(sql, (userId, ))
        links = self.cursor.fetchall()
        #  use list comprehension to cast to LinkTuple
        links = [LinkTuple(*item) for item in links]
        return links

    #  retrieve a link (web account) by name
    @db_try_catch
    def getLinkBySiteName(self, sitename):
        # sitename must be unique for this to work
        sql = f"SELECT * FROM links WHERE site_name = ?"
        self.cursor.execute(sql, (sitename, ))
        link = self.cursor.fetchone()
        link = LinkTuple(*link)
        return link

    #  delete a link
    @db_try_catch
    def deleteLink(self, linkId):
        sql = f"DELETE FROM links WHERE id=?"
        rowCount = self.cursor.execute(sql, (linkId, ))  #  don't need
        #  if we fail to commit, all changes will be gone next time we run the program
        self.conn.commit()

    #  update a link
    @db_try_catch
    def updateLink(self, link):
        sql = f"UPDATE links SET user_id = ?, site_name = ?," \
              f" username = ?, url = ?, note = ?, password = ?, security = ?," \
              f"email = ? WHERE id = ?"
        values = (link.user_id, link.site_name, link.username, link.url, link.note,
                            link.password, link.security, link.email, link.id)
        self.cursor.execute(sql, values)
        #  if we fail to commit, all changes will be gone next time we run the program
        self.conn.commit()

    #  save a link
    @db_try_catch
    def saveLink(self, link, user_id):
        sql = f"INSERT INTO links(user_id, site_name, username, url, note, password, security, email)" \
              f"VALUES(?,?,?,?,?,?,?,?)"
        values = (user_id, link.site_name, link.username, link.url, link.note, link.password,
                  link.security, link.email)
        self.cursor.execute(sql, values)
        lastRowId = self.cursor.lastrowid
        self.conn.commit()
        return lastRowId

    #  save a user after registration and return a UserTuple
    @db_try_catch
    def saveUser(self, email, password):
        #  encrypt the password first
        encryptedPassword = self.encryption.encrypt_password(password)
        values = (email, encryptedPassword)
        # values = (email, password)
        sql = f"INSERT INTO users (email, password) VALUES (?,?)"
        self.cursor.execute(sql, values)
        userId = self.cursor.lastrowid
        self.conn.commit()
        return UserTuple(id=userId, email=email, password=password)

    #  outputs a report to a text file containing the web account data sorted a-z
    def printReport(self, principalEmail, links):
        #  links are already sorted in alphabetical order
        #  get today's date
        today = date.today()
        #  parse it to month day year
        monthDayYear = today.strftime("%B %d, %Y")
        # open file 'password-report.txt', write data, close file
        with open(DataAccessClass.USER_REPORT, 'w') as report:
            report.write(f"Web Account Data Report\nPrepared: {monthDayYear}\nFor User: {principalEmail}".upper())
            report.write('\n')
            report.write("=" * 40)
            report.write('\n\n')
            for link in links:
                report.write('*' * 5 + '--> ' + link.site_name.upper() + ' <--' + '*' * 5 + '\n')
                report.write(f"Username: {link.username}\n"
                             f"Email user to register: {link.email}\n"
                             f"URL: {link.url}\n"
                             f"Password: {link.password}\n"
                             f"Security: {link.security}\n"
                             f"Note: {link.note}\n\n")
            report.close()

