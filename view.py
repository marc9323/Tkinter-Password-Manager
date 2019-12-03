"""
Marc D. Holman
CIS 2531 - Introduction to Python Programming
11 / 17 / 2019

Term Project - Tkinter Password Manager Application

Module: view.py
This file consists of the view module for the application and
extends Frame.  Here the components are assembled on placed on the
single frame.
"""

from dao import *
from components import *
from tkinter import messagebox

class View(Frame):
    def __init__(self, master, model):
        """ Set up and display the user interface """
        Frame.__init__(self, master)
        self.model = model
        #  assemble the view components and place them in the main view frame
        self.menubar = Menu(master)
        self.menubar.add_command(label="Print Report")
        self.menubar.add_command(label="Help")
        self.menubar.add_command(label="Exit")
        self.currentUserLabel = Label(self.master, text='Web Accounts For: ')
        self.master = master
        self.loginFrame = LoginFrame(self)
        self.registerFrame = RegisterFrame(self)
        self.siteListBoxFrame = SiteListBoxFrame(self)
        self.addSiteFrame = AddSiteFrame(self)
        self.currentUserLabel = Label(self, text="Accounts for User:", fg='red', bg='black')
        self.master.config(menu=self.menubar)

        #  assemble using grid manager
        self.currentUserLabel.grid(row=0, column=0, pady=10, padx=15)
        self.loginFrame.grid(row=1, column=0, sticky=NW, pady=10, padx=15)
        self.registerFrame.grid(row=1, column=1, sticky=NE, pady=10, padx=15)
        self.addSiteFrame.grid(row=2, column=0, pady=10, padx=15)
        self.siteListBoxFrame.grid(row=2, column=1, sticky=N, pady=10, padx=15)

    #  populates the listbox of web accounts using data from the model.links
    def populateSiteListBox(self):
        for item in self.model.links:
            self.siteListBoxFrame.siteListBox.insert(END, item.site_name)

    #  populates the form for entering/reading web account data based on data
    #  passed from controller -- refactor to use the model
    def populateSiteEntryForm(self, linkData):
        self.clearForm()
        self.addSiteFrame.username.set(linkData.username)
        self.addSiteFrame.siteName.set(linkData.site_name)
        self.addSiteFrame.email.set(linkData.email)
        self.addSiteFrame.url.set(linkData.url)
        self.addSiteFrame.security.set(linkData.security)
        self.addSiteFrame.password.set(linkData.password)
        self.addSiteFrame.note.set(linkData.note)

    #  fetches data entered by the user for a web account
    #  and returns it in the form of a LinkTuple
    def getLinkDataFromForm(self):
        siteName = self.addSiteFrame.siteName.get().strip()
        url = self.addSiteFrame.url.get().strip()
        username = self.addSiteFrame.username.get().strip()
        email = self.addSiteFrame.email.get().strip()
        note = self.addSiteFrame.note.get().strip()
        security = self.addSiteFrame.security.get().strip()
        password = self.addSiteFrame.password.get().strip()

        link = LinkTuple(site_name=siteName, url=url, username=username, note=note,
                         user_id=self.model.principal.id, password=password, id=self.model.currentEntryId,
                         security=security, email=email)
        return link

    #  set the current user label based on the model.principal.email
    def setCurrentUserLabel(self):
        self.currentUserLabel['text'] = f"Web Accounts For: {self.model.principal.email}"

    #  clears the form containing web account data
    def clearForm(self):
        self.addSiteFrame.siteUsernameEntry.delete(0, END)
        self.addSiteFrame.siteNameEntry.delete(0, END)
        self.addSiteFrame.emailUsedToRegisterEntry.delete(0, END)
        self.addSiteFrame.urlEntry.delete(0, END)
        self.addSiteFrame.securityQuestionAnswer1Entry.delete(0, END)
        self.addSiteFrame.passwordEntry.delete(0, END)
        self.addSiteFrame.noteEntry.delete(0, END)

    #  clears the list box containing web account names
    def clearListBox(self):
        self.siteListBoxFrame.siteListBox.delete(0, END)
        self.update()

    #  clears the login box fields
    def clearLogin(self):
        self.loginFrame.usernameEntry.delete(0, END)
        self.loginFrame.passwordEntry.delete(0, END)

    #  change color of fields to provide user feedback
    def setLoginFieldsRed(self):
        self.loginFrame.usernameEntry['bg'] = 'red'
        self.loginFrame.passwordEntry['bg'] = 'red'

    def setLoginFieldsWhite(self):
        self.loginFrame.usernameEntry['bg'] = 'white'
        self.loginFrame.passwordEntry['bg'] = 'white'

    def setRegisterUsernameRed(self):
        self.registerFrame.usernameEntry['bg'] = 'red'

    def setRegisterUsernameWhite(self):
        self.registerFrame.usernameEntry['bg'] = 'white'

    #  unused
    def showInfoMessageBox(self, title, info):
        messagebox.showinfo(title, info)








