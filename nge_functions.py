from nge_const import NGE_WHITE, NGE_LT_GRAY, NGE_DK_GRAY, NGE_BLACK, COLOR_DICT
from tkinter import PhotoImage
####                    NGE FUNCTIONS                   ####
# This section contains the functions that power the NGE   #
############################################################

def character_to_hex(character):
    first_byte = ""
    second_byte = ""
    hexit_1 = ""
    hexit_2 = ""
    char_hex = ""
    pixel_counter = 0
    print(character.data)
    for pixel in character.data:
        pixel_counter += 1
        if pixel == 3:
            hexit_1 += "0"
            hexit_2 += "0"
        if pixel == 2:
            hexit_1 += "1"
            hexit_2 += "0"
        if pixel == 1:
            hexit_1 += "0"
            hexit_2 += "1"
        if pixel == 0:
            hexit_1 += "1"
            hexit_2 += "1"
        if pixel_counter == 4:
            first_byte += convert_bin_string_to_hexit(hexit_1)
            if(len(first_byte) == 2):
                char_hex += first_byte
                first_byte = ""
            second_byte += convert_bin_string_to_hexit(hexit_2)
            if(len(second_byte) == 2):
                char_hex += second_byte
                second_byte = ""
            hexit_1 = ""
            hexit_2 = ""
            pixel_counter = 0
    return char_hex
        
def convert_bin_string_to_hexit(hexit):
    hexit = hex(int(hexit, 2))[2]
    return hexit           
    
def character_row_to_hex(character, row_num):
    first_byte = ""
    second_byte = ""
    char_hex = ""
    for pixel in character.data[row_num]:
        if pixel == NGE_WHITE:
            first_byte += "0"
            second_byte += "0"
        if pixel == NGE_LT_GRAY:
            first_byte += "1"
            second_byte += "0"
        if pixel == NGE_DK_GRAY:
            first_byte += "0"
            second_byte += "1"
        if pixel == NGE_BLACK:
            first_byte += "1"
            second_byte += "1"
    hex_row = first_byte + second_byte
    char_hex += (hex(int(hex_row, 2))[2:6].zfill(4))

def createCharacterImage(character):
    imageData = 'P6\n#wat\n8\n8\n189\n'
    for pixel in character.data:
        imageData +=  ' ' + str(63*pixel)
    imageData += ' '
    print(imageData)
    return PhotoImage(name='test', data=imageData, format='PPM')