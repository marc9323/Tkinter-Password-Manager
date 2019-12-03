"""
Marc D. Holman
CIS 2531 - Introduction to Python Programming
11 / 17 / 2019

Term Project - Tkinter Password Manager Application

Module: controller.py
consists of the main Controller and entry/exit point for the application.
"""

from dao import *
from model import *
from view import *
from tkinter import messagebox
import re
import webbrowser as wb


class Controller:
    def __init__(self):
        #  initialize Tk, set geometry, and title, no resizing
        self.root = Tk()
        self.root.geometry('890x600')
        self.root.resizable(False, False);
        self.root.title("Password Manager Application")

        #  get reference to DAO and the view, pass root to View
        self.dao = DataAccessClass()
        self.model = Model()
        self.view = View(self.root, self.model)

        #  use the DAO to set the principal (current user) and associated links
        #  since user has option of checking 'save login' the app will check for
        #  a saved login and open to that users accounts
        self.model.principal = self.dao.getLastUser()
        #  get all the links for the user
        self.model.links = self.dao.getLinks(self.model.principal.id)

        #  bind view widgets to controller methods
        self.view.siteListBoxFrame.siteListBox.bind('<<ListboxSelect>>', self.onListBoxSelect)
        self.view.menubar.entryconfigure(1, command=self.printReport)  #  print report menu option
        self.view.menubar.entryconfigure(2, command=self.help)  #  help menu option
        self.view.menubar.entryconfigure(3, command=self.exit)  #  exit menu option
        self.view.addSiteFrame.updateEntryButton['command'] = self.updateLink
        self.view.addSiteFrame.addEntryButton['command'] = self.addLink
        self.view.addSiteFrame.clearButton['command'] = self.view.clearForm
        self.view.loginFrame.loginButton['command'] = self.processLogin
        self.view.registerFrame.registerButton['command'] = self.registerUser
        self.view.siteListBoxFrame.siteListBoxDeleteButton['command'] = self.deleteLink

        #  populate the list box with the links for the principal, set current user label,
        #  and set focus to login
        self.view.populateSiteListBox()
        self.view.setCurrentUserLabel()
        self.view.loginFrame.usernameEntry.focus()


    #  runs when user hits 'login' button
    def processLogin(self):
        email = self.view.loginFrame.username.get().strip()
        password = self.view.loginFrame.password.get().strip()
        #  is the form incompletely filled out?
        if email == '' or password == '':
            messagebox.showwarning('Warning', 'Please enter username AND password.')
            self.view.setLoginFieldsRed()
            return
        # is the user already logged in?
        if email == self.model.principal.email:
            messagebox.showwarning('Warning', f'User: {self.model.principal.email} is already logged in.')
            return
        #  fields filled in properly so process login
        try:
            user = self.dao.getUserCheckPw(email, password)
            #  if False is returned login failed - password didn't match
            if not user:
                messagebox.showwarning('Login Failed', 'Enter a valid password.')
                self.view.setLoginFieldsRed()
                return
        except TypeError:
            messagebox.showwarning('Login Failure', 'Enter a valid username (email) and password.')
            self.view.setLoginFieldsRed()
        else:
            #   now a new user is logged in, set the principal and get his links
            self.model.principal = user
            #  fetch links by user id
            self.model.links = self.dao.getLinks(self.model.principal.id)
            #  if save login box is checked, write id to file
            if self.view.loginFrame.checkVar.get() == 1:
                self.dao.saveLogin(self.model.principal.id)
            #  update gui
            self.view.clearListBox()
            self.view.populateSiteListBox()
            self.view.setCurrentUserLabel()
            self.view.clearForm()
            self.view.setLoginFieldsWhite()
            #  use messagebox to provide user feedback - successful login
            messagebox.showinfo('Login Successful!', f'User {self.model.principal.email} logged in.')

    #  runs when user clicks 'register' buttons -- add check to see if user already exists!
    def registerUser(self):
        username = self.view.registerFrame.username.get().strip()
        password = self.view.registerFrame.password.get().strip()
        #  is either field blank?
        if username == '' or password == '':
            messagebox.showwarning('Warning!', 'Enter a valid email address AND choose a password.')
            return
        # validate that email is an email address
        if not self.checkEmail(username):
            messagebox.showwarning('Warning!', 'Enter a valid email address.')
            self.view.setRegisterUsernameRed()
            return
        #  check if a user with that email already exists
        if self.dao.userExists(username):
            messagebox.showwarning('Warning', f'User: {username} already exists.\n'
                                              f'Pick a different username/email.')
            self.view.setRegisterUsernameRed()
            return
        else:
            try:
                #  returns a UserTuple
                user = self.dao.saveUser(username, password)
                #  set the principal to the UserTuple returned above
                self.model.principal = user
            except TypeError:
                messagebox.showerror('Registration Failed', 'Enter Valid data\nSee Marc if problem persists.')
            else:
                #  blank out the password and username in registerFrame
                self.view.registerFrame.passwordEntry.delete(0, END)
                self.view.registerFrame.usernameEntry.delete(0, END)
                self.view.setRegisterUsernameWhite()
                #  set current user label and clear GUI
                self.view.setCurrentUserLabel()
                self.view.clearListBox()
                self.view.clearForm()
                self.view.clearLogin()
                #  provide feedback on successful registration
                messagebox.showinfo(f'Registered New User: {username}',
                                    f'Your password is: {password}\nWrite it down now!')

    #  runs when user hits 'Add Entry' button
    def addLink(self):
        #  returns a LinkTuple
        link = self.view.getLinkDataFromForm()
        #  display confirmation
        response = messagebox.askyesno('Confirm Add Entry', f'About to add a NEW ENTRY consisting of values:\n'
                                         f'Site: {link.site_name}\n'
                                         f'Username: {link.username}\n'
                                         f'Link: {link.url}\n'
                                         f'Note: {link.note}\n'
                                         f'Password: {link.password}\n'
                                         f'Security: {link.security}\n'
                                         f'Email: {link.email}\n'
                                         f'For USER: {self.model.principal.email}\n'
                                                    f'YES saves data.  NO clears form.')

        if response:  # if yes
            # TODO:  does the entry already exist?  Is there already an account with the same site_name?
            try:
                #  saveLink returns the id of the last record, use to set currentEntryId
                lastRowId = self.dao.saveLink(link, self.model.principal.id)
                #  set currentEntryId -- used to track which link entry has the focus (is current)
                self.model.currentEntryId = lastRowId
            except TypeError:
                messagebox.showerror('Database Error', 'Could not add entry\nSee Marc.')
            else:
                messagebox.showinfo('Add Success', 'New entry added to database.')
                #  make listbox reflect the new entry
                self.model.links = self.dao.getLinks(self.model.principal.id)
                self.view.clearListBox()
                self.view.populateSiteListBox()
        else:  # if no
            self.view.clearForm()

    #  runs when user clicks 'Update Entry', updates an entry in the database
    def updateLink(self):
        link = self.view.getLinkDataFromForm()
        try:
            print('update CID: ', self.model.currentEntryId)
            # self.dao.updateLink(link)
            self.dao.updateLink(link)
        except TypeError:
            messagebox.showerror('Error Updating', 'Unable to write to the database.\nSee Marc.')
        else:
            messagebox.showinfo('Update Success', f'{link.site_name} updated successfully!')
            #  update the list of links, self.model.links, and reflect in GUI
            self.updateLinksForCurrentUser()

    #  runs when user clicks 'Delete'
    def deleteLink(self):
        #  get the item from the listbox
        item = self.view.siteListBoxFrame.siteListBox.get(self.view.siteListBoxFrame.siteListBox.curselection())
        #  confirm deletion
        response = messagebox.askquestion('Delete Item', f'Delete {item}?')
        if response == 'yes':
            try:
                self.dao.deleteLink(self.model.currentEntryId)
            except Error:
                messagebox.showerror('Error', f'Account: {item} was NOT deleted.\n'
                                              f'For technical support email:  marcholman9323@gmail.com.')
            else:
                messagebox.showinfo('Item Deleted', f'Account: {item} has been deleted.')
                #  update self.model.links, reflect changes in the GUI
                self.updateLinksForCurrentUser()
                self.view.clearForm()

    #  updates the list of links, self.model.links, for the current user, clears/populates listbox
    def updateLinksForCurrentUser(self):
        self.model.links = self.dao.getLinks(self.model.principal.id)
        self.view.clearListBox()
        self.view.populateSiteListBox()

    #  populates the form for entering web accounts
    def populateSiteEntryForm(self, linkData):
        self.view.populateSiteEntryForm(linkData)

    #  runs when user selects an item inside the list box
    def onListBoxSelect(self, event):
        #  populate the add/update form
        w = event.widget
        idx = int(w.curselection()[0])
        value = str(w.get(idx))
        linkData = self.dao.getLinkBySiteName(value)  # names must be unique
        self.model.currentEntryId = linkData.id
        print('onlistbox select - currentEntryId: ', self.model.currentEntryId)
        self.populateSiteEntryForm(linkData)

    #  generate a text file report containing all of a users data
    def printReport(self):
            self.dao.printReport(self.model.principal.email, self.model.links)
            messagebox.showinfo('SUCCESS!', 'To view the report open text file: password-report.txt')

    #  uses webbrowser module to open local html help file
    def help(self):
        wb.open("pwm-help.html")

    #  use a regular expression to test if a valid email address was entered
    def checkEmail(self, email):
        regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        if re.search(regex, email):
            return True
        return False

    #  on exit close connection and destroy root
    def exit(self):
        self.dao.closeConnection()
        self.root.destroy()

    #  runs the GUI and application
    def run(self):
        self.view.pack()
        self.root.mainloop()


#  starts the application
if __name__ == '__main__':
    Controller().run()

