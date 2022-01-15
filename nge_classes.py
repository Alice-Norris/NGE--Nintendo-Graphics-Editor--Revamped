from nge_const import NGE_BLACK, NGE_DK_GRAY, NGE_LT_GRAY, NGE_WHITE
import re
####                     NGE CLASSES                    ####
# This section contains the classes for the NGE            #
############################################################
#this class creates tools with specified name and bitmap
class Tool:
    def __init__(self, name, cursor):
        self.tool_name = name
        self.tool_cursor = cursor

#this class is used to describe the character data for a single object
class Character: 
    def __init__(self, obj_num, name = "unnamed", charPixels = None):
        self.obj_num = obj_num #this should be a hex number
        self.data = [] #64 member list, used to store individual pixel information. Should be 0 to 3.
        self.name = name #character name
        #if the character data is of the appropriate length and exists,
        if charPixels != None and len(charPixels) == 64: 
            for digit in charPixels: #for each byte or digit in charPixels,
                self.data.append(int(digit)) #append the byte to character data, converted to base-10
        else:
            while (len(self.data) < 64):
                self.data.append(3)
    
    #used to turn character into bytes for saving
    def selfAsBytes(self):
        #create character header
        characterHeader = b'\x1F' + bytes(self.obj_num) + bytes(self.name) + 'x\10' 
        #empty byte string for pixel data
        characterPixels= b''
        #for each pixel in self.data,
        for pixel in self.data:
            #append the pixel's value (00-03) to the hex string.
            characterBytes += bytes(pixel)
        #return yourself
        return characterHeader + characterPixels + b'\x1F'

#this class holds "sheets" of characters. 
class Sheet:
    def __init__(self, sheet_name, sheetData = None):
        self.name = sheet_name #name of sheet
        self.char_list = [] #list used to store characters.
        
        #if sheetData is given,
        if sheetData != None:
            #create character list from data
            createCharListFromData(sheetData)
        else:
            char_num = 0
            while(len(self.char_list) <= 127):
                char = Character(char_num, sheet_name)
                self.char_list.append(char)
                char_num += 1
    
    def createCharListFromData(self, sheetData):
    #regex to find each character.
        char_regex = re.compile(b'(?:\x1F([\x00-\x7F])(\w+)\x10([\x00-\x03]{64})\x1F)')
        #store groups into list
        charMatches = char_regex.findall(sheetData)
        #for the character information (a tuple: char number, char name, char pixel data) in each group
        for charData in charMatches:
            #storing each member of the tuple into their respective variables
            charNum, charName, charPixels = charData
            #create a character using the data, to be handled by Character constructor
            #then, append the character to the Sheet's character list
            self.char_list.append(Character(charNum, charName, charPixels))

    def selfAsBytes(self):
        sheetHeader = b'\x1E' + bytes(self.name)
        sheetData = b''
        for character in self.char_list:
            sheetData += character.selfAsBytes()
        return sheetHeader + sheetData + b'\x1E'

class Book:
    def __init__(self, book_name, bookData = None):
        self.name = book_name #This string is the name of the book. Books hold sheets.
        self.sheet_list = [] #List to hold the book's sheet objects
        if bookData: #if book data is provided (from a file),
           buildSheetListFromData(bookData)

    def buildSheetListFromData(self, bookData):
        #find sheets using regex.
        sheet_regex = re.compile(b'\x1E.*\x1F[\x00-\x7F]{1}.*\x10.*[\x00-\x03]{1}\x1F\x1E') 
        #return list of matched sheet data
        sheet_matches = sheet_regex.findall(bookData)
        #for each sheet's data in the matches,
        for sheet in sheet_matches:
            #find index of first char delimiter (1F)
            sheet_title_end = sheet.find(b'\x1F')
            #assign sheet title the decoded string contained after the sheet delimiter (1E),
            #assign sheet data the sheet's character data
            sheet_title, sheet_data = sheet[1:sheet_title_end].decode(), sheet[sheet_title_end:-1]
            #create sheet with sheet title, supplying sheet data to be processed by Sheet's constructor
            self.sheet_list.append(Sheet(sheet_title, sheet_data))

    def selfAsBytes(self):
        bookHeader = b'\x1D' + self.name
        bookData = b''
        for sheet in self.sheet_list:
                sheet_data += sheet.selfAsBytes()
        return bookHeader + bookData + b'\x1D'

class Shelf:
    def __init__(self, shelf_name):
        self.name = shelf_name #This string is the name of the shelf, also the file name, and holds books.
        self.book_list = []