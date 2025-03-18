#######################################################################################################
######### This file will create a GUI for choosing structures to be used in the optimization. #########
####### The work is done by Mia Johanne Larsen (contact: mia@bel.no or +47 482 11 593) as work ########
################# in her masters thesis in biophysics at NTNU in the spring of 2025. ##################
#######################################################################################################

import tkinter as tk
from tkinter import *
from tkinter import Tk, Label, Button, Frame, X
from tkinter import ttk


def add_entry(label_text, options, frame, default_value):
    # Initialize row count if it doesn't exist
    if not hasattr(frame, "row_count"):
        frame.row_count = 0
    
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=1)
    
    Label(frame, text=label_text, font=("Arial", 10, "bold"), anchor="center", justify="center").grid(
        row=frame.row_count, column=0, sticky="ew", padx=5, pady=5)
    combo = ttk.Combobox(frame, values=options, width=25)
    
    if default_value in options:
        combo.set(default_value)
    combo.grid(row=frame.row_count, column=1, padx=5, pady=5)
    frame.row_count += 1

    return combo

def structure_lists(patient):
    ctv_list = []
    gtv_list = []
    oar_list = []
    
    for roi in patient.RegionsOfInterest:
        if roi.Type == 'Ctv':
            ctv_list.append(roi.Name)

        if roi.Name == 'ICTV_eskalert':
            ctv_list.append(roi.Name)

    for roi in patient.RegionsOfInterest:
        if roi.Type == 'Gtv':
            gtv_list.append(roi.Name)

    for roi in patient.RegionsOfInterest:
        if roi.Type != 'Ctv' and roi.Type != 'Gtv' and roi.Type != 'Ptv':
            oar_list.append(roi.Name)
    
    return ctv_list, gtv_list, oar_list


def structure_gui(ctv_list, gtv_list, oar_list):
    # Set up window
    win = Tk()
    win.title("Structure registration")
    win.geometry("600x800")
    win.resizable(False, True)
    
    # Set the style for better font and color
    style = ttk.Style()
    style.configure("TLabel", font=("Arial", 10))
    style.configure("Header.TLabel", font=("Arial", 12, "bold"))

    # Create a header for instructions
    info_label = tk.Label(win, text="If the patient doesn't have the structure, leave the field empty.\n"
         "Select PET volume for PET boost or GTVp to escalate the entire GTVp.",
         font=("Arial", 10, "italic"),
         wraplength=500)
    info_label.pack()
    
    main_frame = Frame(win, padx=10, pady=10)
    main_frame.pack(fill=X)
    
    # Create dictionary for storing structures
    struct_dict = {}
    
    # Add structure selection fields
    ctvbox = add_entry("ICTV:", ctv_list, main_frame, default_value="ICTV")
    ctvpbox = add_entry("ICTVp:", ctv_list, main_frame, default_value="ICTVp")
    ctvnbox = add_entry("ICTVn:", ctv_list, main_frame, default_value="ICTVn")
    ictv_gtv_box = add_entry("ICTVp-IGTVp:", ctv_list, main_frame, default_value="ICTVp-IGTVp")
    gtvpbox = add_entry("GTVp:", gtv_list, main_frame, default_value="IGTVp")
    boostbox = add_entry("Primary Boost Volume:", gtv_list, main_frame, default_value="GTVp_PT")
    gtvnbox = add_entry("GTVn:", gtv_list, main_frame, default_value=None)
    nodebox = add_entry("Nodal Boost Volume:", gtv_list, main_frame, default_value=None)
    bodybox = add_entry("Body:", oar_list, main_frame, default_value="Body")
    lungsbox = add_entry("Lungs:", oar_list, main_frame, default_value="Lungs-IGTV")
    heartbox = add_entry("Heart:", oar_list, main_frame, default_value="Heart")
    esophbox = add_entry("Esophagus:", oar_list, main_frame, default_value="Esophagus")
    spinalbox = add_entry("Spinal Canal:", oar_list, main_frame, default_value="SpinalCanal")
    wallbox = add_entry("Chest Wall:", oar_list, main_frame, default_value="Chestwall")
    ctbox = add_entry("Mediastinum:", oar_list, main_frame, default_value="ConnectiveTissue")
    tracheabox = add_entry("Trachea:", oar_list, main_frame, default_value="Trachea")
    bronchibox = add_entry("Bronchi:", oar_list, main_frame, default_value="Bronchus")
    aortabox = add_entry("Aorta:", oar_list, main_frame, default_value="A_Aorta")
    plexusbox = add_entry("Plexus Brachialis:", oar_list, main_frame, default_value=None)
    ictv_expbox = add_entry("ICTV Expanded:", ctv_list, main_frame, default_value="ICTV_expanded")
    
    
    def Button_pressed():
        global ctv, ctvp, ctvn, ictv_gtv
        global gtvp, boost, gtvn, nodeboost
        global body, lungs, heart, esophagus, spinal, chestwall
        global mediastinum, trachea, bronchi, aorta, plexus, expanded
    
        struct_dict['ctv'] = ctvbox.get()
        struct_dict['ctvp'] = ctvpbox.get()
        struct_dict['ctvn'] = ctvnbox.get()
        struct_dict['ictv_gtv'] = ictv_gtv_box.get()
        struct_dict['gtvp'] = gtvpbox.get()
        struct_dict['boost'] = boostbox.get()
        struct_dict['gtvn'] = gtvnbox.get()
        struct_dict['nodeboost'] = nodebox.get()
        struct_dict['body'] = bodybox.get()
        struct_dict['lungs'] = lungsbox.get()
        struct_dict['heart'] = heartbox.get()
        struct_dict['esophagus'] = esophbox.get()
        struct_dict['spinal'] = spinalbox.get()
        struct_dict['chestwall'] = wallbox.get()
        struct_dict['mediastinum'] = ctbox.get()
        struct_dict['trachea'] = tracheabox.get()
        struct_dict['bronchi'] = bronchibox.get()
        struct_dict['aorta'] = aortabox.get()
        struct_dict['plexus'] = plexusbox.get()
        struct_dict['expanded'] = ictv_expbox.get()
        
        win.destroy()
    
    button = Button(win, text="Save", command=Button_pressed)
    button.pack()
    win.mainloop()
    
    return struct_dict

# Function for unpacking dictionary since this will make the main file less cluttered
def dict_unpack(dict):
    ctv = dict['ctv']
    ctvp = dict['ctvp'] 
    ctvn = dict['ctvn']  
    ictv_gtv = dict['ictv_gtv']
    gtvp = dict['gtvp']  
    boost = dict['boost'] 
    gtvn = dict['gtvn'] 
    nodeboost = dict['nodeboost'] 
    body = dict['body']  
    lungs = dict['lungs'] 
    heart = dict['heart']  
    esophagus = dict['esophagus']  
    spinal = dict['spinal']  
    chestwall = dict['chestwall'] 
    mediastinum = dict['mediastinum']  
    trachea = dict['trachea'] 
    bronchi = dict['bronchi'] 
    aorta = dict['aorta'] 
    plexus = dict['plexus']  
    expanded = dict['expanded'] 
    
    return ctv, ctvp, ctvn, ictv_gtv, gtvp, boost, gtvn, nodeboost, body, lungs, heart, esophagus, spinal, chestwall, mediastinum, trachea, bronchi, aorta, plexus, expanded