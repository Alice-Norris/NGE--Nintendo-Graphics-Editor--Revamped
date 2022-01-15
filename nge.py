from nge_classes import Character, Sheet, Book, Shelf
from userInterface import nge_interface
from nge_librarian import Librarian
class NGE:
    interface = None
    the_librarian = Librarian()
    index = None

    def __init__(cls):
        #cls.the_librarian = Librarian()
        cls.interface = nge_interface(cls, cls.index)

#create instance of nge_interface and NGE
NGE = NGE()
NGE.interface.mainloop()
#create instance of GUI, change title, begin program loop

