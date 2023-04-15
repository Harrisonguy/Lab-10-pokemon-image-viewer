from tkinter import *
from tkinter import ttk
import os
import ctypes
import pokeapi
import image_lib

# Get the path of the script and its parent directory
script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)

# Create image cache directory
image_cache_dir = os.path.join(script_dir, 'images')
if not os.path.isdir(image_cache_dir):
    os.makedirs(image_cache_dir)


# Create the main window
root = Tk()
root.title("Pokemon Image Viewer")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.minsize(500, 600)


# Set the window icon
icon_path = os.path.join(script_dir, 'poke.ico')
app_id = 'COMP593.PokeImageViewer'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
root.iconbitmap(icon_path)

# Put a frame on the GUI
frame = ttk.Frame(root, relief='ridge')
frame.grid(row=0, column=0, sticky=NSEW)
frame.columnconfigure(0, weight=100)
frame.rowconfigure(0, weight=100)

# Put image into frame
image_path = os.path.join(script_dir, 'logo.png')
img_poke = PhotoImage(file=image_path)
lbl_image = ttk.Label(frame, image=img_poke)
lbl_image.grid(padx=10, pady=10)


# Put the pull-down list of the pokemon names into frame
pokemon_name_list = sorted(pokeapi.get_pokemon_names())
cbox_poke_name = ttk.Combobox(frame, values=pokemon_name_list, state='readonly')
cbox_poke_name.set("Select a Pokemon")
cbox_poke_name.grid(padx=10, pady=(10,0))

def handle_pokemon_select(event):
    """changes display image into selected pokemon on GUI

    Args:
        event (<<ComboboxSelected>>): when the user selects from the drop down menu.
    """
      
    sel_pokemon = cbox_poke_name.get()
    if sel_pokemon is None:
        return
    else:
        btn_set_desktop.config(state='normal')
    global image_path
    image_path = pokeapi.download_pokemon_artwork(sel_pokemon, image_cache_dir)
    img_poke['file'] = image_path

cbox_poke_name.bind('<<ComboboxSelected>>', handle_pokemon_select)

def handle_set_desktop():
    """Sets desktop background.
    """
    image_lib.set_desktop_background_image(image_path)


# Put "set desktop" button into frame
btn_set_desktop = ttk.Button(frame, text='Set as desktop image', command=handle_set_desktop)
btn_set_desktop.grid(padx=10, pady=(10, 20))
btn_set_desktop.config(state='disabled')

root.mainloop()