################################################################################
# UNDER NO CIRCUMSTANCES SHALL THE CREATOR OF THIS SOFTWARE, OR DEVELOPERS, 
# OR CONTRIBUTORS, BE LIABLE FOR PERSONAL INJURY, OR ANY INCIDENTAL, SPECIAL, 
# DIRECT OR INDIRECT OR CONSEQUENTIAL DAMAGES WHATSOEVER, INCLUDING WITHOUT 
# LIMITATION, DAMAGES FOR LOSS OF PROFITS, LOSS OF DATA, BUSINESS INTERRUPTION 
# OR ANY OTHER COMMERCIAL DAMAGES OR LOSSES, ARISING FROM OR RELATED TO THE 
# USE OR INABILITY TO USE THIS SOFTWARE.  USE THIS SOFTWARE AT YOUR 
# OWN RISK OR DO NOT USE IT! USING THIS SOFTWARE IMPLIES ACCEPTANCE OF FULL 
# RESPONSIBILITY FOR IT'S CONSEQUENCES.
################################################################################

import tkinter as tk
from tkinter import messagebox
import time
from datetime import datetime
import os
import shutil

class SystemPropertiesClass:
    #   System properties ...that is System global variables
    GlobalAbort=False
    GlobalDebug= False      #debug = True takes 6.13 times as long!
    GlobalSystemInited=False
    GlobalVersionStr="Version = -1"
    

#################################################
#################################################
####   S T A R T  O F   U S E R   C O D E
####   S T A R T  O F   U S E R   C O D E
####

def is_hidden_file(file_path):
    # macOS (Unix-based) uses a leading dot in the file name
    return os.path.basename(file_path).startswith('.')
              
def AppWindowInits():
    ### THE FOLLOWING IS AN EXAMPLE OF AN APPLICATION ADDING A TEXT BOX TO THE APP WINDOW 
    System.NewBackupLocationLabel = tk.Label(anchor="w", justify="left",text=r"Incremental Backup Location (example:  /MyBackups)", font = "courier 9 bold", bg="gray94")
    System.NewBackupLocationLabel.place(x=3,y=90)

    ### THE FOLLOWING IS AN EXAMPLE OF AN APPLICATION ADDING A TEXT BOX TO THE APP WINDOW 
    System.NewBackupLocation = tk.Entry(justify="left",font = "courier 9", bg="white",width=80)
    System.NewBackupLocation.place(x=3,y=110)
    #System.NewBackupLocation.insert(0, r"F:\IncBackup")

    System.FullBackupLocationLabel = tk.Label(anchor="w", justify="left",text=r"Full Backup Location (example:  /FullBackups)", font = "courier 9 bold", bg="gray94")
    System.FullBackupLocationLabel.place(x=3,y=140)
    System.FullBackupLocation = tk.Entry(justify="left",font = "courier 9", bg="white",width=80)
    System.FullBackupLocation.place(x=3,y=160)
    #System.FullBackupLocation.insert(0, r"F:\newREFBACKUP\fldr0")
    # G:\PC Backup 2024 03-05 No Music-No Work C

    System.ChangedLocationLabel = tk.Label(anchor="w", justify="left",text=r"Changed Files to be backed up (example: /MyDataFiles)", font = "courier 9 bold", bg="gray94")
    System.ChangedLocationLabel.place(x=3,y=190)
    System.ChangedLocation = tk.Entry(justify="left",font = "courier 9", bg="white",width=80)
    System.ChangedLocation.place(x=3,y=210)

    # Read the 3 paths in from the file 'MACdefaultpaths.txt', to save user time.
    if os.path.exists("MACdefaultpaths.txt"):
        file = open("MACdefaultpaths.txt",'r')
        
        ReadLine = file.readline()
        ReadLine=ReadLine.strip()
        System.NewBackupLocation.insert(0, ReadLine)
        
        ReadLine = file.readline()
        ReadLine=ReadLine.strip()
        System.FullBackupLocation.insert(0, ReadLine)

        ReadLine = file.readline()
        ReadLine=ReadLine.strip()
        System.ChangedLocation.insert(0, ReadLine)
        file.close()

