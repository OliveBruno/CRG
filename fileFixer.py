import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox as msg

def fix(file):

    Turmas = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    Creditos = ["01","02","03","04","05","06","07","08","09","10","16"]
    Symbols = ['+','X','*','-']

    with open(file,'r') as f:
        fileData = f.readlines()

    for i in range(len(fileData)):

        fileData[i] = fileData[i].replace(",",".")
        fileData[i] = fileData[i].replace('\t',' ')
        
        if(fileData[i][0] == 'F' and fileData[i][1] == ' '):
            fileData[i] = 'F' + fileData[i][2:]

        if(not(fileData[i].split(" ")[1] in Turmas)):

            newFileData = fileData[i].split(" ")[0]+ " A"
            
            for j in range(1,len(fileData[i].split(" "))):
                
                newFileData += " " + fileData[i].split(" ")[j]

            fileData[i] = newFileData

        if(not(fileData[i].split(" ")[2] in Creditos)):

            newFileData = fileData[i].split(" ")[0]+" "+ fileData[i].split(" ")[1] + " 04"
            
            for j in range(2,len(fileData[i].split(" "))):
                
                newFileData += " " + fileData[i].split(" ")[j]

            fileData[i] = newFileData
            

        if(not(fileData[i].split(" ")[3] in Symbols)):

            newFileData = fileData[i].split(" ")[0]+" "+ fileData[i].split(" ")[1] + " " + fileData[i].split(" ")[2] + " -"
            
            for j in range(3,len(fileData[i].split(" "))):
                
                newFileData += " " + fileData[i].split(" ")[j]

            fileData[i] = newFileData

        fileData[i] = fileData[i].replace(' ','\t')
        

    with open(file.strip(".txt")+"Fixed.txt",'w') as f:
        f.writelines(fileData)

    
if(__name__ == "__main__"):

    root = tk.Tk()
    root.withdraw()

    file = filedialog.askopenfilename()
    
    fix(file)

    root.quit()
    root.destroy()


#end of the code
