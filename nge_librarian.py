from nge_classes import Shelf, Book, Sheet, Character
####                    THE LIBRARIAN                    ####
# The Librarian is the class that manages all other objects #
# Only one should be created, and only one should be used   #
# Hands data to the user interface upon request.            #
#############################################################

class Librarian:
    __instance = None
    
    def __init__(self):
        if Librarian.__instance != None: #check if another Librarian instance already exists.
            raise Exception("Only one librarian allowed. You've done something wrong.")
        else:
            Librarian.__instance = self
            self.__shelf = Shelf('unnamed')
            self.__current_book = None
            self.__current_sheet = None
            self.__current_char = None
            


    #takes sheet name as an argument, checks to make sure the sheet name does not already
    #exist, and then creates and appends it to the book.
    def add_sheet(self, sheet_name): 
        sheet_list = self.__current_book.sheet_list
        print(sheet_list)
        for sheet in sheet_list:
            if sheet.name == sheet:
                print("This page already exists!")
                sheet_name += '1'
        sheet_list.append(Sheet(sheet_name))
        #print(sheet_name, "added")
        return sheet_list

    def remove_sheet(self, sheet_name): #takes a sheet name as an argument
        #deletes the sheet object and its sheetname from the dictionary
        sheet_list = self.__current_book.sheet_list
        for sheet in sheet_list:
            if sheet.name == sheet_name:
                sheet_list.remove(sheet)
                print(sheet_name, "deleted!")
            else:
                print("That sheet doesn't exist!")

    def request_current_sheet(self): #returns the current sheet from the current book to the caller
        return self.__current_sheet


    def request_sheet(self, sheet_name): #requests a sheet from the current book, making it "active."
        current_sheet_list = self.__current_book.sheet_list
        for sheet in current_sheet_list:
            if sheet.name == sheet_name:
                self.__current_sheet = sheet

    #takes a book name as an argument, checks to ensure a book doesn't already exist
    #with that name, and creates it, appending it to the end of the dictionary.
    def add_book(self, book_name):
        book_list = self.__shelf.book_list
        for book in book_list:
            if book_name == book.name:
                print("This book already exists!")
                break
        book_list.append(Book(book_name))
        return book_list[-1]

    #Takes book name as an argument, deleting the book instance
    # and its name from the book dictionary.
    def remove_book(self, book_name):
        book_list = self.__shelf.book_list
        for book in book_list:
            if book.name == book_name:
                book_list.remove(book)
                print(book_name, "deleted!")
            else:
                print("That sheet doesn't exist!")

    #returns the currently opened book instance to the caller
    def request_current_book(self):
        return self.__current_book

    #requests a book from the currently opened shelf.
    #This replaces the current book, making it "active"
    def request_book(self, book_name):
        current_book_list = self.__shelf.book_list
        for book in current_book_list:
            if book.name == book_name:
                self.__current_book = book
            else:
                print("This book doesn't exist!")

    #returns a shelf of books
    def request_shelf(self):
        return self.__shelf.name

    #returns a list of all books in current shelf.
    def request_book_list(self):
        return self.__shelf.book_list

    #returns a list of all sheets in the current book.
    def request_sheet_list(self):
        return self.__current_book.sheet_list

    #returns a list of characters from the current sheet
    def request_char_list(self):
        return self.__current_sheet.char_list

