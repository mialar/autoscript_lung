# autoscript_lung

This project is a part of my master's thesis at NTNU in collaboration with Haukeland University Hospital. The script automatically creates a dose-escalated proton therapy treatment plan in RayStation intended for LA-NSCLC patients in preparation of a future clinical trial in Norway. It is necessary to have know the wanted beam angles before starting the script. 

4 files are necessary for the script to be run correctly, "function_definitions.py", "structure_gui.py", "beam_gui.py", and "main.py".

The script starts with a GUI for structure selection based on the open imaging set, then a new GUI for inputting beam angles, and finally a GUI for plan name. Currently (as of 18.03.2025), beam angles of 0 do not register and must be altered manually. This altering can be done after giving the plan name as the script at this point has a break in which all details thus far inputted should be checked to be correct, in which a 0 beam angle may be added if necessary. 

The optimization is based on constraints to organs at risk from the NARLAL2 dose-escalation study performed in Denmark and Norway with photon radiotherapy as well as some decrease in lung and heart doses to achieve greater safety margins in regards to toxicity. The script escalates a primary boost volume in the primary tumor to 95 Gy and a nodal boost volume in affected lymph nodes to 74 Gy. The rest of the tumor volume outside the boost volumes are given 66 Gy in 33 fractions. The final optimization run in the script uses Monte Carlo simulations with 200 iterations and a tolerance of 1e-9 and saves the plan when finished. 

