import tkinter as tk
from tkinter import ttk


class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.rowconfigure(0, weight=1)
        canvas.columnconfigure(0,weight=1)

        #canvas.pack(side="left", fill="both", expand=True)
        #scrollbar.pack(side="right", fill="y")
        
        canvas.grid(column=0,row=0, sticky="nsew")
        self.scrollable_frame.columnconfigure(0, weight=1)
        self.scrollable_frame.rowconfigure(0, weight=1)
        scrollbar.grid(column=1, row=0, sticky="ns")
        
'''        
root = tk.Tk()

frame = ScrollableFrame(root)
root.rowconfigure(0, weight=1)

for i in range(50):
    ttk.Label(frame.scrollable_frame, text="Sample scrolling label").grid(column=0, row=i, sticky="ew")

frame.grid(column=0, row=0, sticky="ns")
frame.rowconfigure(0, weight=1)
root.mainloop()
'''