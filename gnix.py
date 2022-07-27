from tkinter import *
from tkinter import filedialog
from turtle import bgcolor
import customtkinter as ctk
import os

# Defining a variable used later
success_token = False

# Finding the required ISO file
def find_iso():
    global isoFile, iso_location
    isoFile = filedialog.askopenfilename(
        initialdir='./Downloads', title='',
        filetypes=(("Image files", "*.iso"), ("All files", "*.*"))
    )
    iso_location = str(isoFile)


# Finds the required drive to burn to
def find_drive():
    global drive_location, drive_rough_location, \
        drive_instructions_for_rough_location, verify_token, finderDrive
    drive_instructions_for_rough_location = ctk.CTkLabel(text="Enter your drives path,\n [should be in '/dev/sdx' format] "
    #CHANGED label styling
                                                        , text_font="Arial", text_color="#e4e6eb")
    drive_instructions_for_rough_location.place(x=95, y=38)

    
    drive_rough_location = ctk.CTkEntry(root, fg_color="#212124", border_width=0.8, width=175)
    drive_rough_location.place(x=112, y=80)
    finderDrive = ctk.CTkButton(root, text="Submit", command=lambda: collect_drive_input(),
                                text_color="#ffffff", width=102, height=25, fg_color="#161618",
                                hover_color="#818181", border_color="#818181", border_width=0.8)
    finderDrive.place(x=148, y=120)

# Ensuring that the drive path matches the '/dev/' format, to make sure the output location is a drive, not another directory
def setting_drive_path():
    global drive_location, verify_token
    if verify_drive == True:
        drive_location = str(one_drive)
        verify_token = True
        dd()
    else:
        verify_token = False
        error_message = Label(root, text="Sorry. You didn't enter a valid drive path. Try again. ")
        error_message.pack()
    
    
# Setting the text input to a variable
def collect_drive_input():
    global verify_drive, one_drive
    one_drive = drive_rough_location.get()
    verify_drive = one_drive.startswith("/dev/")
    setting_drive_path()
    

# Runs the 'dd' command with the correct input and output locations
def warning():
    warning_message = Label(root, text="Warning! You're unable to cancel or remove disk")
    warning_message.pack()
    finderISO.destroy()
    drive_rough_location.destroy()
    drive_instructions_for_rough_location.destroy()
    finderDrive.destroy()
    wait_message_during_dd = Label(root, text="Burning image. Please wait...")
    wait_message_during_dd.pack()
   

# Executing the dd command with the correct parameters
def dd():
    warning()
    os.system('dd if=' + str(iso_location) + " of=" + str(drive_location) + ">> ./.success_verification.txt ")
    success_message_file = open('./.success_verification.txt', 'r')
    success_message = success_message_file.read()
    print(success_message)

# Creating actual window
root = ctk.CTk(fg_color="#161618")
root.geometry("400x250")
#root.geometry("+450+200")
root.resizable(False, False)

# Title
root.title("GNIX IMAGE WRITE")

# Creating a dropdown file browser to locate the ISO file
# CHANGED tk button to ctk and defined layout parameters to improve ui
finderISO = ctk.CTkButton(root, text="Select ISO", command=lambda: find_iso(), 
                        text_color="#ffffff", width=102, height=25, fg_color="#161618",
                        border_color="#818181", border_width=1)
finderISO.pack()

# Calling the function to import and act on the user input in the 'Drive Location" text input field
find_drive()

# Keeping window running constantly
root.mainloop()
