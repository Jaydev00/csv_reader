import tkinter as tk

root = tk.Tk()
root.geometry("200x100")

f1 = tk.Frame(root, background="bisque", width=10, height=100)
f2 = tk.Frame(root, background="pink", width=10, height=100)

f1.grid(row=0, column=0, sticky="nsew")
f2.grid(row=0, column=1, sticky="nsew")

root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=0)

root.mainloop()