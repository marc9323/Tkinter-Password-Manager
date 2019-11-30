
class Model:
    """
    Data Model for the Tkinter Password Manager Application Project
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
        return self.__links

    @links.setter
    def links(self, val):
        self.__links = val

