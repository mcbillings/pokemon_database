##---------------------------------------------------------------------------------------------------------------
##-----------------------------------------IMPORTED LIBRARIES----------------------------------------------------
##---------------------------------------------------------------------------------------------------------------

from tkinter import *
import urllib.request
from tkinter import simpledialog
import os

##---------------------------------------------------------------------------------------------------------------
##-----------------------------------------FUNCTION DEFINITIONS--------------------------------------------------
##---------------------------------------------------------------------------------------------------------------

labelColor = "#dbc6b2"

def create_files():
    """Creates all the required files to run"""
    if not os.path.exists('my_data'): 
        os.mkdir('my_data') ##Makes the my_data folder if it doesn't exist
        
    if not os.path.exists('my_data\pokemon_wallpaper.gif'):
        urllib.request.urlretrieve('https://drive.google.com/uc?export=download&id=1idKePfAKBhpPIh2-lu3mFeb9T8tOmKHH', 'pokemon_wallpaper.gif')
        os.rename("pokemon_wallpaper.gif", "my_data\pokemon_wallpaper.gif")
    
    if not os.path.exists('my_data\database.txt'):
        urllib.request.urlretrieve('https://drive.google.com/uc?export=download&id=1eUJqlfCHULv9SStmfSbiSm_rG8Wk1YVF', 'database.txt')
        os.rename('database.txt', 'my_data\database.txt')

    database()

def database():
    global pokemon_and_dimensions
    pokemon_and_dimensions = {}
    with open('my_data\database.txt', 'r') as fileobject:
        for line in fileobject:
            key, valuess = line.strip().split(':')
            value = tuple(valuess.strip().split(','))
            pokemon_and_dimensions[key.strip()] = value

def landing_page():
    """Creates and displayes all the widgets on the screen when it's opened"""
    window = Tk()
    window.title('Pokemon Database')
    window.resizable(width=False, height=False) ##Can't resize so background image completely fills window
    
    photo=PhotoImage(file="my_data\pokemon_wallpaper.gif")
    photo_label = Label(window, image = photo, background=labelColor)
    photo_label.grid(column = 1, row = 1) ##Places the image on the screen and uses the same column and row as things in Main_frame so they overlap
    
    global canvas
    canvas = Canvas(window, height = 500, width = 330, background=labelColor)
    canvas.grid(row=1, column=1, sticky=NW)
    
    global main_frame ##Used globally so our add and remove functions can use it
    main_frame = Frame(canvas, height = 500, width = 330, background=labelColor)
    canvas.create_window((170,325), window = main_frame)
    
    vsb = Scrollbar(window, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=vsb.set)

    vsb.grid(row = 1, column = 4, sticky = NS)
    
    canvas.configure(scrollregion=(0,0,0,len(pokemon_and_dimensions)*30+30))

    counter = 2 ##This will be used to position the grid widget and keep the pokemon names and dimensions in line with each other, starts at 2 because headers already populate row 1
    
    update_database_visual()
        
    window.mainloop()

def update_database_visual():
    """Replaces the visuals for the database when it's updated"""
    for widget in main_frame.winfo_children():
        widget.destroy() ##Clears the screen
        
    ##Headers----------------------------------------------------------------------------
    pokemon_header = Label(main_frame, text = "Pokemon", font = 200, bg = labelColor)
    pokemon_header.grid(column = 1, row = 1, sticky = W)
        
    height_header = Label(main_frame, text = "Height (cm)", font = 200, bg = labelColor)
    height_header.grid(column = 2, row = 1, sticky = W)
        
    weight_header = Label(main_frame, text = "Weight (lbs)", font = 200, bg = labelColor)
    weight_header.grid(column = 3, row = 1, sticky = W)

    counter = 2 ##This will be used to position the grid widget and keep the pokemon names and dimensions in line with each other, starts at 2 because headers already populate row 1
    for item in pokemon_and_dimensions: ##Places all of the items in dictionary on the screen

        ##Populating Database-----------------------------------------------------------------
        pokemon = Label(main_frame, text = str(item).capitalize(), font = 200, bg = labelColor)
        pokemon.grid(column = 1, row = counter, sticky = W)
        
        height = Label(main_frame, text = pokemon_and_dimensions[item][0], font = 200, bg = labelColor)
        height.grid(column = 2, row = counter, sticky = W)

        weight = Label(main_frame, text = pokemon_and_dimensions[item][1], font = 200, bg = labelColor)
        weight.grid(column = 3, row = counter, sticky = W)
        
        counter += 1
        
    add_entries_button = Button(text = "Add", command = add_entries, width = 10)
    add_entries_button.place(x=590, y = 100)
    
    remove_entries_button = Button(text = "Remove", command = remove_entries, width = 10)
    remove_entries_button.place(x=590, y = 150)
    
    canvas.configure(scrollregion=(0,0,500,len(pokemon_and_dimensions)*30+30))

def add_entries():
    keyValid = False ##Used to make sure user enters a non-empty string
    
    while not keyValid:
        add_key = simpledialog.askstring("Pokemon Name", "Pokemon Name")
        if add_key != "":
            keyValid = True
    add_height = simpledialog.askfloat("Pokemon Height (cm)", "Pokemon Height (cm)")
    add_weight = simpledialog.askfloat("Pokemon Weight (lbs)", "Pokemon Weight (lbs)")
    
    with open('my_data\database.txt', 'a') as fileobject: ##Adds user input to the database file
        fileobject.write(str(add_key) + ": " + str(add_height) + ", " + str(add_weight))
    
    height_and_weight = (add_height, add_weight)
    
    pokemon_and_dimensions.update({add_key: height_and_weight}) ##Adds the new item to the database dictionary

    update_database_visual()
    
    
def remove_entries():
    remove_mon = simpledialog.askstring("Pokemon Name", "Pokemon Name").lower()
    del pokemon_and_dimensions[remove_mon]
    update_database_visual()


create_files()
landing_page()