def AppStart():
    StartT = time.time()
    TimeStart = datetime.now()
    TimeStartStr = TimeStart.strftime("%Y %m %d %H:%M:%S")
    print("TIME = ",TimeStartStr)

    FileCtr=0
    current_time = time.localtime()
    
    path=System.ChangedLocation.get()
    changed_path = r'{}'.format(path)
    
    path=System.FullBackupLocation.get()
    reference_path = r'{}'.format(path)
    
    path=System.NewBackupLocation.get()
    TimeStartStr = TimeStart.strftime("%Y %m-%d")
    TimeStartStr = TimeStartStr + ' INC'
    backup_path = '{}\\{}'.format(path, TimeStartStr)
    print(backup_path)


    # Create the backup folder if it doesn't exist
    if not os.path.exists(backup_path):
        print("backup not exist-",backup_path) 
        os.makedirs(backup_path)

    # Open or create the CHANGES.txt file to log changes
    with open(os.path.join(backup_path, 'CHANGES.txt'), 'w') as changes_file:
        # Walk through the files and folders in the changed folder
        for root, dirs, files in os.walk(changed_path):
            # Iterate through each file
            for file in files:
                FileCtr = FileCtr + 1
                Banner2(FileCtr)
                System.update()
                System.update_idletasks()

                if SystemProperty.GlobalAbort :
                    Banner1("GlobalAbort...Exit")
                    break

                changed_file_path = os.path.join(root, file)
                if is_hidden_file(changed_file_path) :
                    print(f"HIDDEN FILE= '{changed_file_path}' ")
                else:

                    relative_path = os.path.relpath(changed_file_path, changed_path)
                    reference_file_path = os.path.join(reference_path, relative_path)
                    if SystemProperty.GlobalDebug :
                        print("FILE=", file)
                        print("FILE: changed_path  ", changed_path)
                        print("FILE: relative_path  ", relative_path)
                        print("FILE: RefFilePath      ", reference_file_path)
                
                    # Check if the file exists in the reference folder
                    if not os.path.exists(reference_file_path):
                        # If not, copy it to the backup folder
                        if SystemProperty.GlobalDebug :
                            print("FILE: NEW  no ref path,backup path=", backup_path)
                            print("FILE: ChangedfilePath  ", changed_file_path)
                        shutil.copy2(changed_file_path, backup_path)
                        # Log the change in the changes.txt file
                        changes_file.write(f"Added File: {relative_path}\n")
                    else:
                        # Compare timestamps of the file
                        # I see about 3600 difference in PCs. This is in secs. For MACs use 30secs until feedback indicates a better number. 
                        reference_timestamp = os.path.getmtime(reference_file_path)
                        changed_timestamp = os.path.getmtime(changed_file_path)
                        if SystemProperty.GlobalDebug :
                            print("FILE: RefFilePath      ", reference_file_path)
                            print("FILE: ChangedfilePath  ", changed_file_path)
                            print("FILE: RefTIMESTAMP      ", reference_timestamp)
                            print("FILE: Changed TIMESTAMP ", changed_timestamp)
                        # If timestamps are different, copy the file to the backup folder
                        # For some reason the timestamp on Flash drive is a couple secs different than C:\. Dont know why.
                        if (abs(reference_timestamp - changed_timestamp ) > 30) :
                        #if reference_timestamp != changed_timestamp:
                            if SystemProperty.GlobalDebug :
                                print("FILE: TIMESTAMP  ,backup path", backup_path)
                            backup_file_path = os.path.join(backup_path, relative_path)
                            #shutil.copy2(changed_file_path, backup_file_path)
                            shutil.copy2(changed_file_path, backup_path)
                            # Log the change in the changes.txt file
                            changes_file.write(f"Modified: {relative_path}\n")
                    
            # Iterate through each folder
            for folder in dirs:
                FileCtr = FileCtr + 1
                Banner2(FileCtr)
                System.update()
                System.update_idletasks()
 
                if SystemProperty.GlobalAbort :
                    Banner1("GlobalAbort...Exit")
                    break

                changed_folder_path = os.path.join(root, folder)
                relative_path = os.path.relpath(changed_folder_path, changed_path)
                reference_folder_path = os.path.join(reference_path, relative_path)
                if SystemProperty.GlobalDebug :
                    print("FOLDER=",folder)
                    print("changed_folder_path=", changed_folder_path)
                    print("relative_path=", relative_path)
                    print("reference_folder_path=", reference_folder_path)
                
                # Check if the folder exists in the reference folder
                if not os.path.exists(reference_folder_path) :
                #if ((not os.path.exists(reference_folder_path) ) and ( (not os.path.exists(reference_folder_path) ):
                    # If not, copy it to the backup folder
                    backup_folder_path = os.path.join(backup_path, relative_path)
                    if not os.path.exists(backup_folder_path) :
                        if SystemProperty.GlobalDebug :
                            print("No Ref Folder:backup_folder_path=", backup_folder_path)
                            print("No Ref Folder:changed_folder_path=", changed_folder_path)
                            print("No Ref Folder:backup_path=", backup_path)
                        shutil.copytree(changed_folder_path, backup_folder_path)
                        # Log the change in the changes.txt file
                        changes_file.write(f"Added Folder: {relative_path}\n")

    TimeStop = datetime.now()
    TimeStopStr = TimeStop.strftime("%Y %m %d %H:%M:%S")
    print("TIME = ",TimeStopStr)
    
    StopT = time.time()
    elapsedT = StopT-StartT
    format_float = "{:.2f}".format(elapsedT)
    Banner1("Done...   Elapsed time " + format_float + "secs")


