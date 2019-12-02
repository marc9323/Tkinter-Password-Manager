"""
Marc D. Holman
CIS 2531 - Introduction to Python
12 / 02 / 2019

Term Project - Tkinter Password Manager Application

Module: components.py
consists of components used to build the view for the
application.  Each component subclasses tkinter LabelFrame:

RegisterFrame - user registration
LoginFrame -- user login
SiteListBoxFrame -- display web account names in listbox
AddSiteFrame -- data entry form
"""

from tkinter import *


class RegisterFrame(LabelFrame):
    """
    RegisterFrame class assembles into a LabelFrame the fields for
    user registration.
    """
    def __init__(self, master):
        LabelFrame.__init__(self, master, text='Register as a New User')

        #  StringVar to hold username and password
        self.username = StringVar()
        self.password = StringVar()

        #  Label, Entry, Button
        self.usernameLabel = Label(self, text="Username: ")
        self.passwordLabel = Label(self, text="Password: ")
        self.usernameEntry = Entry(self, textvariable=self.username, width=30)
        self.passwordEntry = Entry(self, textvariable=self.password, width=30)
        self.registerButton = Button(self, text='Register')

        #  assemble using grid manager
        self.usernameLabel.grid(row=0, column=0)
        self.usernameEntry.grid(row=0, column=1)
        self.passwordLabel.grid(row=1, column=0)
        self.passwordEntry.grid(row=1, column=1)
        self.registerButton.grid(row=3, column=1, sticky=E, pady=25, padx=25)


class LoginFrame(LabelFrame):
    """
    LoginFrame class holds the login fields for user login.
    """
    def __init__(self, master):
        LabelFrame.__init__(self, master, text="Login")

        # Int and String vars
        self.checkVar = IntVar()
        self.username = StringVar()
        self.password = StringVar()

        #  labels, checkbutton,  entries, and button
        self.usernameLabel = Label(self, text="Username: ")
        self.passwordLabel = Label(self, text="Password: ")
        self.saveLoginCheckbutton = Checkbutton(self, variable=self.checkVar,
                                           text="Save Login")
        self.usernameEntry = Entry(self, textvariable=self.username, width=30)
        self.passwordEntry = Entry(self, textvariable=self.password, width=30)
        self.loginButton = Button(self, text="Login")

        #  assemble using grid manager
        self.usernameLabel.grid(row=0, column=0)
        self.usernameEntry.grid(row=0, column=1)
        self.passwordLabel.grid(row=1, column=0)
        self.passwordEntry.grid(row=1, column=1)

        self.saveLoginCheckbutton.grid(row=2, column=0)
        self.loginButton.grid(row=2, column=1, sticky=E, pady=25, padx=25)


class SiteListBoxFrame(LabelFrame):
    """
    SiteListBoxFrame holds the listbox containing the names of the users
    web accounts and a scrollbar.
    """
    def __init__(self, master):
        LabelFrame.__init__(self, master, text="Active Accounts", padx=15)

        #  listbox with sunken border
        self.siteListBox = Listbox(self, width=25)
        self.siteListBox.config(border=2, relief='sunken')

        #  scrollbar
        self.listScroll = Scrollbar(self, orient=VERTICAL,
                               command=self.siteListBox.yview)
        self.siteListBox['yscrollcommand'] = self.listScroll.set

        #  button
        self.siteListBoxDeleteButton = Button(self, text='Delete Entry')

        #  assemble using grid manager
        self.listScroll.grid(row=0, column=1, sticky='nsw', rowspan=3)
        self.siteListBox.grid(row=0, column=0, rowspan=2, sticky='nsew')
        self.siteListBoxDeleteButton.grid(row=2, column=0, sticky=W, pady=10, padx=25)


class AddSiteFrame(LabelFrame):
    """
    AddSiteFrame class holds the fields for entering web account data and password
    """
    def __init__(self, master):
        LabelFrame.__init__(self, master, text="Store Additional Passwords:")
        # StringVars
        self.username = StringVar()
        self.siteName = StringVar()
        self.url = StringVar()
        self.email = StringVar()
        self.security = StringVar()
        self.password = StringVar()
        self.note = StringVar()

        #  instantiate components
        self.siteNameLabel = Label(self, text="Account Name: ", justify=LEFT, anchor=E)
        self.siteNameEntry = Entry(self, width=45, textvariable=self.siteName)
        self.urlLabel = Label(self, text="Account Link: ", justify=LEFT, anchor=E)
        self.urlEntry = Entry(self, width=45, textvariable=self.url)
        self.siteUsernameLabel = Label(self, text="Account Username: ", justify=LEFT, anchor=E)
        self.siteUsernameEntry = Entry(self, width=45, textvariable=self.username)
        self.emailUsedToRegisterLabel = Label(self, text="Account Email:")
        self.emailUsedToRegisterEntry = Entry(self, width=45, textvariable=self.email)
        self.securityQuestionAnswer1Label = Label(self, text="Security Questions:")
        self.securityQuestionAnswer1Entry = Entry(self, width=45, textvariable=self.security)
        self.noteLabel = Label(self, text="Notes: ")
        self.noteEntry = Entry(self, width=45, textvariable=self.note)
        self.passwordLabel = Label(self, text="Password: ")
        self.passwordEntry = Entry(self, width=45, textvariable=self.password)

        self.updateEntryButton = Button(self, text="Update Entry")
        self.addEntryButton = Button(self, text="Add Entry")
        self.clearButton = Button(self, text="Clear Form")

        #  assemble using grid manager
        self.siteNameLabel.grid(row=0, column=0, padx=3, pady=3)
        self.siteNameEntry.grid(row=0, column=1, sticky=EW,  padx=3, pady=3)
        self.urlLabel.grid(row=1, column=0,  padx=3, pady=3)
        self.urlEntry.grid(row=1, column=1, sticky=EW,  padx=3, pady=3)
        self.siteUsernameLabel.grid(row=2, column=0,  padx=3, pady=3)
        self.siteUsernameEntry.grid(row=2, column=1, sticky=EW,  padx=3, pady=3)
        self.emailUsedToRegisterLabel.grid(row=3, column=0,  padx=3, pady=3)
        self.emailUsedToRegisterEntry.grid(row=3, column=1, sticky=EW,  padx=3, pady=3)
        self.passwordLabel.grid(row=4, column=0,  padx=3, pady=3)
        self.passwordEntry.grid(row=4, column=1, sticky=EW,  padx=3, pady=3)
        self.securityQuestionAnswer1Label.grid(row=5, column=0,  padx=3, pady=3)
        self.securityQuestionAnswer1Entry.grid(row=5, column=1, sticky=EW,  padx=3, pady=3)
        self.noteLabel.grid(row=6, column=0,  padx=3, pady=3)
        self.noteEntry.grid(row=6, column=1, sticky=EW,  padx=3, pady=3)

        #  buttonFrame holds update, add entry, and clear form buttons
        self.buttonFrame = Frame(self)
        self.updateEntryButton = Button(self.buttonFrame, text="Update Entry")
        self.addEntryButton = Button(self.buttonFrame, text="Add Entry")
        self.clearButton = Button(self.buttonFrame, text="Clear Form")

        self.buttonFrame.grid(row=7, column=1, sticky=W)
        self.updateEntryButton.grid(row=0, column=1, padx=10, pady=5)
        self.addEntryButton.grid(row=0, column=2, padx=10, pady=5)
        self.clearButton.grid(row=0, column=3, padx=10, pady=5)





