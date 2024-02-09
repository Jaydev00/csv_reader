import tkinter
from tkinter import *
from tkinter import filedialog as fd
from tkinter import ttk #pip install tkinter
import os
import ScrollableFrame as sf
import csv
import webbrowser
import re
import matplotlib.pyplot as plt
import numpy as np
from datetime import date
from pprint import pprint
from matplotlib.backend_bases import key_press_handler
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)
from matplotlib.figure import Figure

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
    fileprefix = ''
    labelFont = ('Arial', '16')
    loadedFileNames = []
    
    
    def __init__(self, root):
        root.option_add('*TCombobox*Listbox.font', self.labelFont)
        root.geometry("1200x500")
        s=ttk.Style()
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
        

        
        mainframe = ttk.Frame(root, padding="3 3 12 12")
        mainframe.grid(row=0, column=0, sticky="nsew")
        
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        mainframe.columnconfigure(0, weight=1)
        mainframe.rowconfigure(0,weight=0)
        mainframe.rowconfigure(1,weight=1)
        #top left panel 
        self.options = ttk.Combobox(mainframe, font=self.labelFont)
        self.options.state(["readonly"])
        self.options['values'] =('')
        print(self.options.winfo_class())
            #self.options.current(0)
        self.options.selection_clear()
        self.options.grid(row=0,column=0) #Grid the options
        
        
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
        
        #print("self.channelListFrame winfo_width: %d" %self.channelListFrame.winfo_width())
        #ttk.Label(master=self.channelListFrame, text="test").grid(column=1, row=0, sticky=E)
        #ttk.Button(self.channelListFrame, text="button",command=self.outputDimensions).grid(column=0, row=0, sticky=E)
        
        self.options.bind('<<ComboboxSelected>>', self.handle_channels)
        
        #top right panel
        buttonsFrame = ttk.Frame(mainframe)
        #print("buttons Frame %s"%type(buttonsFrame))
        buttonsFrame.grid(column=1, row=0,sticky="new")
        ttk.Button(buttonsFrame, text="Load file", command=self.getFileName).grid(column=0, row=0, sticky=(EW))
        ttk.Button(buttonsFrame, text="reset", command=self.clearData).grid(column=1, row=0, sticky=(EW))
        ttk.Button(buttonsFrame, text="refresh", command=self.refreshChannelList).grid(column=0, row=1, sticky=(EW))
        ttk.Button(buttonsFrame, text="plot", command=self.plotData).grid(column=1, row=1, sticky=(EW))
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
        self.options.configure(style='combo.TCombobox')    
            
        
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
            ttk.Label(frame, text="Iteration: %s | %s %s" %(iteration, name, Channel_number),font=self.labelFont, style='unknown.TLabel').grid(column=0, row=0, sticky=("nsw"))
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
    
    def buildFileNamePrefix(self, fileNames):
        print(fileNames)
        prefix = ""
        match = re.search("(\\d+(\\.\\d+)+)", fileNames)
        if match:
            prefix += match.group() + "_"
        if 'NightlyTest' in fileNames:
            prefix += 'nightly_'
        elif 'RebootTest' in fileNames:
            prefix += 'reboot_'
        return prefix
    
    def getFileName(self):
        name = fd.askopenfilename(filetypes=[("csv files", ".csv")],initialdir=self.fileLocation)
        if name != "":
            self.fileLocation = "/".join(name.replace('\\', '/').split("/")[0:-1])
            if not name in self.loadedFileNames:
                self.parseCSV(name)
                self.loadedFileNames.append(name)
            else:
                print("File already loaded")
            #print("prefix: " + self.prefix)
            #print("Current Directory:" + self.fileLocation)
            
            
    
    def parseCSV(self, fileName):
        self.prefix = self.buildFileNamePrefix("/".join(fileName.replace('\\', '/').split("/")[-3:-1]))
        fileD = open(file=fileName, newline='')
        reader = csv.reader(fileD, dialect='excel')
        for row in reader:
            outputType = row[1].lower()
            if outputType == 'output':
                continue
            outputType = self.prefix + outputType
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
        fileD.close()
                        
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
        self.loadedFileNames = []
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
        if loadUrl[:7] != 'http://':
            loadUrl = 'http://' + loadUrl
        print(loadUrl)
        webbrowser.open_new_tab(loadUrl)
       
    def outputDimensions(self):
        print("Width: %d, Height %d"%(self.channelListFrame.winfo_width(), self.channelListFrame.winfo_height()))
        print(self.channelListFrame.grid_size())
        
    def refreshChannelList(self):
        filesToLoad = self.loadedFileNames
        self.clearData()
        pprint(filesToLoad)
        for fileName in filesToLoad:
            self.parseCSV(fileName)
    
    def plotData(self):
        customGreen = (0.166,0.720,0.193,1)
        #pprint(self.outputsCounts)
        barTitles = list(self.outputsCounts.keys())
        passes = np.array(list(self.outputsCounts.values()))
        totals = np.array(list(self.outputsTotals.values()))
        fails = np.zeros(passes.size)
        percentageLabels = []
        for i in range(len(passes)):
            fails[i] = totals[i] - passes[i]
        passFailCounts = {
            "Pass": passes,
            "Fail": fails,
        }
        
        for i in range(passes.size):
            percentageLabels.append(str(np.round(100 * np.round(passes[i] / (totals[i]), 3),3)) + "% \n" + str(passes[i]) + "/" + str(totals[i])) 
            
        
        width = 0.5
        fig = Figure()
        ax = fig.add_subplot()
        bottom = np.zeros(passes.size)
        for category, weight_count in passFailCounts.items():
            if category == "Pass":
                p = ax.bar(barTitles, weight_count, width, label=category, bottom=bottom, color=customGreen ,linewidth=10)
                ax.bar_label(p, label_type='center', labels=percentageLabels)
            if category == "Fail":
                p = ax.bar(barTitles, weight_count, width, label=category, bottom=bottom, color="red",linewidth=10)
            bottom += weight_count
        ax.set_title("STB Results for " + str(date.today()))
        ax.legend(loc="upper right", reverse=True)
        newWindow = Toplevel(root)
        newWindow.title("New Window")
        newWindow.geometry("500x500")
        canvas = FigureCanvasTkAgg(fig, master=newWindow)  # A tk.DrawingArea.
        canvas.draw()
        ax.set_xticklabels(ax.get_xticklabels(), rotation=30, ha='right')
        toolbar = NavigationToolbar2Tk(canvas, newWindow, pack_toolbar=False)
        toolbar.update()
        button_quit = ttk.Button(master=newWindow, text="Quit", command=newWindow.destroy)
        button_test = ttk.Button(master=newWindow, text="test", command= lambda: self.canvasFillerButtonTest(figure=fig, canvas=canvas))
        button_quit.pack(side=tkinter.BOTTOM)
        button_test.pack(side=tkinter.BOTTOM)
        toolbar.pack(side=tkinter.BOTTOM, fill=tkinter.X)
        canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True)
        print(fig)
        
    def canvasFillerButtonTest(self, canvas, figure):
        print(figure)
        print("test Button Pressed")
        ax = figure.gca()
        print(ax)
        ax.cla()
        canvas.draw()
        

        
        
        
root = Tk()
csvReader(root)
root.mainloop()