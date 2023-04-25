# Import tkinter and webview libraries
from tkinter import *
import webview
  
# define an instance of tkinter
#tk = Tk()
  
#  size of the window where we show our website
#tk.geometry("800x450")
  
# Open website
webview.create_window('video', 'http://10.70.20.4:5000/61-15_nightly_debug/2023-04-25/447-SMB2--_Standalone_STB-Tester_Nightly_Test/Iteration_1/DishIP106.mp4')
webview.start()