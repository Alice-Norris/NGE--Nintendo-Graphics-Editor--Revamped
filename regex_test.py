import re #import regex module for searching with regex
import codecs #import codecs module for decoding bytes
from nge_classes import Character, Sheet, Book, Shelf #import classes to create objects

dataReader = open("../test.nge", "rb") #open data file
data = bytearray(dataReader.read()) #create bytearray from datafile
data = data.strip(b'\x1C') #strip shelf delimiters from data
shelf_title_end = data.find(b'\x1D') #get shelf name 
shelf_name, data = data[:shelf_title_end], data[shelf_title_end:]
shelf = Shelf(shelf_name) #create shelf object


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
        






























# #shelf_name_regex_pattern = b"\x1C{1}{\x1D".format(book_name)
# shelf_name_regex = re.compile(b"\x1C.*\x1D")


# book_name_regex = re.compile(b"\x1D(\w*)\x1E")
# #shelf_name_regex_pattern = b"\x1D{1}{\x1E".format(book_name)
# sheet_name_regex = re.compile(b"\x1E(\w*)\x1F")
# char_header_regex = re.compile(b"\x1E(\w*)\x10")

# book_data_regex = re.compile(b"\x1D.+\x1F\x1E\x1D")
# sheet_data = re.compile(b"\x1F.*\x1F\x1E")
# char_data = re.compile(b"\x10([\x00-\x03]{64})\x1F")
# current_section = dataReader.read()

# book_list = []

# book_titles = book_name_regex.findall(current_section)

# for book_name in book_titles:
#     book_list.append(Book(book_name.decode))
#     book_data = re.search(b"\x1D" + book_name + b"\x1E.*\x1F\x1E\x1D", current_section)
#     print(book_data)
