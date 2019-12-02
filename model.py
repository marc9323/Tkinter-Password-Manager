
from collections import namedtuple


#  namedtuple is a factory function which subclasses namedtuple.
#  instead of creating classes with no methods and all data attributes I
#  chose to use named tuples.
UserTuple = namedtuple('User', ['id', 'email', 'password'])
LinkTuple = namedtuple('Link', ['id', 'user_id', 'site_name', 'username', 'url', 'note', 'password', 'security', 'email'])

class Model:
    """
    Data Model for the Tkinter Password Manager Application Project.
    links = list of links for the current user
    currentEntryId = tracks the current entry for the site list box
    principal = current user
    """
    def __init__(self):
        self.__links = []
        self.__currentEntryId = 0
        self.__principal = None

    @property
    def currentEntryId(self):
        return self.__currentEntryId

    @currentEntryId.setter
    def currentEntryId(self, val):
        self.__currentEntryId = val

    @property
    def principal(self):
        return self.__principal

    @principal.setter
    def principal(self, val):
        self.__principal = val

    @property
    def links(self):
        #  keeps the list of links sorted
        #  the lambda acts as an anonymous function which simply returns link.site_name
        #  for the sort key - sort is in alphabetical order
        return sorted(self.__links, key=lambda link: link.site_name)

    @links.setter
    def links(self, val):
        self.__links = val

