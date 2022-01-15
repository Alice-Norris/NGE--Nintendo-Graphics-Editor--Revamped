import os
from nge_librarian import Librarian
import re

#saves NGE files
def write_file_data(directory, file):
    shelf = the_librarian.request_shelf() #get shelf from library, which cont
    if (os.path.exists(directory)):
        file_to_write = open(directory + file, 'wb')
        print(shelf.name)
        file_to_write.write(bytes('\x1C' + shelf.name, encoding = 'utf-8'))
        for book in shelf.book_list:
            file_to_write.write(bytes('\x1D' + book.name, encoding = 'utf-8'))
            for sheet in book.sheet_list:
                file_to_write.write(bytes('\x1E' + sheet.name, encoding = 'utf-8'))
                for character in sheet.char_list:
                    file_to_write.write(bytes('\x1F', encoding = 'utf-8'))
                    file_to_write.write(bytes([character.obj_num]))   
                    file_to_write.write(bytes(character.name + '\x10', encoding = 'utf-8'))
                    for pixel in character.data:
                        file_to_write.write(bytes([pixel]))
                    file_to_write.write(bytes('\x1F', encoding = 'utf-8'))
                file_to_write.write(bytes('\x1E', encoding = 'utf-8'))
            file_to_write.write(bytes('\x1D', encoding = 'utf-8'))
        file_to_write.write(bytes('\x1C', encoding = 'utf-8'))
        file_to_write.close()

def read_file_data(directory, file):
    dataReader = open("../test.nge", "rb") #open data file
    data = bytearray(dataReader.read()) #create bytearray from datafile
    data = data.strip(b'\x1C') #strip shelf delimiters from data
    shelf_title_end = data.find(b'\x1D') #get shelf name 
    shelf_name, data = data[:shelf_title_end], data[shelf_title_end:]
    shelf = Shelf(shelf_name) #create shelf object

    #while loop to be broken
    while True:
        book_end = data.find(b'\x1F\x1E\x1D')
        if book_end == -1:
            break
        else:
            raw_book = data[:book_end+3] #store entire raw book data into variable
            data = data[book_end+3:] #store remaining data in data, cutting off current book.
            book_title_end = raw_book.find(b'\x1E') #find index of sheet delimiter (1E)
            #assign book_title the decoded string of the book title bytes, assign book_data the rest of the data
            book_title, book_data = raw_book[1:book_title_end].decode(), raw_book[book_title_end:-1]
            book = Book(book_title, book_data) #create book using extracted book_title, pass data to book constructor
            shelf.book_list.append(book) #append book instance to shelf.

#called by either clicking the "New..." option from the file menu, 
# and when starting the program. must be passed the program's librarian instance
def nge_new(librarian):
    librarian.add_book('unnamed')
    librarian.request_book('unnamed')
    librarian.add_sheet('unnamed')
    librarian.request_sheet('unnamed')
    librarian.request_char_list()

def nge_open():
    pass

def nge_save():
    pass

#def create_bitmap(char):
    