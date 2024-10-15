import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from connect_the_dots import main 

class ConnectTheDotsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Settings")
        self.root.geometry("400x400")
        
        # create the settings dictionary which will be passed to main
        # predetermined values values, tkiter datatype for buttons and labels to work.
        self.settings = {
            "num_balls": tk.IntVar(value=30),
            "std": tk.DoubleVar(value=6),
            "speed": tk.DoubleVar(value=0.5),
            "length": tk.DoubleVar(value=50.0),
            "width": tk.DoubleVar(value=30.0),
        }
        
        # store user inputs in this dict
        self.entries = {}  
        
        # create labels and variables for the settings
        self.create_setting_input(label_text = "Number of Balls", setting_key = "num_balls", row = 0)
        self.create_setting_input(label_text = "Standard Deviation", setting_key = "std", row = 1)
        self.create_setting_input(label_text = "Execution Speed", setting_key = "speed", row = 2)
        self.create_setting_input(label_text = "Length", setting_key = "length", row = 3)
        self.create_setting_input(label_text = "Width", setting_key = "width", row = 4)
        
        # create "run" button, obs! run_program is not excecuted for now, just if button is pressed
        start_button = ttk.Button(self.root, text="RUN", command=self.run_program)
        # position it correctly, pady = vertical space around button, columnsspan = number of columns for the button to take up
        start_button.grid(row=len(self.settings), column=0, columnspan=2, pady=10)

        # the "status" label should for now be invisible
        self.status_label = ttk.Label(self.root, text="")
        self.status_label.grid(row=len(self.settings)+1, column=0, columnspan=2, pady=10)

    def create_setting_input(self, label_text, setting_key, row):
        label = ttk.Label(self.root, text=label_text)
        label.grid(row=row, column=0, padx=10, pady=5, sticky='w')
        
        # gets the value from the dictionary defined in constructor 
        # obs! this will be self.settings[key] provided user doesnt change the input
        # if so, then textvariable will be updated with the user input 
        entry = ttk.Entry(self.root, textvariable=self.settings[setting_key])
        entry.grid(row=row, column=1, padx=10, pady=5)

        #add the entry value to self.entries dicrionary
        self.entries[setting_key] = entry 

    def run_program(self):
        # store "valid" user input here
        settings_dict = {}

        # make sure num_valls >= 5, that it's an integer value, and that the rest are float
        for setting, value in self.settings.items():
            # get user input from the dict stored in entries dictionary
            # .get() method needed bekauce keys are tkiter datatypes 
            user_input = self.entries[setting].get()  
            try:
                # check that num_valls exceeds 5
                if setting == "num_balls":
                    settings_dict[setting] = int(user_input)
                    if int(user_input) < 5:
                        raise ValueError
                else:
                    #check that the rest of the settings are floats.
                    settings_dict[setting] = float(user_input)
            except ValueError:
                messagebox.showerror(f"Invalid input for {setting}. You entered '{user_input}'. Enter a valid number.")
                # leave programme 
                return 
       
        # close matplotlib plots from previous runs
        plt.close('all')  
        
        # show label "Computing distances "
        self.status_label.config(text="Computing distances ...")
        self.root.update_idletasks()

        # this runs the backend in connect_the_dots.py file, which
        # returns the approximation of the optimal distance and 
        # if chosen, the actual optimal distance. 
        approx_dist, optimal_dist = main(settings_dict)

        # if optimal_dist is defined, then print out both optimal_dist and the approximation,
        # otherwise only print out the approximation
        if optimal_dist is False:
            self.status_label.config(text=f"Approximation: {approx_dist}")
        else:
            self.status_label.config(text=f"Approximation: {approx_dist}, \n Optimal: {optimal_dist}")

if __name__ == "__main__":
    
    root = tk.Tk()
    
    app = ConnectTheDotsApp(root)
    
    root.mainloop()
