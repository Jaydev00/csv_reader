from tkinter import *
from tkinter import filedialog as fd
from tkinter import ttk
import ScrollableFrame as sf
import csv

class csvReader:
    masterChannelList = [[]]
    optionsMapping = {0 : "",
                      1 : "",
                      2 : "",
                      3 : "",
                      4 : ""}
    optionsMappingReverse = {}
    outputsCounts = {}
    outputLabels = {}
    channelListFrame = None
    currentOutput = None
    options = None
    
    
    def __init__(self, root):
        root.geometry("1200x500")
        s =ttk.Style()
        s.theme_create('good.TButton','default')
        s.theme_create('bad.TButton','default')
        s.theme_create('good.TLabel','default')
        s.configure('good.TButton',  foreground='white',background='green', )
        s.map('good.TButton',
              background=[('active', '#90EE90')],
            foreground=[('active', 'white')])
        s.configure('good.TLabel',  foreground='white',background='green', )
        s.map('good.TLabel',
              background=[('active', '#90EE90')],
            foreground=[('active', 'white')])
        s.configure('bad.TButton', foreground='white',background='red')
        s.map('bad.TButton',
              background=[('active', '#ffcccb')],
            foreground=[('active', 'white')])
        s.configure('bad.TLabel', foreground='white',background='red')
        s.map('bad.TLabel',
              background=[('active', '#ffcccb')],
            foreground=[('active', 'white')])
        

        print(ttk.Style().theme_names())
        mainframe = ttk.Frame(root, padding="3 3 12 12")
        mainframe.grid(row=0, column=0, sticky="nsew")
        
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        mainframe.columnconfigure(0, weight=1)
        mainframe.rowconfigure(0,weight=0)
        mainframe.rowconfigure(1,weight=1)
        #top left panel
        self.options = ttk.Combobox(mainframe)
        self.options.state(["readonly"])
        self.options['values'] =('')
        #self.options.current(0)
        self.options.selection_clear()
        self.options.grid(row=0,column=0)
        
        
        #bottom left panel
        scrollFrameMaster = sf.ScrollableFrame(mainframe)
        self.channelListFrame = scrollFrameMaster.scrollable_frame
        scrollFrameMaster.grid(column=0, row=1, sticky="nsew")
        self.channelListFrame.rowconfigure(0, weight=1)
        self.channelListFrame.columnconfigure(0, weight=1)
        scrollFrameMaster.rowconfigure(0, weight=1)
        scrollFrameMaster.columnconfigure(0,weight=1)
        
        ttk.Label(master=self.channelListFrame, text="test").grid(column=0, row=0, sticky="nsew")
        
        #self.makeChannel(self.channelListFrame, 'Streaming', self.sChannels,15)
        #self.makeChannel(self.channelListFrame, 'Diship', self.dChannels, 10)
        
        self.options.bind('<<ComboboxSelected>>', self.handle_channels)
        
        #top right panel
        buttonsFrame = ttk.Frame(mainframe)
        buttonsFrame.grid(column=1, row=0,sticky="new")
        ttk.Button(buttonsFrame, text="Load file", command=self.getFileName).grid(column=0, row=0, sticky=(EW))
        ttk.Button(buttonsFrame, text="reset").grid(column=1, row=0, sticky=(EW))
        #load file button and reset data
        
        #bottom right panel
        ttk.Label()
        #totals
    
    def handle_channels(self,event):
        self.options.selection_clear()
        #print("Handling Channels")
        #print("%s output" %self.options.current())
        self.removeChannels()
        #print("gridding %s"%self.optionsMapping[self.options.current()])
        self.gridChannels(self.masterChannelList[self.options.current()])    
            
        
    def removeChannels(self):
        print("removing Channels")
        for element in self.channelListFrame.winfo_children():
            element.grid_remove()
    def gridChannels(self, channels):
        i = 0
        for element in channels:
            print("gridding %s" %(str(element)))
            element.grid(column=0, row=i, sticky=(E,W))
            print("element Style: %s" %element['style'])
            i+=1
    
    def makeChannel(self, parentFrame, name, channels, Channel_number, results):
        def createFrame():
            frame = ttk.Frame(parentFrame)
            ttk.Label(frame, text="Channel %s %s" %(name, Channel_number)).grid(column=0, row=0, sticky=(E, W))
            details = ""
            if results[0] == 'false':
                details += "OCR: false | "
            if results[1] == 'false':
                details += "Error Text: false | "
            if results[2] == 'false':
                details += "Motion: false | "
            if results[3] == 'false':
                details += "Frozen: false | "
            ttk.Label(frame, text=details).grid(column=1, row=0,sticky=(E))
            ttk.Button(frame, text="OK", command=lambda : self.changeButtons(frame, True)).grid(column=2, row=0, sticky=(W))
            ttk.Button(frame, text="BAD", command=lambda: self.changeButtons(frame, False)).grid(column=3, row=0,sticky=(W))
            frame.columnconfigure(0, weight=1)
            frame.columnconfigure(1, weight=1)
            return frame    
        channels.append(createFrame())
        
    def changeButtons(self,frame, success):
        if success:
            frame.winfo_children()[0].configure(style='good.TLabel')
            frame.winfo_children()[2].configure(style='good.TButton')
            if(frame.winfo_children()[3] != ''):
                frame.winfo_children()[3].configure(style='TButton')
                self.outputsCounts[self.optionsMappingReverse[self.options.current()]] += 1
                self.updateTotals()
        else :
            frame.winfo_children()[0].configure(style='bad.TLabel')
            if(frame.winfo_children()[2] != ''):
                frame.winfo_children()[2].configure(style='TButton')
                self.outputsCounts[self.optionsMappingReverse[self.options.current()]] -= 1
                self.updateTotals()
            frame.winfo_children()[3].configure(style='bad.TButton')
    def getFileName(self):
        name = fd.askopenfilename(filetypes=[("csv files", ".csv")],initialdir='/home/jason/Documents')
        if name != "":
            self.parseCSV(name)
    
    def parseCSV(self, fileName):
        fileD = open(file=fileName, newline='')
        #print(fileD.readline()) #toss the header
        #print("reading file")
        reader = csv.reader(fileD, dialect='excel')
        for row in reader:
            outputType =row[0].lower()
            if outputType == 'output':
                continue
            if not outputType in self.options['values']:
                tempOptions = list(self.options['values'])
                tempOptions.append(outputType)
                self.options['values'] = tuple(tempOptions)
                self.updateOptionsBindings()
                self.masterChannelList.append([])
            if row[3].lower() == 'false' or row[4].lower() == 'false' or row[5].lower() == 'false' or row[6].lower() == 'false':
                results = []
                for i in range(3, 7):
                    results.append(row[i].lower())
                self.makeChannel(self.channelListFrame, row[0], self.masterChannelList[self.optionsMappingReverse[outputType]], row[1], results)
            else:
                self.outputsCounts[outputType] += 1
                        
    def updateOptionsBindings(self):
        i=0
        for value in self.options['values']:
            self.optionsMapping[i] = value
            self.optionsMappingReverse[value] = i
            i+=1
        #print("bindings updated")
        #print(self.optionsMapping)
        #print(self.optionsMappingReverse)
        
    def updateTotals(self):
        
        temp = "yes"
        
        
root = Tk()
csvReader(root)
root.mainloop()