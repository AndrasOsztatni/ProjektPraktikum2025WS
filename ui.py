import tkinter as tk
from tkinter import ttk
import fft
import sfft
import pandas as pd

class AnalysisUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Analysis Configuration")
        
        # Define Data
        self.headers = ["Opening Widths", "in90", "in70", "in60", "in45", "Select All"]
        self.widths = ["10 mm", "20 mm", "30 mm", "40 mm"]
        
        # head_length is 8. Last index is 7 (Select All).
        self.head_length = len(self.headers)
        self.vars = {}
        
        self.init_ui()

    def init_ui(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # 1. Create Headers
        for col, text in enumerate(self.headers):
            header_label = ttk.Label(main_frame, text=text, font=('Helvetica', 10, 'bold'), anchor="center")
            header_label.grid(row=0, column=col, padx=5, pady=5, sticky="nsew")

        # 2. Create Rows
        for row_idx, width_name in enumerate(self.widths):
            actual_row = row_idx + 1 
            
            # Column 0: Label
            name_label = ttk.Label(main_frame, text=width_name)
            name_label.grid(row=actual_row, column=0, padx=5, pady=5, sticky="w")

            # Columns 1 to 6 (Inputs and Results)
            for col_idx in range(1, self.head_length - 1):
                var = tk.BooleanVar()
                self.vars[(row_idx, col_idx)] = var
                if (row_idx+1, col_idx) in [(1, 2), (1, 3), (4, 2), (4, 3), (4, 4)]: continue
                # Logic: Link in90, in70, in60, in45 (Cols 1, 2, 3, 4)
                if col_idx in [1, 2, 3, 4]:
                    cb = ttk.Checkbutton(main_frame, variable=var, 
                                         command=lambda r=row_idx, c=col_idx: self.toggle_group(r, c))
                else:
                    cb = ttk.Checkbutton(main_frame, variable=var)
                
                cb.grid(row=actual_row, column=col_idx, padx=5, pady=5)

            # Column 7: "Select All" Checkbox
            master_idx = self.head_length - 1
            master_var = tk.BooleanVar()
            self.vars[(row_idx, master_idx)] = master_var
            
            master_cb = ttk.Checkbutton(main_frame, variable=master_var, 
                                        command=lambda r=row_idx: self.toggle_row(r))
            master_cb.grid(row=actual_row, column=master_idx, padx=5, pady=5)

        # Run Button
        run_btn = ttk.Button(main_frame, text="Run Analysis", command=self.process_data)
        run_btn.grid(row=len(self.widths)+1, column=0, columnspan=self.head_length, pady=20)

    def toggle_group(self, row_idx, col_clicked):
        """Links columns 1, 2, 3, 4 together"""
        new_state = self.vars[(row_idx, col_clicked)].get()
        for c in []:
            self.vars[(row_idx, c)].set(new_state)

    def toggle_row(self, row_idx):
        """Selects/Deselects the whole row"""
        master_idx = self.head_length - 1
        master_state = self.vars[(row_idx, master_idx)].get()
        for col_idx in range(1, master_idx):
            self.vars[(row_idx, col_idx)].set(master_state)

    def process_data(self):
        print("Starting processing...")
        df = pd.read_csv("init.csv", delimiter=",")
        files = df['file_name'].values
        start_list = df['start_ms'].values
        end_list = df['end_ms'].values
        
        for r in range(len(self.widths)):
            current_width_label = self.widths[r].replace(" ", "")
            width = self.widths[r]
            for c in range(1, self.head_length - 1):
                if self.vars[(r, c)].get():
                    file = f"{current_width_label}_{self.headers[c]}"
                    for i in range(len(start_list)):
                        if file in files[i]:
                            start = start_list[i]
                            end = end_list[i]
                            fft.main(files[i], start, end)
                            sfft.main(files[i], start, end)
                            print(f"Done with {files[i]}")
                        

if __name__ == "__main__":
    root = tk.Tk()
    app = AnalysisUI(root)
    root.mainloop()