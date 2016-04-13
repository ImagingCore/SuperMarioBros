from Tkinter import *
import tkFileDialog
from os import path
import csv
import BioRad_CSV
import inspect





class CsvGuiClass(Frame):

    # Button labels. String literals. Sizes - all class constants
    SELECT_FILE = "Transform the .csv file"
    EXIT_PROGRAM = "Exit!"
    MAIN_WIN_WIDTH = 380  # not in use
    MAIN_WIN_HEIGHT = 200  # not in use


    # Opens file selection window. Calls OpeanAndRead from this class (to be altered)
    def fileSelect(self,optionChoice):

        #  *************** file operations and other action calls to be implemented here ***************
        #
        #                                    FILE OPERATION CALLS
        if optionChoice == 1:
            print "Option 1: under development"
        elif optionChoice == 2:
            print "Option 2: under development"
        elif optionChoice == 3:
            self.filename = tkFileDialog.askopenfilename(filetypes=[("CSV", "*.csv")])
            BioRad_CSV.pivotMe(self.filename)
        else:
            print "ERROR: else condition inside fileSelect"
        #
        #
        #  *********************************************************************************************


    def iconClick(self,masterIn):

        # get the name of the outside function calling iconClick
        calledBy = inspect.currentframe().f_back.f_code.co_name


        def icOn():
            self.third_handle.grid_forget()
            self.start_handle.grid(row=1, columnspan=2, sticky=N)
        def icOff():
            self.start_handle.grid_forget()
            self.third_handle.grid(row=1, columnspan=2, sticky=N)

            # Check against which option is chosen by comparing against\
            #  the name of the function that called iconClick
            if calledBy == "firstOptionClick":
                self.fileSelect(1)
            elif calledBy == "secondOptionClick":
                self.fileSelect(2)
            elif calledBy == "thirdOptionClick":
                self.fileSelect(3)
            else:
                print "ERROR: else condition inside iconClick"

        masterIn.after(25, icOn)
        masterIn.after(300, icOff)

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

        # Status bar display functions called by motionMouse
        def statNone():
            self.stat_label_None.grid(row=2, column=0, sticky=W)
        def statOne():
            self.stat_label_1.grid(row=2, column=0, sticky=W)
        def statTwo():
            self.stat_label_2.grid(row=2, column=0, sticky=W)
        def statThree():
            self.stat_label_3.grid(row=2, column=0, sticky=W)

        # Mouse tracking functionality. Highlighting screen objects
        def motionMouse(event):
            x, y = event.x, event.y
            # position reporter
            #print('{}, {}'.format(x, y))

            if (18 <= x <= 112):
                if (25 <= y <= 114):
                    #print "100<x<150 & 75<y<150"
                    self.start_handle.grid_forget()
                    self.second_handle.grid_forget()
                    self.third_handle.grid_forget()
                    showFirst()
                    self.stat_label_None.grid_forget()
                    self.stat_label_2.grid_forget()
                    self.stat_label_3.grid_forget()
                    statOne()
                else:
                    foo = None
                    #print "else condition"

            elif (135 <= x <= 233):
                if (20 <= y <= 118):
                    self.start_handle.grid_forget()
                    self.first_handle.grid_forget()
                    self.third_handle.grid_forget()
                    showSecond()
                    self.stat_label_None.grid_forget()
                    self.stat_label_1.grid_forget()
                    self.stat_label_3.grid_forget()
                    statTwo()
                else:
                    foo = None
                    #print "else condition"

            elif (254 <= x <= 350):
                if (20 <= y <= 120):
                    self.start_handle.grid_forget()
                    self.second_handle.grid_forget()
                    self.third_handle.grid_forget()
                    showThird()
                    self.stat_label_None.grid_forget()
                    self.stat_label_1.grid_forget()
                    self.stat_label_2.grid_forget()
                    statThree()
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
                statNone()

        # To enable mouse tracking (i.e. root.bind('<Motion>', motionMouse))
        masterIn.bind('<Motion>', motionMouse)

        # Status labels (bottom left)
        self.stat_label_None = Label(masterIn,text=" ", fg='blue')
        self.stat_label_1 = Label(masterIn, text=" -- Option1 -- [in development]", font=("Arial", 14, "italic"), fg='gray')
        self.stat_label_2 = Label(masterIn, text=" -- Option2 -- [in development]", font=("Arial", 14, "italic"), fg='gray')
        self.stat_label_3 = Label(masterIn, text=" >> BioRad file processing ", font=("Arial", 14, "italic"), fg='blue')
        # Exit button (bottom right
        self.button2 = Button(masterIn, text=self.EXIT_PROGRAM, font=("Arial", 16), command=self.quit)
        # Version label (top right)
        self.ver_label_str = "v " + VERSION_NUMBER + ", last updated on " + VERSION_DATE
        self.ver_label = Label(masterIn, text=self.ver_label_str, font=("Arial", 10, "italic"), fg='gray')

        # Construct the the main window interface for the first time
        showStart()
        self.stat_label_None.grid(row=2, column=0, sticky=W)
        self.button2.grid(row=2, column=1, sticky=E)
        self.ver_label.grid(row=0,column=1, sticky=E)


    # Class initialization
    def __init__(self, master=None,version=None):
        Frame.__init__(self, master)
        #master.minsize(width=self.MAIN_WIN_WIDTH, height=self.MAIN_WIN_HEIGHT)
        #master.maxsize(width=self.MAIN_WIN_WIDTH, height=self.MAIN_WIN_HEIGHT)
        self.filename = None
        self.grid()
        self.createWidgets(master, version)



class FileOps():                # Class currently not implemented

    # Accepts 1) path-file object, 2)the number of rows, 3) number of columns
    # Performs error checking against .csv extension
    # Reads the csv file row by row. Prints out results in a "matrix" form
    # No return
    def openAndRead(self, file, rows, col):
        # Error checking. Report an error if not a csv file
        fileExtention = str(path.basename(file))
        if (fileExtention[-3:] != "csv"):
            print "\n Pick a CSV file! \n"

        else:
            with open(file, "r") as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                k = 0;
                for row in reader:
                    while (k < rows):
                        print (row[0:col])
                        k = k + 1




def main():

    # Developer: remember to update these!
    global VERSION_DATE
    global VERSION_NUMBER
    VERSION_DATE = "4/12/16"
    VERSION_NUMBER = "2.4"


    # start main GUI window.
    # Instantiate a CsvGuiClass object.
    # Developer: select GUI version (1 or 2)
    root = Tk()
    root.title("Snake Tools")
    mainWindow = CsvGuiClass(master=root, version=2)
    mainWindow.mainloop()


if __name__ == "__main__":
    main()
