import re
import glob
import os
import tkinter as tk
current_directory = os.getcwd()
print ("Current directory is : ", os.getcwd())
print ("\n")
files_with_bugs = ""
for filename in glob.glob('*.py'):
    print ("-"*80)
    print ("Checking file", filename)
    file = open(filename, "r")
    lines = file.readlines()
    words = str(lines).split(" ")
    file_content = ""
    with open(filename) as f:
        for line in f.readlines():
            file_content += line
    red_from_file = file_content
    if re.match(r'\w{0,100}\s{0,100}while\s{1,100}\w{1,100}\s{0,100}\<\s{0,100}0\s{0,100}\w{0,100}\s{0,100}\w{0,100}\-\-', red_from_file):
        print ("Infinite while loop found in [", filename , "], iterator not incremented")
        files_with_bugs += filename+"\n"
    red_from_file = file_content
    if re.match(r'\w{0,100}\s{0,100}while\s{1,100}\w{1,100}\s{0,100}\>\s{0,100}0\s{0,100}\w{0,100}\s{0,100}\w{0,100}\+\+', red_from_file):
            print ("Infinite while loop found in [",filename,  "], iterator not decremented")
            files_with_bugs += filename+"\n"
    red_from_file = file_content
    if re.match(r'\w{0,100}\s{0,100}while\s{1,100}[1-9]{1,10}', red_from_file):
        print( "Infinite loop detected in [", filename, "]", ", while someconstant")#, red_from_file, "}"
        files_with_bugs += filename+"\n"
    red_from_file = file_content
    #red_from_file = "while TRUE"
    if re.match(r'\w{0,100}\s{0,100}while\s{1,100}TRUE', red_from_file):
        print ("Infinite loop detected in file - ", filename, ", while TRUE")#, red_from_file, "}"
        files_with_bugs += filename + "\n"
    #red_from_file = "while    TRUE     bigcode break"
    red_from_file = file_content
    if re.match(r'\w{0,100}\s{0,100}while\s{1,100}TRUE\s{1,100}\w{0,100}\s{0,100}break', red_from_file):
        print ("case 5 [",filename , "] may go in Infinite loop")
        files_with_bugs += filename+"\n"
    f = open(filename, "r")
    lines = f.readlines()
    bound = -1;
    linetemp = ""
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
        linetemp = re.sub('[^A-Za-z0-9]+', ' ',linetemp)
        if bound == -1:
            bound = [int(s) for s in linetemp.split() if s.isdigit()]
        else:
            i = [int(s) for s in linetemp.split() if s.isdigit()]
            if i > bound:
                print ("Buffer over detected in line - ", line, "This index",i,"can't be accessed")
                files_with_bugs += filename+"\n"
def remove_files():
    title = tk.Label(text="Files removed", font = ("Times New Roman", 18))
    l = files_with_bugs.split(" ")
    print(l)
    #files_with_bugs.replace("\n", "")
    #os.unlink("while_flaw.py")
    
    #shutil.rmtree("while_flaw.py")
    #f = open("while_flaw.py")
    #print (f.readlines())
    #f.close()
    #os.remove("while_flaw.py")
    f = open("log.txt", "w")
    f.write(files_with_bugs)
    f.close()
    #os.remove(files_with_bugs.split("\n"))
    try:
        file_list = files_with_bugs.split("\n")
        for flist in file_list:
            print(flist)
            if flist != "":
                os.remove(flist)
                files_with_bugs.replace(flist+"\n", "")
    except:
        print(files_with_bugs+"can't be accessed, because it is accessed by someother process")
        title = tk.Label(text="Some files can't be removed", font = ("Times New Roman", 18))
        print("Try something else")
        
    title.grid(column=0, row = 9)
    
def red_button_pressed():
    text = tk.Text(master = window, height = 10, width = 30)
    text.grid()
    text.insert(tk.END, files_with_bugs)
    button2 = tk.Button(text="Press me to remove bugs", bg="red", command = remove_files)
    button2.grid(column=0,row = 8)
    
window = tk.Tk()
window.title("DUCS Anti-Virus Version 1.00000001")
window.geometry("450x500")
title = tk.Label(text="Anti-Virus for finding bugs in languages like \npython and R\n", font = ("Times New Roman", 18))
title.grid(column=0, row = 1)
title = tk.Label(text="Working directry is "+current_directory)
title.grid(column=0, row = 2)


button1 = tk.Button(text="Press me to find bugs", bg="red", command = red_button_pressed)
button1.grid(column=0, row = 5)

#text_field = tk.Text(master=window, height=10, width = 30)
#text_field.grid()

window.mainloop()   #do everythin in the window.