####
#### E N D   O F   U S E R / A P P   C O D E 
#################################################
#################################################


#################################################
#################################################
####   S Y S T E M    C O D E    S T A R T S
####
def clickStart():
    SystemProperty.GlobalAbort = False
    Banner1("Started...")
    #SystemStart()
    AppStart()

def clickAbort():
    Banner1("Aborted")
    SystemProperty.GlobalAbort = True

def clickDebug():
    if SystemProperty.GlobalDebug :
        SystemProperty.GlobalDebug = False
        System.DebugBtn['text'] = "Debug =OFF"
    else :
        SystemProperty.GlobalDebug = True
        System.DebugBtn['text'] = "Debug =ON "
    System.update()
    System.update_idletasks()
    
def clickVersion():
    messagebox.showinfo(title="Version info", message=SystemProperty.GlobalVersionStr)    
   
def Banner1(StrIn):
    System.ScreenBanner1["text"]=StrIn

def Banner2(StrIn):
    System.ScreenBanner2["text"]=StrIn

def donothing():
    Banner1("Not implemented")

def exitProgram():
    exit()

def SystemVariableInits():
    SystemProperty.GlobalDebug = False
    SystemProperty.GlobalAbort=False
    SystemProperty.GlobalSystemInited=False
    root.update()              

def SystemWindowInits():
    System.ScreenBanner1 = tk.Label(anchor="w", justify="left",text="Starting...", font = "courier 20 bold", bg="white",width=40)
    System.ScreenBanner1.place(x=0,y=0)
    System.ScreenBanner2 = tk.Label(anchor="w", justify="left",text="", font = "courier 20 bold", bg="white",width=40)
    System.ScreenBanner2.place(x=0,y=40)

    StartBtn=tk.Button(text="START",width = 7)
    StartBtn["command"] = clickStart
    StartBtn.place(x=400,y=280)
                            
    AbortBtn=tk.Button(text="ABORT",width = 7)
    AbortBtn["command"] = clickAbort
    AbortBtn.place(x=475,y=280)

    System.DebugBtn=tk.Button(text="Debug",width = 11)
    System.DebugBtn["command"] = clickDebug
    System.DebugBtn.place(x=3,y=280)
    if SystemProperty.GlobalDebug :
        System.DebugBtn['text'] = "Debug =ON"
    else :
        System.DebugBtn['text'] = "Debug =OFF"


    MenuBar = tk.Menu(root)
    filemenu = tk.Menu(MenuBar,tearoff=0)
    filemenu.add_command(label="Version",command=clickVersion)
    filemenu.add_command(label="Exit",command=exitProgram)
    MenuBar.add_cascade(label="File",menu=filemenu)
  
    root.config(menu=MenuBar)

    # version   date        comments
    # 0.01      04/18/2024  Creating the First MAC GUI for incremental backup, from Windows version.
    # 0.02      04/23/2024  Changed GUI label to reflect Mac folders.
    #                           
    SystemProperty.GlobalVersionStr="Version 0.01  04/18/2024"
    SystemProperty.GlobalVersionStr="Version 0.02  04/23/2024"
    Banner2(SystemProperty.GlobalVersionStr)
####
#### E N D   O F   S Y S T E M   C O D E 
#################################################
#################################################
    
    
#################################################
#################################################
##    PROGRAM STARTS
##    RUNNING HERE
##

root = tk.Tk()
root.geometry("640x310")
root.resizable(0,0)   # disable window resizing

System=root
System.title('FSIB   Friendly Simple Incremental Backup')

# SYSTEM INITIALIZATIONS HERE
SystemProperty = SystemPropertiesClass()  #only create this instance once!!
SystemVariableInits()
SystemWindowInits()

Banner1("Ready")

while (SystemProperty.GlobalAbort == False):
    if (SystemProperty.GlobalSystemInited == False):
        #AFTER WINDOW INITIALIZATIONS ARE DONE
        #VARIABLE AND HARDWARE INITIALIZATIONS ARE DONE HERE
        #SO THAT ANYTHING TO BE DISPLAYED IN THEM CAN BE SHOWN
        #SystemVariableInits()
        AppWindowInits()
        SystemProperty.GlobalSystemInited = True
        
    root.update()
    root.update_idletasks()

