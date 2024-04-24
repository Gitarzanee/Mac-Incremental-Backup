***  By using this software, you agree that the developers and contributors shall not be held liable for any damages, including but not limited to direct, indirect, incidental, special, or consequential damages arising from the use of this software or inability to use it (even if advised of the possibility of such damages), unless required by applicable law. Use this software at your own risk.  ***

MAC INCREMENTAL BACKUPS USER MANUAL  (GUI version) 

        2024 04-02	Initial 
        2024 04-23	Revised for GUI version

Overview
This is documentation for an easy to use, python program, that does incremental backups for Macs.  The idea is to have a friendly way for a person with a Mac to easily backup their home files and data.  (It is not intended as an enterprise or network solution!)  The intended use case is a person that wants to backup their Mac data to a flash drive or external drive.  Full backups, backing up everything, from one location to another,  is easy to do and is NOT implemented at this time.  What is implemented is an easy way to backup everything that has changed, since the full backup was done.   A reasonable use case would be to do a FULL backup once or twice a month, and do the incremental backups every day  or two, until the next FULL backup.  Incremental backups, backup everything that has changed since the full backup. 

One major advantage of this program is the privacy.  When an ‘.exe’ program is run, it is difficult to tell if data is being sent over the internet…and who the recipients might be.  With this python program, as with open source, one can see from the code, that there are no shenanigans going on.

Background
My use case was a home PC, with ~20GB of data files, and I might add or edit several files every day.  These files might be pictures, audio, documents, programs, spreadsheets, etc.  I did not want to do full backups every day as that is a lot of memory, and it took hours to do a FULL backup!  I spend a lot of time doing research and creating these files, so the data is very valuable to me.  I think there are many home users that have the same needs and use case.


USER INSTRUCTIONS

Quick Start

Before using the program, a full backup must be done.  That is, copy all of your data files to some backup location.   Note this location, as we will need it for the incremental backup later.

Edit and add to your data files, as needed.  When some files have changed, or been added, you will be ready to do the incremental backup:

1.	Run the Python program.
2.	Set up a location for the backed up files to be placed.  Then enter this path underneath the label that says “Incremental Backup Location”.  That is the location that the program will put the changed files and folders.  Note:  A folder will automatically be created there with a name of this format “YYYY mm-dd INC”.  I.e. “2024 04-23 INC”. 
3.	 Enter the location of the full backup under the label “Full Backup Location”.
4.	Under the label “Changed Files to be backed up”, enter the location of the data files that have been changed.  The ones that have been changed, will be backed up.

NOTE: As an alternative to steps 2,3,4 above.   The three paths can be set up in the text file “MACdefaultpaths.txt”.
The program only looks at the first three lines.  If you use the same locations each time, this will save time entering in the paths each time the program is run.  The file “MACdefaultpaths.txt”, must be in the same location as the python program.


RESULTS

First, if any folders have been changed or added, you will see them in the backup folder. 

Second, any files that have been changed or added, will be put in the root of the backup folder.

Additionally, the program creates, in the backup_folder, a “CHANGES.txt” file.  This is a log file contain the names and paths of files and folders, that have changed/added, and will describe whether they were “Modified” or “Added”.  This will aid in reconstructing the file structure if the hard drive crashes.

DETAILED INSTRUCTIONS
To be determined.

