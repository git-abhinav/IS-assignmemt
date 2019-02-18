import re    # package for regular expression in python
import glob	 # for accessing all the files in the directory 
import os    # for gettin pwd and removing files that anti-virus finds buggy
import tkinter as tk  # graphical user interface package


current_directory = os.getcwd() # storing current working directory in the string 
print ("Current directory is : ", os.getcwd()) # printing pwd 
print ("\n")   
files_with_bugs = ""  # intializing buggy files list with empty 
for filename in glob.glob('*.py'):  # reading all python files 
    print ("-"*80)                  
    print ("Checking file", filename)# printing file being processed 
    file = open(filename, "r")       # file reference 
    lines = file.readlines()         # reading lines of the source code 
    words = str(lines).split(" ")    # spliting string to words 
    file_content = ""                # intialization
    
    with open(filename) as f:		 # 
        for line in f.readlines():   # storing whole file in one string 
            file_content += line     # 
    red_from_file = file_content     # 
    
    '''
    	checking: 
    	somecode 
    	while some_counter < 0
    	...
    	some_counter-- 
    '''
    if re.match(r'\w{0,100}\s{0,100}while\s{1,100}\w{1,100}\s{0,100}\<\s{0,100}0\s{0,100}\w{0,100}\s{0,100}\w{0,100}\-\-', red_from_file):
        print ("Infinite while loop found in [", filename , "], iterator not incremented")
        files_with_bugs += filename+"\n"
    #red_from_file = file_content
    

    '''
    	checking: 
    	somecode 
    	while some_counter > 0
    	...
    	some_counter++ 
    '''
    if re.match(r'\w{0,100}\s{0,100}while\s{1,100}\w{1,100}\s{0,100}\>\s{0,100}0\s{0,100}\w{0,100}\s{0,100}\w{0,100}\+\+', red_from_file):
            print ("Infinite while loop found in [",filename,  "], iterator not decremented")
            files_with_bugs += filename+"\n"
    #red_from_file = file_content

    '''
    	checking: 
    	somecode 
    	while 123 //some constant number
    	some_counter-- 
    '''
    if re.match(r'\w{0,100}\s{0,100}while\s{1,100}[1-9]{1,10}', red_from_file):
        print( "Infinite loop detected in [", filename, "]", ", while someconstant")#, red_from_file, "}"
        files_with_bugs += filename+"\n"
    #red_from_file = file_content


    #red_from_file = "while TRUE"
    if re.match(r'\w{0,100}\s{0,100}while\s{1,100}TRUE', red_from_file):
        print ("Infinite loop detected in file - ", filename, ", while TRUE")#, red_from_file, "}"
        files_with_bugs += filename + "\n"


    #red_from_file = "while    TRUE     bigcode break"
    #there is chance that loop might break.
    
    if re.match(r'\w{0,100}\s{0,100}while\s{1,100}TRUE\s{1,100}\w{0,100}\s{0,100}break', red_from_file):
        print ("case 5 [",filename , "] may go in Infinite loop")
        files_with_bugs += filename+"\n"

    #checking buffer overflow condition in the source-code

    f = open(filename, "r")
    lines = f.readlines()
    bound = -1; # initializing bound with -1 
    linetemp = "" # 
    for line in lines:
        if line.find("=")!=-1:
            line = line.replace("=", " ")
            line = line.replace(" ", "")
        if re.match(r"\s{0,100}\w{0,100}\s{0,100}\[\d{1,100}\]", line):
            linetemp = line
        if linetemp.find("[")!=-1:
             linetemp = linetemp.replace("[", " ")
        if linetemp.find("]")!=-1:
            linetemp = linetemp.replace("]", " ")
        linetemp = re.sub('[^A-Za-z0-9]+', ' ',linetemp)#extracting the integer part only 
        if bound == -1:   # if bound not set 
            bound = [int(s) for s in linetemp.split() if s.isdigit()]
        else:  # if we know the bound then check if it exceeds or not 
            i = [int(s) for s in linetemp.split() if s.isdigit()]
            if i > bound:
                print ("Buffer over detected in line - ", line, "This index",i,"can't be accessed")
                files_with_bugs += filename+"\n"
def remove_files():
	'''
		objective: to remove buggy files from the current working directory
		input : none 
		output : none 
		approach : we have a list of buggy files 
				   delete file using os package (if file not currently accessed by some other program)
				   and update the GUI and commandline accordingly and
				   updating the log file containing the list of buggy files 
	'''
    title = tk.Label(text="Files removed", font = ("Times New Roman", 18))
    l = files_with_bugs.split(" ")
    print(l) # print list on commandline 
    
    #shutil.rmtree("while_flaw.py")
    #f = open("while_flaw.py")
    #print (f.readlines())
    #f.close()

    #os.remove("while_flaw.py")
    f = open("log.txt", "w")
    f.write(files_with_bugs) 
    f.close()
    #os.remove(files_with_bugs.split("\n"))
    try:  # there may be a chance that the files we want to delete is being acccess by someother process or program 
        file_list = files_with_bugs.split("\n")
        for flist in file_list:
            print(flist)
            if flist != "":
                os.remove(flist)
                files_with_bugs.replace(flist+"\n", "")
    except: # update the commandline about the files that can not be deleted from the DUCKS ;) anti-virus 
        print(files_with_bugs+"can't be accessed, because it is accessed by someother process")
        #update GUI about the situation also 
        title = tk.Label(text="Some files can't be removed", font = ("Times New Roman", 18))
        print("Try something else")
        
    title.grid(column=0, row = 9) #update the GUI 
    
def red_button_pressed():
	'''
	    objective: to take the control of the program to remove_files method to try to delete buggy files 
		input : none 
		output : none
		approach : updating text field with the list of buggy files
				   and updating the GUI accordingly
	'''
    text = tk.Text(master = window, height = 10, width = 30)
    text.grid()
    text.insert(tk.END, files_with_bugs)   #updating text field printed on the GUI 
    button2 = tk.Button(text="Press me to remove bugs", bg="red", command = remove_files) #taking commad to method that deletes the files
    button2.grid(column=0,row = 8)
    
'''
	Making GUI 
'''
window = tk.Tk()
window.title("DUCS Anti-Virus Version 1.00000001") #our copy right 
window.geometry("450x500")   #dimensions 
title = tk.Label(text="Anti-Virus for finding bugs in languages like \npython and R\n", font = ("Times New Roman", 18))
title.grid(column=0, row = 1) # grid system position 
title = tk.Label(text="Working directry is "+current_directory)
title.grid(column=0, row = 2)


button1 = tk.Button(text="Press me to find bugs", bg="red", command = red_button_pressed)
button1.grid(column=0, row = 5)

#text_field = tk.Text(master=window, height=10, width = 30)
#text_field.grid()

window.mainloop()   #do everythin in the window.
