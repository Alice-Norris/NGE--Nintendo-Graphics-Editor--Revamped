def character_to_hex(character):
    first_byte = ""
    second_byte = ""
    hexit_1 = ""
    hexit_2 = ""
    char_hex = ""
    pixel_counter = 0
    for pixel in character:
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
            print(convert_bin_string_to_hexit(hexit_1))
            first_byte += convert_bin_string_to_hexit(hexit_1)
            if(len(first_byte) == 2):
                char_hex += first_byte
                first_byte = ""
            print(convert_bin_string_to_hexit(hexit_2))
            second_byte += convert_bin_string_to_hexit(hexit_2)
            if(len(second_byte) == 2):
                char_hex += second_byte
                second_byte = ""
            hexit_1 = ""
            hexit_2 = ""
            pixel_counter = 0
    print(char_hex)

def convert_bin_string_to_hexit(hexit):
    hexit = hex(int(hexit, 2))[2]
    return hexit

character = [2, 2, 2, 2, 3, 3, 3, 3, 2, 2, 2, 2, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 3, 3, 2, 2, 2, 2, 2, 2, 3, 3, 2, 2, 2, 2, 2, 2, 3, 3, 2, 2, 2, 2, 2, 2, 3, 3, 2, 2, 2, 2, 3, 3, 2, 2, 2, 2, 2, 2, 3, 3, 2, 2]
character_to_hex(character)