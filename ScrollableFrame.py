import tkinter as tk
from tkinter import ttk

#print("Configure event for masterScrollFrame %s"%e.width)

class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.bind("<Configure>", self.canvasConfigure)

        self.canvasID = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw",tags="frame")
        self.canvas.rowconfigure(0, weight=1)
        self.canvas.columnconfigure(0,weight=1)

        self.canvas.configure(yscrollcommand=scrollbar.set,border=2, borderwidth=10)
        
        self.canvas.grid(column=0,row=0, sticky="nsew")
        scrollbar.grid(column=1, row=0, sticky="ns")
    def canvasConfigure(self, e):
        #print("canvas Configure width %d"% e.width)
        self.canvas.itemconfig(self.canvasID, width = e.width-50)
    def changeCanvasColor(self,color):
        self.canvas.configure(bg=color)
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