from tkinter import *
from tkinter import filedialog as fd
from tkinter import ttk #pip install tkinter
import os
import ScrollableFrame as sf
import csv
import webbrowser

class csvReader:
    masterChannelList = [[]]
    optionsMappingKeyIndex = {}
    optionsMappingKeyName = {}
    outputsCounts = {}
    outputsTotals = {}
    outputLabels = {}
    outputLabelMasterFrame = None
    channelListFrame = None
    currentOutput = None
    options = None
    resultsBGColor = '#99ccff'
    canvasBGColor = '#669999'
    goodColor = '#33cc33'
    goodColorLighter = '#99e699'
    badColor = '#b32400'
    badColorLighter = '#ff5c33'
    unknownColor = '#ffff80'
    unknownColorLighter = '#ffffb3'
    fileLocation = os.getcwd()
    
    
    
    def __init__(self, root):
        root.geometry("1200x500")
        s =ttk.Style()
        s.theme_create('good.TButton','default')
        s.theme_create('bad.TButton','default')
        s.theme_create('good.TLabel','default')
        s.theme_create('notif.TFrame','default')
        s.theme_create('notif.TLabel','default')
        s.theme_create('unknown.TLabel','default')
        s.theme_create('unknown.TButton','default')
        s.theme_create('bg.TFrame')
        s.configure('bg.TFrame', background=self.canvasBGColor)
        s.configure('unknown.TLabel', background=self.unknownColor)
        s.configure('notif.TFrame', background=self.resultsBGColor)
        s.configure('notif.TLabel', background=self.resultsBGColor)
        s.configure('good.TLabel',  foreground='black', background=self.goodColor)
        s.configure('bad.TLabel', foreground='white',background=self.badColor)
        s.configure('notif.TFrame', frameBoarder=2)
        
        s.configure('good.TButton',  foreground='black', background=self.goodColor)
        s.map('good.TButton', background=[('active', self.goodColorLighter)], foreground=[('active', 'black')])
        
        s.configure('bad.TButton', foreground='white',background=self.badColor)
        s.map('bad.TButton', background=[('active', self.badColorLighter)], foreground=[('active', 'white')])
        
        s.configure('unknown.TButton', foreground='black',background=self.unknownColor)
        s.map('unknown.TButton', background=[('active', self.unknownColorLighter)], foreground=[('active', 'black')])
        

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
        scrollFrameMaster.changeCanvasColor(self.canvasBGColor)
        self.channelListFrame = scrollFrameMaster.scrollable_frame
        scrollFrameMaster.grid(column=0, row=1, sticky="nsew")
        self.channelListFrame.rowconfigure(0, weight=1)
        self.channelListFrame.columnconfigure(0, weight=1)
        #self.channelListFrame.configure(borderwidth=2)
        scrollFrameMaster.rowconfigure(0, weight=1)
        scrollFrameMaster.columnconfigure(0,weight=1)
        self.channelListFrame.configure(style='bg.TFrame')
        
        print("self.channelListFrame winfo_width: %d" %self.channelListFrame.winfo_width())
        #ttk.Label(master=self.channelListFrame, text="test").grid(column=1, row=0, sticky=E)
        #ttk.Button(self.channelListFrame, text="button",command=self.outputDimensions).grid(column=0, row=0, sticky=E)
        
        self.options.bind('<<ComboboxSelected>>', self.handle_channels)
        
        #top right panel
        buttonsFrame = ttk.Frame(mainframe)
        print("buttons Frame %s"%type(buttonsFrame))
        buttonsFrame.grid(column=1, row=0,sticky="new")
        ttk.Button(buttonsFrame, text="Load file", command=self.getFileName).grid(column=0, row=0, sticky=(EW))
        ttk.Button(buttonsFrame, text="reset", command=self.clearData).grid(column=1, row=0, sticky=(EW))
        #load file button and reset data
        
        #bottom right panel
        self.outputLabelMasterFrame = ttk.Frame(mainframe)
        self.outputLabelMasterFrame.grid(row=1, column=1, sticky="new")
        self.outputLabelMasterFrame.columnconfigure(0, weight=1)
        #self.outputLabelMasterFrame.configure(style='notif.TFrame')
        
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
            #print("gridding %s" %(str(element[0])))
            if i %2 == 0:
                element[0].configure(style='notif.TFrame')
                element[0].winfo_children()[1].configure(style='notif.TLabel')
            else:
                element[0].configure(style='TFrame')
                element[0].winfo_children()[1].configure(style='TLabel')
            element[0].grid(column=0, row=i, sticky=("we"))
            
            #print("element Style: %s" %element[0]['style'])
            i+=1
        #self.channelListFrame.grid(row=0, column=0, sticky="new")
    
    def makeChannel(self, parentFrame, iteration, name, channels, Channel_number, results, link):
        def createFrame():
            url = link
            frame = ttk.Frame(parentFrame, style='notif.TFrame', padding=2, relief='raised')
            details = ""
            if results[0] == 'false':
                details += "OCR: false | "
            if results[1] == 'false':
                details += "Error Text: false | "
            if results[2] == 'false':
                details += "Motion: false | "
            if results[3] == 'false':
                details += "Frozen: false | "
            ttk.Label(frame, text="Iteration: %s | %s %s" %(iteration, name, Channel_number), style='unknown.TLabel').grid(column=0, row=0, sticky=("nsw"))
            ttk.Label(frame, text=details,style='notif.TLabel').grid(column=1, row=0,sticky=("e"))
            ttk.Button(frame, text="OK", command=lambda : self.changeButtons(frame, True)).grid(column=2, row=0, sticky=("e"))
            ttk.Button(frame, text="BAD", command=lambda: self.changeButtons(frame, False)).grid(column=3, row=0,sticky=("e"))
            ttk.Button(frame, text="Link", command=lambda: self.openURL(link,"I:%s | Chan %s %s" %(iteration, name, Channel_number)), style='unknown.TButton').grid(column=4, row=0, sticky=("e"))
            frame.columnconfigure(0, weight=10)
            frame.columnconfigure(1, weight=10)
            return [frame, url]    
        channels.append(createFrame())
        
    def changeButtons(self,frame, success):
        if success:
            if not frame.winfo_children()[0]['style'] == 'good.TLabel':
                #increment for a success
                self.outputsCounts[self.optionsMappingKeyIndex[self.options.current()]] += 1
                self.updateTotals(self.optionsMappingKeyIndex[self.options.current()])
            frame.winfo_children()[0].configure(style='good.TLabel')
            frame.winfo_children()[2].configure(style='good.TButton')
            if(frame.winfo_children()[3]['style'] != ''):
                frame.winfo_children()[3].configure(style='TButton')
            frame.winfo_children()[4].configure(style='TButton')
        else :
            frame.winfo_children()[0].configure(style='bad.TLabel')
            frame.winfo_children()[3].configure(style='bad.TButton')
            frame.winfo_children()[4].configure(style='TButton')
            if(frame.winfo_children()[2]['style'] == 'good.TButton'):
                frame.winfo_children()[2].configure(style='TButton')
                self.outputsCounts[self.optionsMappingKeyIndex[self.options.current()]] -= 1
                self.updateTotals(self.optionsMappingKeyIndex[self.options.current()])
    def getFileName(self):
        name = fd.askopenfilename(filetypes=[("csv files", ".csv")],initialdir=self.fileLocation)
        if name != "":
            self.parseCSV(name)
            self.fileLocation = "/".join(name.replace('\\', '/').split("/")[0:-1])
            print(self.fileLocation)
            
            
    
    def parseCSV(self, fileName):
        fileD = open(file=fileName, newline='')
        #print(fileD.readline()) #toss the header
        #print("reading file")
        reader = csv.reader(fileD, dialect='excel')
        for row in reader:
            outputType =row[1].lower()
            if outputType == 'output':
                continue
            if not outputType in self.options['values']:
                tempOptions = list(self.options['values'])
                tempOptions.append(outputType)
                self.options['values'] = tuple(tempOptions)
                self.updateOptionsBindings()
                self.masterChannelList.append([])
                self.outputsCounts[outputType] = 0
                self.outputsTotals[outputType] = 0
                self.makeOutputLabel(outputType)
                
            if row[5].lower() == 'false' or row[6].lower() == 'false' or row[7].lower() == 'false' or row[8].lower() == 'false':
                results = []
                for i in range(5, 9):
                    results.append(row[i].lower())
                self.makeChannel(self.channelListFrame, row[0], row[1], self.masterChannelList[self.optionsMappingKeyName[outputType]], row[2], results, row[3])
                self.outputsTotals[outputType] += 1
            else:
                self.outputsCounts[outputType] += 1
                self.outputsTotals[outputType] += 1
        #print("Options Mapping Key Index %s"% self.optionsMappingKeyIndex)
        #print("Options Mapping Key Name %s"% self.optionsMappingKeyName)
        for outputIndex in self.optionsMappingKeyIndex:
            #print("outputIndex: %s"% outputIndex)
            self.updateTotals(self.optionsMappingKeyIndex[outputIndex])
                        
    def updateOptionsBindings(self):
        i=0
        for value in self.options['values']:
            self.optionsMappingKeyIndex[i] = value
            self.optionsMappingKeyName[value] = i
            i+=1
        
    def updateTotals(self, outputTypeName):
        #print("updating Totals")
        tempframe = self.outputLabels[self.optionsMappingKeyName[outputTypeName]]
        tempframe.winfo_children()[1].configure(text=" %d/%d"%(self.outputsCounts[outputTypeName], self.outputsTotals[outputTypeName]))
        if self.outputsCounts[outputTypeName] == self.outputsTotals[outputTypeName]:
            tempframe.winfo_children()[1].configure(style='good.TLabel')
        elif tempframe.winfo_children()[1]['style'] != '':
            tempframe.winfo_children()[1].configure(style='TLabel')

    
    def makeOutputLabel(self, outputTypeName):
        #print("making output label for %s"%outputTypeName)
        frame = ttk.Frame(self.outputLabelMasterFrame)
        ttk.Label(frame, text=outputTypeName).grid(column=0, row=0, sticky="w")
        ttk.Label(frame, text=" %d/%d"%(self.outputsCounts[outputTypeName], self.outputsTotals[outputTypeName])).grid(column=1, row=0, sticky="e")
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        frame.grid(column=0, row=self.optionsMappingKeyName[outputTypeName], sticky="ew")
        self.outputLabels[self.optionsMappingKeyName[outputTypeName]] = frame
        #print("output labels contents: %s"%str(self.outputLabels))
        
    def clearData(self):
        self.removeChannels()
        for element in self.outputLabelMasterFrame.winfo_children():
            element.grid_forget()
        self.masterChannelList = [[]]
        self.optionsMappingKeyIndex = {}
        self.optionsMappingKeyName = {}
        self.outputsCounts = {}
        self.outputsTotals = {}
        self.outputLabels = {}
        self.options['values'] = ""
        self.options.selection_clear()
        self.updateOptionsBindings()
        return ""
    def openURL(self, loadUrl, name):
       webbrowser.open_new_tab(loadUrl)
       
    def outputDimensions(self):
        print("Width: %d, Height %d"%(self.channelListFrame.winfo_width(), self.channelListFrame.winfo_height()))
        print(self.channelListFrame.grid_size())
        
        
        
root = Tk()
csvReader(root)
root.mainloop()