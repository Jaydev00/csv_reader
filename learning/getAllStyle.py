import tkinter.ttk as ttk
from pprint import pprint                                                      

s = ttk.Style()                                                                
data = {}                                                                      
for e in s.element_names():
    #pprint(e)                                                    
    data[e] = s.element_options(e)      

pprint(s.lookup("TCombobox", "font"))
#pprint(s.theme_use())
#pprint(len(data))
#pprint(data)