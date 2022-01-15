from nge_functions import character_to_hex, character_row_to_hex, createCharacterImage #import functions from nge
from nge_const import NGE_BLACK, NGE_DK_GRAY, NGE_LT_GRAY, NGE_WHITE, COLOR_DICT, REVERSE_COLOR_DICT
from nge_files import write_file_data, read_file_data, nge_new, nge_open, nge_save
from tkinter import Menu, Canvas, Text, BitmapImage, PhotoImage, Button, Scrollbar, StringVar, TclError, Toplevel, ACTIVE, filedialog, ttk, messagebox
from tkinter.constants import *
from imageCreator import createPPM
from math import ceil, floor
from nge_classes import Tool
from random import randint

class nge_interface(ttk.Frame):
    #Constructor, calls functions to create GUI
    def __init__ (self, NGE, index, master=None):
        self.application = NGE
        self.the_librarian = self.application.the_librarian
        nge_new(self.the_librarian)
        self.current_char = 0
        self.file_directory = None
        self.filename = None
        self.saveable = False
        #style setup
        nge_style = ttk.Style()
        nge_style.theme_use('winnative')
        
        ttk.Frame.__init__(self, master, width=1024, height = 768, class_ = 'application_window')
        #setting top level window to a variable
        self.TLW = self.winfo_toplevel()
        self.grid()
        self.columnconfigure(0, minsize = 512)
        self.columnconfigure(1, minsize = 512)
        self.rowconfigure(0, minsize=384)
        self.rowconfigure(1, minsize=384)
        self.TLW.title("Nintendo Graphics Editor")
        #Creating menu along top of window
        self.create_menu(self.TLW)

        #creating tools
        self.Select = Tool('select', BitmapImage('@empty.xbm', foreground = 'black', background = 'white'))
        self.Pencil = Tool('pencil', BitmapImage('@PencilGray.cur', foreground = 'black', background = 'white'))
        self.Bucket = Tool('bucket', BitmapImage('@bucket.cur', foreground = 'black', background = 'white'))
        self.Eraser = Tool('eraser', BitmapImage('@Eraser.cur', foreground = 'black', background = 'white'))
        
        #create program variables
        self.active_book = StringVar()
        self.active_sheet = StringVar()
        self.active_char = StringVar()
        self.active_char_num = StringVar()
        self.entry_text = StringVar()
        self.current_tool = self.Select
        self.current_color = NGE_WHITE
        self.character_images = []
        #Creates different areas of the GUI
        self.organization_frames()
        self.sheet_area()    #populates sheet frame
        self.tile_area()     #populates tile frame
        self.tool_area()     #populates tool frame 
        self.color_area()    #populate color frame with available colors and current color tools
        self.tree_area()     #populate tree area
        self.text_area()

        #create grids in sheet and character canvases
        self.create_canvas_grid(self.tile_display)
    ###################
    ###GUI FUNCTIONS###
    ###################

    #highlights text in text area to show hex code of current character
    def highlight_text(self):
        self.hex_display.tag_delete('current_char')
        current_char_num = int(self.active_char_num.get())
        self.hex_display.tag_add('current_char', str(current_char_num + 2) + '.0', str(current_char_num + 2) + '.53')
        self.hex_display.tag_config('current_char', background = '#c0c0c0')


    def create_canvas_grid(self, canvas):
        row = 0
        column = 0
        height = int(canvas.cget('height'))
        width = int(canvas.cget('width'))
        canvas.create_line(width, 0, width, height+1)
        while (column <= floor(width / 33)):
            canvas.create_line(row*33, 0, row*33, height)
            row += 1
            if (row == floor(width / 33)):
                canvas.create_line(0, column * 33, width, column * 33)
                row= 0
                column += 1
        
    def text_area_setup(self):
        text_area_width = 53
        hex_loc = 0
        header = "       0"
        line_num = 2
        while len(header) < text_area_width:
            header += "  " + hex(hex_loc + 1)[2:4]
            hex_loc += 1
        self.hex_display.insert('1.0', header + '\n')
        for character in self.current_sheet.char_list:
            hex_line = ""
            line_index = 5
            byte_num = 0
            index = str(line_num) + "." + str(line_index)
            character_hex = character_to_hex(character)
            self.hex_display.insert(str(line_num) + ".0", str(hex(character.obj_num)).rjust(4) + "|")
            while(byte_num < 32):
                if(byte_num < 32):
                    hex_line += " " + (character_hex[byte_num : byte_num + 2])
                elif (byte_num == 32):
                    hex_line += (character_hex[byte_num : byte_num + 2])
                byte_num += 2
            self.hex_display.insert(index, hex_line + "\n")
            line_num += 1
        self.highlight_text()

    def create_tile_display_pixels(self):
        row = 0
        column = 0
        while column < 8:
            x_1 = row * 33 + 1
            y_1 = column * 33 + 1
            x_2 = x_1 + 31
            y_2 = y_1 + 31
            self.tile_display.create_rectangle(x_1, y_1, x_2, y_2, fill = self.current_color, outline = self.current_color)
            row += 1
            if row == 8:
                row = 0
                column += 1

    def create_character_images(self):
        for character in self.the_librarian.request_char_list():
            for pos, pixel in enumerate(character.data):
                character.data[pos] = randint(0, 3)
        for character in self.the_librarian.request_char_list():
            imageHeader = bytearray("P6\n8 8\n3\n", "utf-8")
            imagePixels = bytearray(192)
            for pos, pixel in enumerate(character.data):
                imagePixels[pos*3] = imagePixels[pos*3+1] = imagePixels[pos*3+2] = pixel
            image = PhotoImage(name = character.obj_num, data = bytes(imageHeader + imagePixels), format = "PPM")
            image = image.zoom(4, 4)
            self.character_images.append(image)

    def create_sheet_display_images(self):
        self.create_character_images()
        for pos, image in enumerate(self.character_images):
            char_num = pos
            xCoord = floor(char_num % 16) * 33
            yCoord = floor(char_num / 16) * 33  
            self.sheet_display.create_image(self.sheet_display.canvasx(xCoord), self.sheet_display.canvasy(yCoord), image=image, anchor = 'nw')
            
    def update_character_image(self):
        imageHeader = bytearray('P6\n8 8\n3\n', 'utf-8')
        imagePixels = bytearray(192)
        for pos, pixel in enumerate(self.current_char.data):
            print(self.current_char.data)
            imagePixels[pos*3] = imagePixels[pos*3+1] = imagePixels[pos*3+2] = pixel
        image = PhotoImage(name = self.current_char.obj_num, data = bytes(imageHeader+imagePixels), format = "PPM")
        image = image.zoom(4, 4)
        self.character_images[self.current_char.obj_num] = image
        self.sheet_display.delete(self.current_char.obj_num + 1)
        xCoord = self.sheet_display.itemcget(self.current_char.obj_num + 1, "x")
        yCoord = self.sheet_display.itemcget(self.current_char.obj_num + 1, "y")
        print(xCoord, yCoord)
        self.sheet_display.create_image(self.sheet_display.canvasx(xCoord), self.sheet_display.canvasy(yCoord), image=image)
        

    def update_tile_display_pixels(self):
        if(self.current_char):
            self.active_char.set(self.current_char.name)
            character_pixels = self.current_char.data
            for index, pixel in enumerate(character_pixels):
                self.tile_display.itemconfig(index + 1, fill = REVERSE_COLOR_DICT[pixel])

    def update_text_area(self):
        character = self.current_char
        character_data = self.current_char.data
        hex_line = ""
        byte_num = 0
        start_index = str(character.obj_num + 2) + ".5"
        end_index = str(character.obj_num + 2) + ".53"
        character_hex = character_to_hex(character)
        while(byte_num < 32):
            if(byte_num < 32):
                hex_line += " " + (character_hex[byte_num : byte_num + 2])
            elif (byte_num == 32):
                hex_line += (character_hex[byte_num : byte_num + 2])
            byte_num += 2
        self.hex_display.replace(start_index, end_index, hex_line)
        self.hex_display.tag_config('current_char', background = '#c0c0c0')

    def tree_view_update(self):
        shelf_name = self.the_librarian.request_shelf()
        book_list = self.the_librarian.request_book_list()
        self.tree_view.insert('', 0, iid = shelf_name, tags = 'shelf', text = shelf_name)
        for book in book_list:
            book_name = book.name
            page_count = len(book.sheet_list)
            self.tree_view.insert(shelf_name, 'end', iid = 'book_'+book_name, tags = 'book', values = (book_name, '', page_count))
            for sheet in book.sheet_list:
                self.tree_view.insert('book_'+book_name, 'end', iid = 'sheet_' + sheet.name, tags = 'sheet', values=('', sheet.name, ''))


    def change_active(self, book_name, sheet_name = None):
        self.current_book = self.the_librarian.request_book(book_name)
        self.active_book.set(book_name)
        if sheet_name:
            self.current_sheet = self.the_librarian.request_sheet(sheet_name)
            self.current_char = self.the_librarian.request_char_list[0]
            print(self.current_char)
            self.active_sheet.set(sheet_name)
            self.text_area_setup()
        self.update_tile_display_pixels()


    #######################
    ###HANDLER FUNCTIONS###
    #######################
    # def save_as_dialog(self):
    #     if self.filename:
    #         self.file_menu.add_command(label = 'Save')
    #     elif not self.filename:
    #         print(event.widget.dir())
    #         file_name_and_dir = ''
    #     if action == 'open':
    #         filedialog.askopenfilename            
    #     elif action == 'save_as' and self.filename:
    #         file_name_and_dir = filedialog.asksaveasfilename(defaultextension = '.nge', filetypes = [("NGE file", "*.nge")], initialfile = self.filename)
    #     elif action == 'save_as':
    #         file_name_and_dir = filedialog.asksaveasfilename(defaultextension = '.nge', filetypes = [("NGE file", "*.nge")])
        
        # print(file_name_and_dir)
        # last_slash = file_name_and_dir.rfind("/")
        # self.filename = file_name_and_dir[last_slash+1:]
        # self.file_directory = file_name_and_dir[0:last_slash]

        # write_file_data(self.file_directory, self.filename, self.index, "test")

    def name_dialog_action(self, event):
        if event.widget.cget(name = 'add_book'):
            self.the_librarian.add_book(self.input_name)

    def color_swatch_clicked(self, event):
        self.current_color_swatch.configure(bg = event.widget.cget('bg'))
        self.current_color = event.widget.cget('bg')

    def tool_button_clicked(self, event):
        clicked_tool = event.widget.winfo_name()
        if (clicked_tool == 'select'):
            self.current_tool = self.Select
        elif (clicked_tool == 'pencil'):
            self.current_tool = self.Pencil
        elif (clicked_tool == 'eraser'):
            self.current_tool = self.Eraser
        elif (clicked_tool == 'bucket'):
            self.current_tool = self.Bucket

    #detects when the tile display is clicked and applies the appropriate action given a selected tool
    def tile_display_clicked(self, event):     
        click_x = self.tile_display.canvasx(event.x)
        click_y = self.tile_display.canvasy(event.y)
        clicked_rectangle = self.tile_display.find_closest(click_x, click_y)
        if self.current_tool == self.Pencil:
            color = self.current_color
            self.tile_display.itemconfigure(clicked_rectangle, fill = self.current_color)
            print(clicked_rectangle)
            self.current_char.data[clicked_rectangle[0] - 1] = COLOR_DICT[self.current_color]
            self.update_character_image()
        if self.current_tool == self.Eraser:
            self.tile_display.itemconfigure(clicked_rectangle, fill = NGE_WHITE)
            self.current_char.data[clicked_rectangle - 1] = 0
        self.update_text_area()
        self.highlight_text()
    
    def sheet_display_clicked(self, event):
        click_x = self.sheet_display.canvasx(event.x)
        click_y = self.sheet_display.canvasy(event.y)
        character_number = floor(click_x / 33) + floor(click_y / 33)*16
        self.current_char = self.the_librarian.request_char_list()[character_number]
        self.active_char.set(self.current_char.name)
        self.active_char_num.set(self.current_char.obj_num)
        self.tile_display_label.config(text = "Object Number: " + str(character_number))
        self.hex_display.see(str(character_number + 2) + '.0')
        self.highlight_text()
        self.update_tile_display_pixels()
        tile_display_string = "Object " + str(character_number) + ": "
        self.tile_display_label.config(text = tile_display_string)

    def tile_name_enter(self, event):
        self.current_char.name = self.entry_text.get()
        

    def make_active(self, event):
        item_iid = self.tree_view.selection()[0]
        #item_type = self.tree_view.item(item_iid, 'tags')[0]
        item_type = self.tree_view.item(item_iid, 'tags')
        if(item_type == 'book'):
            book_name = self.tree_view.item(item_iid, 'values')[0]
            if (len(self.tree_view.get_children([item_iid])) != 0):
                first_sheet = self.tree_view.get_children([item_iid])[0]
                sheet_name = self.tree_view.item(first_sheet, option = 'values')[1]
                self.change_active(book_name, sheet_name)
            else:
                self.change_active(book_name)

        elif (item_type == 'sheet'):
            parent_iid = self.tree_view.parent(item_iid)
            book_name = self.tree_view.item(parent_iid, option = 'values')[0]
            sheet_name = self.tree_view.item(item_iid, option = 'values')[1]
            self.change_active(book_name, sheet_name)


    def add_dialog(self, event):
        self.input_name = StringVar()
        widget_name = event.widget._name
        if widget_name == "add_sheet" and not self.the_librarian.request_current_book:
            messagebox.showerror("No Books", "There are no books available to add a sheet too! Open a file or add a book!")
        
        self.name_dialog = Toplevel(width = 512, height = 256, padx = 32, pady = 32)
        self.instructions_label = ttk.Label(self.name_dialog)
        self.instructions_label.grid(row = 0, column = 1, columnspan = 2)
        self.name_entry_label = ttk.Label(self.name_dialog)

        self.ok_button = ttk.Button(self.name_dialog, text = 'Ok', command = self.clean_up_dialog)
        self.ok_button.grid(row = 2, column = 1, sticky = W)
        self.cancel_button = ttk.Button(self.name_dialog, text = 'Cancel')
        self.cancel_button.grid(row = 2, column = 2, sticky = E)
        
        if widget_name == "add_book":
            self.name_dialog.title = 'Add Book'
            self.input_name.set(self.the_librarian.request_current_book().name)
            self.instructions_label.config(text = 'Please enter a name for the new book:')
            self.name_entry_label.config(text = 'Book Name: "')
            self.name_entry_label.grid(row = 1, column = 1)
            self.name_entry_box = ttk.Entry(self.name_dialog, width = 24, textvariable = self.input_name)
            self.name_entry_box.grid(row = 1, column = 2)
            self.ok_button.bind('<ButtonRelease-1>', lambda discard: self.the_librarian.add_book(self.input_name.get()))
        
        elif widget_name == "add_sheet":
            book_name = self.the_librarian.request_current_book().name
            self.name_dialog.title = 'Add Sheet'
            self.input_name.set(book_name)
            self.instructions_label.config(text = 'Please enter a name for the new sheet:')
            self.name_entry_label.config(text = 'Sheet Name: ')
            self.name_entry_label.grid(row = 1, column = 1)
            self.name_entry_box = ttk.Entry(self.name_dialog, width = 24, textvariable = self.input_name)
            self.name_entry_box.grid(row = 1, column = 2)
            self.ok_button.bind('<ButtonRelease-1>', lambda discard: self.the_librarian.add_sheet(self.input_name.get()))          
        
    def remove_dialog(self, event):
        widget_name = event.widget._name
        print(widget_name)
        if widget_name == "remove_book" and self.current_book== None:
            messagebox.showerror("No Books", "There are currently no books available. Open a file or add a book!")
            return        
        elif widget_name == "remove_sheet" and self.current_sheet == None:
            messagebox.showerror("No Sheets", "There are currently no sheets available. Open a file or add a sheet!")
            return
        self.name_dialog = Toplevel(width = 512, height = 256, padx = 32, pady = 32)
        self.instructions_label = ttk.Label(self.name_dialog)
        self.instructions_label.grid(row = 0, column = 1, columnspan = 2)
        self.ok_button = ttk.Button(self.name_dialog, text = 'Ok', command = self.clean_up_dialog)
        self.ok_button.grid(row = 2, column = 1, sticky = W)
        self.cancel_button = ttk.Button(self.name_dialog, text = 'Cancel')
        self.cancel_button.grid(row = 2, column = 2, sticky = E)        
        if widget_name == "remove_book":
            book_name = self.active_book.get()
            self.name_dialog.title = 'Remove Book'
            self.instructions_label.config(text = 'Are you sure you want to remove ' + self.active_book.get())
            self.ok_button.bind('ButtonRelease-1>', lambda: self.the_librarian.remove_book(book_name))
        elif widget_name == "remove_sheet":
            sheet_name = self.active_sheet.get()
            self.name_dialog.title = 'Remove Sheet'
            self.instructions_label.config(text = 'Are you sure you want to remove ' + self.active_sheet.get())
            self.ok_button.bind('ButtonRelease-1>', lambda: self.the_librarian.remove_sheet(sheet_name))
        self.name_dialog.columnconfigure(0, weight = 1)
        self.name_dialog.columnconfigure(3, weight = 1)
        
    def clean_up_dialog(self):
        self.name_dialog.destroy()
        self.tree_view_update()

    ###########################
    ###END HANDLER FUNCTIONS###
    ###########################       


    ######################
    ###WIDGET FUNCTIONS###
    ######################
    def create_menu(self, TLW):
        #Creating menu along top of window
        self.menu_bar = Menu(TLW)
        TLW['menu'] = self.menu_bar

        #creates file menu
        self.file_menu = Menu(self.menu_bar, tearoff = 0)
        
        self.sheets_menu = Menu(self.file_menu, tearoff=0)
        
        self.menu_bar.add_cascade(label = 'File', menu=self.file_menu)
        
        self.file_menu.add_command(label = 'New', command = nge_new)
        self.file_menu.add_command(label = 'Open...', command = nge_open)
        self.file_menu.add_command(label = 'Save', command = nge_save, state = 'disabled')
        self.file_menu.add_command(label = 'Save As...', state = 'disabled')
        self.file_menu.add_command(label = 'Import image...',)
        self.file_menu.add_command(label = "Quit", command=self.quit)

        #creates edit menu, menu items, and defines their commands
        self.edit_menu = Menu(self.menu_bar, tearoff = 0)
        self.edit_menu.add_command(label = 'Preferences...')

        self.menu_bar.add_cascade(label = 'Edit', menu=self.edit_menu)

        #creates help menu, menu items, and defines their commands
        self.help_menu = Menu(self.menu_bar, tearoff = 0)
        self.menu_bar.add_cascade(label = 'Help', menu=self.help_menu)
        self.help_menu.add_command(label = 'About')

    def organization_frames(self):
        self.top_left_frame = ttk.Frame(self)
        self.top_left_frame.grid(row = 0, column = 0, sticky = N+S+E+W)
        self.bottom_left_frame = ttk.Frame(self)
        self.bottom_left_frame.grid(row = 1, column = 0, sticky = N+S+E+W)
        self.top_right_frame = ttk.Frame(self)
        self.top_right_frame.grid(row = 0, column = 1, sticky = N+S+E+W)
        self.bottom_right_frame = ttk.Frame(self)
        self.bottom_right_frame.grid(row=1, column = 1, sticky = N+S+E+W)

    def sheet_area(self):
        self.sheet_frame = ttk.LabelFrame(self.top_left_frame, 
                                          labelanchor = 's', 
                                          borderwidth = 2, 
                                          text = "Sheet View")

        self.sheet_frame.grid(row = 0, 
                              column = 0, 
                              in_ = self.top_left_frame, 
                              padx =5, pady = 5, 
                              ipadx = 5, ipady = 5)

        self.sheet_frame.grid_columnconfigure(0, weight = 1)

        self.sheet_frame.grid_columnconfigure(3, weight = 1)
        
        self.sheet_frame.grid_rowconfigure(0, weight = 1)

        self.sheet_frame.grid_rowconfigure(3, weight = 1)
        
        self.sheet_display = Canvas(self.sheet_frame, 
                                    height=264, 
                                    width=528, 
                                    bg='#FFFFFF', 
                                    border=0, 
                                    borderwidth = 0, 
                                    highlightthickness=0, 
                                    cursor='tcross')
        self.sheet_display.grid(in_ = self.sheet_frame, 
                                row = 1, 
                                column = 1, 
                                ipadx = 1, 
                                ipady = 1, 
                                columnspan = 2)
        self.sheet_display.bind('<ButtonRelease-1>', self.sheet_display_clicked)
        self.sheet_display_label = ttk.Label(self.sheet_frame, text = "Sheet:")
        self.sheet_display_label.grid(row = 2, column = 1, in_ = self.sheet_frame, sticky = E)
        
        self.sheet_name_box = ttk.Entry(self.sheet_frame, textvariable = self.active_sheet)
        self.sheet_name_box.bind('<Return>', self.tile_name_enter)
        self.sheet_name_box.grid(row = 2, column = 2, in_ = self.sheet_frame, sticky = W)

        self.current_sheet = self.the_librarian.request_sheet("unnamed")

        self.create_sheet_display_images()
        
    def tile_area(self):
        #create area label0
        self.tile_frame = ttk.LabelFrame(self.top_right_frame, labelanchor = 's', borderwidth = 2, text = 'Character View')
        self.tile_frame.grid(row = 0, column = 1, in_ = self.top_right_frame, padx = 5, pady = 5)
        self.tile_frame.grid_columnconfigure(0, weight = 1)
        self.tile_frame.grid_columnconfigure(3, weight = 1)
        self.tile_frame.grid_rowconfigure(0, weight = 1)
        self.tile_frame.grid_rowconfigure(3, weight = 1)
        
        #create canvas to display tile
        self.tile_display = Canvas(self.tile_frame, height = 264, width = 264, bg = '#FFFFFF', borderwidth = 0, highlightthickness=0)
        self.tile_display.bind('<ButtonRelease-1>', self.tile_display_clicked) #bind canvas to 
        self.tile_display.grid(row = 1, column = 1, columnspan = 2, in_=self.tile_frame, padx = 5, pady = 5, ipadx = 1, ipady = 1)
        self.create_tile_display_pixels()

        #create label to indicate current object
        current_char_number = self.active_char_num.get()
        tile_display_string = "Object " + current_char_number + ": "
        self.tile_display_label = ttk.Label(self.tile_frame, text = tile_display_string)
        self.tile_display_label.grid(row = 2, column = 1, in_ = self.tile_frame, sticky = E)

        self.tile_name_box = ttk.Entry(self.tile_frame, textvariable = self.active_char)
        self.tile_name_box.bind('<Return>', self.tile_name_enter)
        self.tile_name_box.grid(row = 2, column = 2, in_ = self.tile_frame, sticky = W)

    def tool_area(self):
        self.tool_frame = ttk.LabelFrame(self.top_right_frame, labelanchor = 's', borderwidth = 2, text = 'Tools')
        self.tool_frame.grid(row = 0, column = 3, in_ = self.top_right_frame, sticky = N+S)

        self.select_button = Button(self.tool_frame, name = self.Select.tool_name, bitmap = '@select.xbm', width = 64, height = 64)
        self.select_button.bind('<ButtonRelease-1>', self.tool_button_clicked)
        self.select_button.grid(in_ = self.tool_frame)

        self.pencil_button = Button(self.tool_frame, name = self.Pencil.tool_name, bitmap = '@pencil.xbm', width = 64, height = 64)
        self.pencil_button.bind('<ButtonRelease-1>', self.tool_button_clicked)
        self.pencil_button.grid(in_ = self.tool_frame)
        
        self.eraser_button = Button(self.tool_frame, name = self.Eraser.tool_name, bitmap = '@eraser.xbm', width = 64, height = 64)
        self.eraser_button.bind('<ButtonRelease-1>', self.tool_button_clicked)
        self.eraser_button.grid(in_ = self.tool_frame)
        
        self.bucket_button = Button(self.tool_frame, name = self.Bucket.tool_name, bitmap = '@bucket.xbm', width = 64, height = 64)
        self.bucket_button.bind('<ButtonRelease-1>', self.tool_button_clicked)
        self.bucket_button.grid(in_ = self.tool_frame)

    def color_area(self):
        self.color_frame = ttk.LabelFrame(self.top_right_frame, labelanchor = 's', borderwidth = 2, text = 'Colors')
        self.color_frame.grid(row = 0, column = 2, in_ = self.top_right_frame, sticky = N+S)

        self.palette_frame = ttk.LabelFrame(self.color_frame, labelanchor = 's', borderwidth = 0, text= 'Palette')
        self.palette_frame.grid(row = 0, in_ = self.color_frame)
        self.palette_frame.columnconfigure(0, weight = 1)
        self.palette_frame.columnconfigure(2, weight = 1)

        self.current_color_frame = ttk.LabelFrame(self.color_frame, labelanchor='s', borderwidth = 0, text='Current')
        self.current_color_frame.grid(row = 1, in_ = self.color_frame, sticky = S)
        self.current_color_frame.columnconfigure(0, weight = 1)
        self.current_color_frame.columnconfigure(2, weight = 1)

        self.black_swatch = Canvas(self.palette_frame, height = 32, width = 32, borderwidth = 3, relief = 'sunken', bg = NGE_BLACK)
        self.black_swatch.bind('<ButtonRelease-1>', self.color_swatch_clicked)
        self.black_swatch.grid(pady=5, in_ = self.palette_frame, row = 0, column = 1)

        self.dk_gray_swatch = Canvas(self.palette_frame, height = 32, width = 32, borderwidth = 3, relief = 'sunken', bg = NGE_DK_GRAY)
        self.dk_gray_swatch.bind('<ButtonRelease-1>', self.color_swatch_clicked)
        self.dk_gray_swatch.grid(pady=5, in_ = self.palette_frame, row = 1, column = 1)
        
        self.lt_gray_swatch = Canvas(self.palette_frame, height = 32, width = 32, borderwidth = 3, relief = 'sunken', bg = NGE_LT_GRAY)
        self.lt_gray_swatch.bind('<ButtonRelease-1>', self.color_swatch_clicked)        
        self.lt_gray_swatch.grid(pady=5, in_ = self.palette_frame, row = 2, column = 1)

        self.white_swatch = Canvas(self.palette_frame, height = 32, width = 32, borderwidth = 3, relief = 'sunken', bg = NGE_WHITE)
        self.white_swatch.bind('<ButtonRelease-1>', self.color_swatch_clicked)        
        self.white_swatch.grid(in_ = self.palette_frame, row = 3, column = 1)

        self.current_color_swatch = Canvas(self.current_color_frame, height = 32, width = 32, borderwidth = 3, relief = 'sunken', bg = NGE_WHITE)
        self.current_color_swatch.grid(pady = 5, in_ = self.current_color_frame, row = 1, column = 1)
        

    def text_area(self):

        self.text_frame = ttk.LabelFrame(self.bottom_right_frame, labelanchor='s', borderwidth = 2, text = 'Hex Data')
        self.text_frame.grid(row = 1, column = 1, in_ = self.bottom_right_frame, columnspan = 3, ipadx = 5, ipady = 5, padx = 5, pady = 5)
        
        self.hex_display = Text(self.text_frame, width=53, height=16)
        self.hex_display.grid(row = 0, column = 0, in_ = self.text_frame)
        
        self.hex_display_scrollbar = Scrollbar(self.text_frame, orient = VERTICAL, command=self.hex_display.yview)
        self.hex_display_scrollbar.grid(row = 0, column = 1, sticky=N+S, in_ = self.text_frame)
        self.hex_display['yscrollcommand'] = self.hex_display_scrollbar.set

    def tree_area(self):
        self.tree_area_frame = ttk.LabelFrame(self.bottom_left_frame, labelanchor='s', borderwidth = 2, text = 'Information')
        self.tree_area_frame.grid(row = 1, column = 0, in_ = self.bottom_left_frame, sticky=N+S, padx = 5, pady =5, ipadx = 5, ipady = 5)
        
        self.tree_view_frame = ttk.Frame(self.tree_area_frame)
        self.tree_view_frame.grid(row = 0, column = 0, in_ = self.tree_area_frame)
        
        self.info_frame = ttk.LabelFrame(self.tree_area_frame, labelanchor = 's', text = 'Active Items')
        self.info_frame.grid(row = 0, column = 2, in_ = self.tree_area_frame, sticky = N+S)
        
        self.tree_view = ttk.Treeview(self.tree_area_frame, columns = ('Books', 'Sheets', 'Length'), displaycolumns='#all')
        self.tree_view.column('#0', width=150)
        self.tree_view.heading('#0', text = 'Shelf')
        self.tree_view.column('Books', width = 150)
        self.tree_view.heading('Books', text = 'Books')
        self.tree_view.column('Sheets', width= 150)
        self.tree_view.heading('Sheets', text='Sheets')
        self.tree_view.column('Length', width = 60)
        self.tree_view.heading('Length', text='Length')
        self.tree_view.grid(column=0, row =0, columnspan = 2, in_ = self.tree_area_frame)
        self.tree_view.bind('<<TreeviewSelect>>', self.make_active)
        self.tree_view_update()

        self.book_controls = ttk.Frame(self.tree_area_frame)
        self.book_controls.grid(row = 1, column = 0, in_ = self.tree_area_frame)
        
        self.add_book_button = ttk.Button(self.book_controls, name = 'add_book', text = '+', width = 2)
        self.add_book_button.grid(row = 0, column = 0, in_ = self.book_controls)
        self.add_book_button.bind('<ButtonRelease-1>', self.add_dialog)
        
        self.book_label = ttk.Label(self.book_controls, text = "Book")
        self.book_label.grid(row = 0, column = 1, in_ = self.book_controls)
        
        self.remove_book_button = ttk.Button(self.book_controls, name = 'remove_book', text = '-', width = 2)
        self.remove_book_button.grid(row = 0, column = 2, in_ = self.book_controls)
        self.remove_book_button.bind('<ButtonRelease-1>', self.remove_dialog)

        self.sheet_controls = ttk.Frame(self.tree_area_frame)
        self.sheet_controls.grid(row=1, column = 1, in_ = self.tree_area_frame)
        
        self.add_sheet_button = ttk.Button(self.sheet_controls, name = 'add_sheet', text = '+', width = 2)
        self.add_sheet_button.grid(row = 0, column = 0, in_ = self.sheet_controls)
        self.add_sheet_button.bind('<ButtonRelease-1>', self.add_dialog)
        
        self.sheet_label = ttk.Label(self.sheet_controls, text = "Sheet")
        self.sheet_label.grid(row = 0, column = 1, in_ = self.sheet_controls)
        
        self.remove_sheet_button = ttk.Button(self.sheet_controls, name = 'remove_sheet', text = '-', width = 2)
        self.remove_sheet_button.grid(row = 0, column = 2, in_ = self.sheet_controls)
        self.remove_sheet_button.bind('<ButtonRelease-1>', self.remove_dialog)

        self.active_book_label = ttk.Label(self.info_frame, text = 'Active Book: ')
        self.active_book_label.grid(column = 0, row = 0, in_=self.info_frame)
        
        self.active_book_name = ttk.Label(self.info_frame, textvariable = self.active_book)
        self.active_book_name.grid(column = 0, row = 1, in_=self.info_frame)
        
        self.active_sheet_label = ttk.Label(self.info_frame, text = 'Active Sheet: ')
        self.active_sheet_label.grid(column = 0, row = 2, in_=self.info_frame)
        
        self.active_sheet_name = ttk.Label(self.info_frame, textvariable = self.active_sheet)
        self.active_sheet_name.grid(column = 0, row = 3, in_=self.info_frame)
    ##########################
    ###END WIDGET FUNCTIONS###
    ##########################