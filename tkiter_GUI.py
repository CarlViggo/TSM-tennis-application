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
        self.create_setting_input("Number of Balls", "num_balls", 0)
        self.create_setting_input("Standard Deviation", "std", 1)
        self.create_setting_input("Execution Speed", "speed", 2)
        self.create_setting_input("Length", "length", 3)
        self.create_setting_input("Width", "width", 4)
        
        # create "run" button
        start_button = ttk.Button(self.root, text="RUN", command=self.run_program)
        start_button.grid(row=len(self.settings), column=0, columnspan=2, pady=10)

        # the "status" label should for now be invisible
        self.status_label = ttk.Label(self.root, text="")
        self.status_label.grid(row=len(self.settings)+1, column=0, columnspan=2, pady=10)

    def create_setting_input(self, label_text, setting_key, row):
        label = ttk.Label(self.root, text=label_text)
        label.grid(row=row, column=0, padx=10, pady=5, sticky='w')
        
        entry = ttk.Entry(self.root, textvariable=self.settings[setting_key])
        entry.grid(row=row, column=1, padx=10, pady=5)
        self.entries[setting_key] = entry 

    def run_program(self):
        # store "valid" user input here
        settings_dict = {}

        # make sure num_valls >= 5, that it's an integer value, and that the rest are float
        for setting, value in self.settings.items():
            # get user input from the dict
            user_input = self.entries[setting].get()  
            try:
                if setting == "num_balls":
                    settings_dict[setting] = int(user_input)
                    if int(user_input) < 5:
                        raise ValueError
                else:
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
