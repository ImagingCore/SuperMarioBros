from Tkinter import *
import tkFileDialog
import BioRad_CSV
import inspect
import time


class CsvGuiClass(Frame):

    # Button labels. String literals. Sizes - all class constants
    SELECT_FILE = "Transform the .csv file"
    EXIT_PROGRAM = "Exit!"
    MAIN_WIN_WIDTH = 380  # not in use
    MAIN_WIN_HEIGHT = 200  # not in use
    INFO_LABEL1 = " -- Option1 -- [in development]"
    INFO_LABEL2 = "  Dual channel BioRad file processing"
    INFO_LABEL3 = "  Single channel BioRad file processing "




    def updateStatus(self,masterIn,statusIn):
    # accepts a string value and displays a flash status at the bottom

        def writeStatus():
            self.status_bar = Label(masterIn, text=statusIn, font=("Arial", 13), fg='darkgreen', bd=1, relief=SUNKEN, anchor=W)
            self.status_bar.grid(row=3, columnspan=2, sticky=W + E)
        def emptyStatus():
            self.status_bar = Label(masterIn, text=" ", font=("Arial", 13), fg='darkgreen', bd=1, relief=SUNKEN, anchor=W)
            self.status_bar.grid(row=3, columnspan=2, sticky=W + E)

        emptyStatus()
        last = 0
        DUR = 800
        for k in range(3):
            masterIn.after(last+DUR, writeStatus)
            last = last + DUR
            masterIn.after(last+DUR, emptyStatus)
            last = last + DUR



    # Opens file selection window. Calls OpeanAndRead from this class (to be altered)
    def Operations(self, optionChoice):


        #  *************** file operations and other action calls to be implemented here ***************
        #
        #                                    FILE OPERATION CALLS
        if optionChoice == 1:
            foo = None
        elif optionChoice == 2:
            foo = None
        elif optionChoice == 3:
            self.filename = tkFileDialog.askopenfilename(filetypes=[("CSV", "*.csv")])
            BioRad_CSV.pivotMe(self.filename)
        else:
            print "INTERNAL ERROR: else condition inside fileSelect"
        #
        #
        #  *********************************************************************************************



    def iconClick(self,masterIn):

        # get the name of the outside function calling iconClick
        calledBy = inspect.currentframe().f_back.f_code.co_name

        def icOn(handle_name):
            handle_name.grid_forget()
            self.start_handle.grid(row=1, columnspan=2, sticky=N)
        def icOff1():
            self.start_handle.grid_forget()
            self.first_handle.grid(row=1, columnspan=2, sticky=N)
        def icOff2():
            self.start_handle.grid_forget()
            self.second_handle.grid(row=1, columnspan=2, sticky=N)
        def icOff3():
            self.start_handle.grid_forget()
            self.third_handle.grid(row=1, columnspan=2, sticky=N)

        # Check against which option is chosen by comparing against\
        #  the name of the function that called iconClick
        if calledBy == "firstOptionClick":
            masterIn.after(25, icOn(self.first_handle))
            masterIn.after(100, icOff1)
            self.updateStatus(masterIn, "   Crunching...")
            self.Operations(1)

        elif calledBy == "secondOptionClick":
            masterIn.after(25, icOn(self.second_handle))
            masterIn.after(100, icOff2)
            self.updateStatus(masterIn, "   Processing...")
            self.Operations(2)

        elif calledBy == "thirdOptionClick":
            masterIn.after(25, icOn(self.third_handle))
            masterIn.after(300, icOff3)
            self.Operations(3)
        else:
            print "INTERNAL ERROR: else condition inside iconClick"


    # Click option actuation functions
    def firstOptionClick(self, event):
        self.iconClick(self.master)
    def secondOptionClick(self, event):
        self.iconClick(self.master)
    def thirdOptionClick(self, event):
        self.iconClick(self.master)


    # Main window layout
    def createWidgets(self,masterIn,versionIn):

        # Version choice (1 or 2) passed in at __init__
        if (versionIn == 1):
            # Image files - GUI version 1
            self.START_F = "./graphics/main_start.gif"
            self.FIRST_F = "./graphics/main_first.gif"
            self.SECOND_F = "./graphics/main_second.gif"
            self.THIRD_F = "./graphics/main_third.gif"
        elif (versionIn == 2):
            # Image files - GUI version 2
            self.START_F = "./graphics/main_start_b.gif"
            self.FIRST_F = "./graphics/main_first_b.gif"
            self.SECOND_F = "./graphics/main_second_b.gif"
            self.THIRD_F = "./graphics/main_third_b.gif"
        elif (versionIn == 3):
            # Image files - GUI version 2
            self.START_F = "./graphics/main_SandD_start.gif"
            self.FIRST_F = "./graphics/main_SandD_first.gif"
            self.SECOND_F = "./graphics/main_SandD_second.gif"
            self.THIRD_F = "./graphics/main_SandD_third.gif"
        elif (versionIn == 4):
            # Image files - GUI version 2
            self.START_F = "./graphics/main_b2_start.gif"
            self.FIRST_F = "./graphics/main_b2_first.gif"
            self.SECOND_F = "./graphics/main_b2_second.gif"
            self.THIRD_F = "./graphics/main_b2_third.gif"
        elif (versionIn == 5):
            # Image files - GUI version 2
            self.START_F = "./graphics/main_b3_start.gif"
            self.FIRST_F = "./graphics/main_b3_first.gif"
            self.SECOND_F = "./graphics/main_b3_second.gif"
            self.THIRD_F = "./graphics/main_b3_third.gif"
        else:
            print "\n Choose the GUI version in CsvGuiClass!... Quitting program."
            exit()

        # Load/initiate all graphics
        self.main_start = PhotoImage(file=self.START_F)
        self.start_handle = Label(masterIn, image=self.main_start)
        self.main_first = PhotoImage(file=self.FIRST_F)
        self.first_handle = Label(masterIn, image=self.main_first)
        self.main_second = PhotoImage(file=self.SECOND_F)
        self.second_handle = Label(masterIn, image=self.main_second)
        self.main_third = PhotoImage(file=self.THIRD_F)
        self.third_handle = Label(masterIn, image=self.main_third)

        # Image display functions called by motionMouse
        def showStart():
            self.start_handle.grid(row=1,columnspan=2, sticky=N)
        def showFirst():
            self.first_handle.grid(row=1,columnspan=2, sticky=N)
            self.first_handle.bind("<Button-1>", self.firstOptionClick)
        def showSecond():
            self.second_handle.grid(row=1,columnspan=2, sticky=N)
            self.second_handle.bind("<Button-1>", self.secondOptionClick)
        def showThird():
            self.third_handle.grid(row=1,columnspan=2, sticky=N)
            self.third_handle.bind("<Button-1>", self.thirdOptionClick)

        # Info bar display functions called by motionMouse
        def infoNone():
            self.stat_label_None.grid(row=2, column=0, sticky=W)
        def infoOne():
            self.stat_label_1.grid(row=2, column=0, sticky=W)
        def infoTwo():
            self.stat_label_2.grid(row=2, column=0, sticky=W)
        def infoThree():
            self.stat_label_3.grid(row=2, column=0, sticky=W)

        # Mouse tracking functionality. Highlighting screen objects
        def motionMouse(event):
            x, y = event.x, event.y
            # position reporter
            #print('{}, {}'.format(x, y))

            if (15 <= x <= 147):
                if (20 <= y <= 158):
                    #print "100<x<150 & 75<y<150"
                    self.start_handle.grid_forget()
                    self.second_handle.grid_forget()
                    self.third_handle.grid_forget()
                    showFirst()
                    self.stat_label_None.grid_forget()
                    self.stat_label_2.grid_forget()
                    self.stat_label_3.grid_forget()
                    infoOne()
                else:
                    foo = None
                    #print "else condition"

            elif (188 <= x <= 332):
                if (20 <= y <= 158):
                    self.start_handle.grid_forget()
                    self.first_handle.grid_forget()
                    self.third_handle.grid_forget()
                    showSecond()
                    self.stat_label_None.grid_forget()
                    self.stat_label_1.grid_forget()
                    self.stat_label_3.grid_forget()
                    infoTwo()
                else:
                    foo = None
                    #print "else condition"

            elif (382 <= x <= 505):
                if (20 <= y <= 158):
                    self.start_handle.grid_forget()
                    self.second_handle.grid_forget()
                    self.third_handle.grid_forget()
                    showThird()
                    self.stat_label_None.grid_forget()
                    self.stat_label_1.grid_forget()
                    self.stat_label_2.grid_forget()
                    infoThree()
                else:
                    foo = None
                    #print "else condition"
            else:
                #print "else condition"
                self.first_handle.grid_forget()
                self.second_handle.grid_forget()
                self.third_handle.grid_forget()
                showStart()
                self.stat_label_1.grid_forget()
                self.stat_label_2.grid_forget()
                self.stat_label_3.grid_forget()
                infoNone()

        # To enable mouse tracking (i.e. root.bind('<Motion>', motionMouse))
        masterIn.bind('<Motion>', motionMouse)

        # Info labels (bottom left)
        self.stat_label_None = Label(masterIn,text=" ", fg='blue')
        self.stat_label_1 = Label(masterIn, text=self.INFO_LABEL1, font=("Arial", 14, "italic"), fg='gray')
        self.stat_label_2 = Label(masterIn, text=self.INFO_LABEL2, font=("Arial", 14, "italic"), fg='black')
        self.stat_label_3 = Label(masterIn, text=self.INFO_LABEL3, font=("Arial", 14, "italic"), fg='black')
        # Exit button (bottom right
        self.button2 = Button(masterIn, text=self.EXIT_PROGRAM, font=("Arial", 16), command=self.quit)
        # Version label (top right)
        self.ver_label_str = "v " + VERSION_NUMBER + ", last updated on " + VERSION_DATE
        self.ver_label = Label(masterIn, text=self.ver_label_str, font=("Arial", 10, "italic"), fg='gray')
        self.status_bar = Label(masterIn, text=" ", font=("Arial", 13), fg='gray', bd=1, relief=SUNKEN, anchor=W)

        # Construct the the main window interface for the first time
        showStart()
        self.stat_label_None.grid(row=2, column=0, sticky=W)
        self.button2.grid(row=2, column=1, sticky=E)
        self.ver_label.grid(row=0,column=1, sticky=E)
        self.status_bar.grid(row=3, columnspan=2, sticky=W + E)


    # Class initialization
    def __init__(self, master=None,version=None):
        Frame.__init__(self, master)
        #master.minsize(width=self.MAIN_WIN_WIDTH, height=self.MAIN_WIN_HEIGHT)
        #master.maxsize(width=self.MAIN_WIN_WIDTH, height=self.MAIN_WIN_HEIGHT)
        self.filename = None
        self.grid()
        self.createWidgets(master, version)



# class FileOps():                # Class currently not implemented
#
#     # Accepts 1) path-file object, 2)the number of rows, 3) number of columns
#     # Performs error checking against .csv extension
#     # Reads the csv file row by row. Prints out results in a "matrix" form
#     # No return
#     def openAndRead(self, file, rows, col):
#         # Error checking. Report an error if not a csv file
#         fileExtention = str(path.basename(file))
#         if (fileExtention[-3:] != "csv"):
#             print "\n Pick a CSV file! \n"
#
#         else:
#             with open(file, "r") as csvfile:
#                 reader = csv.reader(csvfile, delimiter=',')
#                 k = 0;
#                 for row in reader:
#                     while (k < rows):
#                         print (row[0:col])
#                         k = k + 1




def main():

    # Developer: remember to update these!
    global VERSION_DATE
    global VERSION_NUMBER
    VERSION_DATE = "4/15/16"
    VERSION_NUMBER = "2.9"


    # start main GUI window.
    # Instantiate a CsvGuiClass object.
    # Developer: select GUI version (1 or 2)
    root = Tk()
    root.title("Snake Tools")
    mainWindow = CsvGuiClass(master=root, version=5)
    mainWindow.mainloop()


if __name__ == "__main__":
    main()
