# autoscript_lung

This project is a part of my master's thesis at NTNU in collaboration with Haukeland University Hospital. The script automatically creates a dose-escalated proton therapy treatment plan in RayStation intended for LA-NSCLC patients in preparation of a future clinical trial in Norway. It is necessary to have know the wanted beam angles before starting the script. 

4 files are necessary for the script to be run correctly, "function_definitions.py", "structure_gui.py", "beam_gui.py", and "main.py".

The script starts with a GUI for structure selection based on the open imaging set, then a new GUI for inputting beam angles, and finally a GUI for plan name. Currently (as of 18.03.2025), beam angles of 0 do not register and must be altered manually. This altering can be done after giving the plan name as the script at this point has a break in which all details thus far inputted should be checked to be correct, in which a 0 beam angle may be added if necessary. 

The script will be updated from time to time during this spring semester, so check that you have the most recent version for best results. 

For any questions, feel free to contact me at mia@bel.no
