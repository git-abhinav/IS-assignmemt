---
output:
  html_document: default
  word_document: default
  pdf_document: default
---
# READ ME file for DUCS &copy; Anti-Virus Version 1.00000001

> **DUCS Anti-Virus finds the bugs in the source-code using regular expression**

_Programming is done in "Python"
It uses many python packages, such as_ : 

* os - _for removing files, working directory_
* glob - _accessing all files in the working directory_ 
* re - _for regular expression_
* tkinter - _for graphical user interface_

> **What DUCS &copy; antivirus finds** 

* finds abnormality in while loop, that may cause the loop to iterate infinitly, example : while TRUE 
* while someconstant 
* while counter < 0 
{ counter - - }
* while counter > 0 
{ counter + + }
* while TRUE { with break condition}, there is a chance that it may iterate infinitly 
* buffer overflow condition, example int buffer[5], after some lines of code the program tries to access location > 5, i.e.  buffer[50]

> **Actions taken on buggy files detected by DUCS &copy; anti-virus** 

* The program tries to remove buggy files 
* If somehow the files are currently access by the other process(can't be deleted then), their log is maitained in _log.txt_ file 

> **Function written in the program**

1. remove_files():
    + removes buggy files using os package's remove function 
    list is buggy files is maintained in string variable _files_with_bugs_
2. red_button_pressed():
    + updating text field with the list of buggy files and updating the GUI accordingly
		+ using text = tk.Text(master = window, height = 10, width = 30)
		+ text.insert(tk.END, files_with_bugs), _insert list to the GUI_
3. Proper exception handling is done in the program using try: and except in code, otherwise program __may crash__ while deleting buggy files. 

> **Program FAQ**

* It uses an external package __tkinter__ that needs to be installed using _pip install tkinter_ make sure that your __environment variables__ are properly set for python 
* Program is compiled to be a executable too, there are 2 executable files
    + __AntiVirus-commandline.exe__, it _printing details_ on _cmd or terminal_ depending opon the OS along with the _GUI_, (details including exception and file deletion details).
    + __AntiVirus-simple.exe__, it provides only GUI with no commandline.
* This program will run on both Python 2.X and 3.X
    