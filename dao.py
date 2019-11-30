"""
Marc D. Holman
CIS 2531 - Introduction to Python Programming

Term Project:  Password Manager Application

This file consists of the Model module for the application,
Model and Database/File access.

Class includes functions for reading/writing users/links to the database
and for reading the saved login from and writing a report to text files.
"""

from sqlite3 import *
from collections import namedtuple
from encryption import Encryption
from datetime import date


CONFIG_FILE = 'pwm-config.txt'

#  namedtuple is a factory function which subclasses named tuple.
UserTuple = namedtuple('User', ['id', 'email', 'password'])
LinkTuple = namedtuple('Link', ['id', 'user_id', 'site_name', 'username', 'url', 'note', 'password', 'security', 'email'])


class DataAccessClass:
    """ This class sets up a database connection and contains methods
    for reading and writing to the database and closing the connection """
    def __init__(self):
        self.__currentEntryId = 0
        self.encryption = Encryption()
        try:
            self.conn = connect('pwmdatabase.db')
            self.cursor = self.conn.cursor()
        except Error as exc:
            print(exc)

    def closeConnection(self):
        self.conn.close()

    def getLastUser(self):
        user_id = self.getLastUserIdFromFile()
        sql = f'SELECT id, email, password FROM users WHERE id={user_id}'
        self.cursor.execute(sql)
        user = self.cursor.fetchone()
        user = UserTuple(*user)
        return user

    def saveLogin(self, userId):
        with open(CONFIG_FILE, 'w') as config:
            config.write(str(userId))
            config.close()

    def getLastUserIdFromFile(self):
        with open(CONFIG_FILE, 'r') as config:
            user_id = config.readline().rstrip('/n')
            config.close()
        return user_id

    def userExists(self, username):
        sql = f'SELECT rowid FROM USERS WHERE email = ?'
        self.cursor.execute(sql, ((username, )))
        data = self.cursor.fetchall()
        if len(data) == 0:
            return False
        return True

    # def getUserByEmailAndPassword(self, email, password):
    #     #  hash the password
    #     sql = f"SELECT * FROM users WHERE email = '{email}' AND password = '{password}'"
    #     self.cursor.execute(sql)
    #     user = self.cursor.fetchone()
    #     user = UserTuple(*user)
    #     return user

    def getUserCheckPw(self, email, password):
        # get the user info by email
        sql = f'SELECT * FROM users WHERE email = ?'
        self.cursor.execute(sql, (email, ))
        user = self.cursor.fetchone()
        user = UserTuple(*user)

        # is the pw valid?
        passwordValid = self.encryption.check_encrypted_password(password, user.password)

        if passwordValid:
            return user
        else:
            return False

    def getLinks(self, userId):
        sql = f"SELECT * FROM links WHERE user_id = ?"
        links = self.cursor.execute(sql, (userId, ))
        links = self.cursor.fetchall()
        #  loop through and cast each link item to LinkTuple
        links = [LinkTuple(*item) for item in links]
        return links

    def getLinkBySiteName(self, sitename):
        # sitename must be unique for this to work
        sql = f"SELECT * FROM links WHERE site_name = ?"
        self.cursor.execute(sql, (sitename, ))
        link = self.cursor.fetchone()
        link = LinkTuple(*link)
        print("getLinkBySiteName link id: ", link.id)
        return link

    def deleteLink(self, linkId):
        sql = f"DELETE FROM links WHERE id=?"
        rowCount = self.cursor.execute(sql, (linkId, ))
        self.conn.commit()

    def updateLink(self, link):
        print("updateLink link.id == ", link.id)
        sql = f"UPDATE links SET user_id = ?, site_name = ?," \
              f" username = ?, url = ?, note = ?, password = ?, security = ?," \
              f"email = ? WHERE id = ?"
        values = (link.user_id, link.site_name, link.username, link.url, link.note,
                            link.password, link.security, link.email, link.id)
        self.cursor.execute(sql, values)
        self.conn.commit()

    def saveLink(self, link, user_id):
        sql = f"INSERT INTO links(user_id, site_name, username, url, note, password, security, email)" \
              f"VALUES(?,?,?,?,?,?,?,?)"
        values = (user_id, link.site_name, link.username, link.url, link.note, link.password,
                  link.security, link.email)
        self.cursor.execute(sql, values)
        lastRowId = self.cursor.lastrowid
        self.conn.commit()
        return lastRowId

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

    #  sorts links in alphabetical order, outputs a report to text file
    def printReport(self, principalEmail, links):
        #  the lambda acts as an anonymous function which simply returns link.site_name
        #  for us to sort by.
        links = sorted(links, key=lambda link: link.site_name)
        #  get today's date
        today = date.today()
        #  parse it to month day year
        monthDayYear = today.strftime("%B %d, %Y")
        # open file 'password-report.txt', write data, close file
        with open('password-report.txt', 'w') as report:
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

    @property
    def currentEntryId(self):
        return self.__currentEntryId

    @currentEntryId.setter
    def currentEntryId(self, currentEntryId):
        self.__currentEntryId = currentEntryId
