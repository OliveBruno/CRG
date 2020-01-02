import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox as msg
from numpy import genfromtxt
from matplotlib.pyplot import plot,title,xlabel,xticks,yticks,show,legend,grid,tight_layout
import seaborn as sns
sns.set()

class CR_Calculator:
    
    def __init__(self,filePath,totalCourse):

        self.filePath = filePath
        self.totalCourse = totalCourse#total number of credits in your course
        
        self.code = []
        self.credits = []
        self.AP = []
        self.grades = []
        self.CA = []
        self.semester = []

        self.Getdatabase()
        self.CR,self.CR_sem,self.CP = self.Calculate()
    
    def Getdatabase(self):#Gets the info from the data.txt and places everything
                    #into separate arrays

        disci = genfromtxt(self.filePath,dtype='str')#database of all disciplines

        semester_pre = []
        
        for i in range(len(disci[:,0])):#will ignore all disciplines with codes 8 or 9
            if(not(int(disci[i,6]) in [8,9])):
                self.code.append(disci[i,0])
                self.credits.append(int(disci[i,2]))
                self.AP.append(disci[i,3])
                self.grades.append(disci[i,4])
                self.CA.append(int(disci[i,6]))
                semester_pre.append(disci[i,7])


        #here I create the "semester array" which will contain the info about what semester (as a number) you took each discipline
        
        aux = semester_pre[0]
        aux_num = 1
        for i in range(len(semester_pre)):
            if(semester_pre[i] == aux):
                self.semester.append(aux_num)
            else:
                aux = semester_pre[i]
                aux_num += 1
                self.semester.append(aux_num)
        
        #here I set the "---" to "0" on the grades array
        
        for i in range(len(self.grades)):
            if(self.grades[i] == "---"):
                self.grades[i] = 0
            else:
                try:
                    self.grades[i] = float(self.grades[i])
                except:
                    self.grades[i] = float(self.grades[i].replace(",","."))
                    

    def getCR( self, disci_grades, disci_credits,disci_CA):#calculates the CR
    
        CR = 0
        Total_cred = 0
        
        for i in range(len(disci_grades)):
            if( disci_CA[i] in [4,5,6] ):#the only codes that matter are 4,5 and 6
                CR += (disci_grades[i])*(disci_credits[i])
                Total_cred += 10*disci_credits[i]
        
        return CR/Total_cred
    

    def getCP( self, disci_credits , disci_CA, disci_AP):#calculates the CP
            
        CP = 0
    
        for i in range(len(disci_credits)):
            if( (disci_AP[i] in ['+','*']) and (not(disci_CA[i] in [5,6,21,0])) ):
               
                CP += disci_credits[i]
            
        return CP/self.totalCourse

    def CPtoPercent(self):#transforms the CP data from a float to a string with 2 decimal places and a '%' at the end
        cpPercent = []

        for i in range(len(CP)):
            cpPercent.append(round(10000*self.CP[i]))
            cpPercent[i] /= 100
            cpPercent[i] = str(cpPercent[i])
            cpPercent[i] += "%"

        return cpPercent
        

    def Calculate(self):
    
        CR = [0]
        CR_sem = [0]
        CP = [0]
        
        start = 0
        end = start
        
        while(end<len(self.semester)):
            
            while((end<len(self.semester)) and (self.semester[end] == self.semester[start])):
                end += 1
            
            CR.append((self.getCR(self.grades[0:end],self.credits[0:end],self.CA[0:end])))        
            CR_sem.append(self.getCR(self.grades[start:end],self.credits[start:end],self.CA[start:end]))
            CP.append(self.getCP(self.credits[0:end],self.CA[0:end],self.AP[0:end]))
            
            start = end
        
        return CR,CR_sem,CP

### end of the CR_Calculator object ###

def printCRTable(CR,CR_sem,CP):
    
    print("SEM\t   CR\t         CR_sem\t           CP")

    for i in range(len(CR)):
        print(i,"\t",'%.4f' % round(CR[i],4),"\t",'%.4f' % round(CR_sem[i],4),"\t",'%.4f' % round(CP[i],4))


    print(" ")
    print("CR atual =",'%.4f' % CR[len(CR)-1])
    if(CP[len(CR)-1] == 1.0):
        print("CP atual =",'%.4f' % CP[len(CR)-1],"\o/ \o/ Parabéns, voce se formou!!! \o/ \o/")
    else:
        print("CP atual =",'%.4f' % CP[len(CR)-1])
        

def askSaveCRTable(CR,CR_sem,CP):

    root = tk.Tk()
    root.withdraw()

    answer = msg.askyesno("Save ?","Save the table data in a .txt file ?")

    root = tk.Tk()
    root.withdraw()

    if(answer):

        save_as = filedialog.asksaveasfilename(filetypes = (("txt files","*.txt"),("all files","*.*"))).replace(" ","_")

        if(not(".txt" in save_as)):
            save_as += ".txt"
    
        with open(save_as,"w+") as f:
            f.write("SEM\tCR\tCR_sem\tCP\n")
                
            for i in range(len(CR)):
                f.write(str(i)+"\t"+str('%.4f' % round(CR[i],4))+"\t"+str('%.4f' % round(CR_sem[i],4))+"\t"+str('%.4f' % round(CP[i],4))+"\n")


            f.write("\nCR atual = "+str('%.4f' % CR[len(CR)-1])+"\n")

            if(CP[len(CR)-1] == 1.0):
                f.write("CP atual = "+str('%.4f' % CP[len(CR)-1])+" \o/ \o/ Parabéns, voce se formou!!! \o/ \o/\n")
            else:
                f.write("CP atual = "+str('%.4f' % CP[len(CR)-1])+"\n")

    root.quit()
    root.destroy()

def askDataFilePath():

    root = tk.Tk()
    root.withdraw()

    filePath = filedialog.askopenfilename()

    root.quit()
    root.destroy()

    return filePath

#
#
#
#
#
#
#
#
#


if(__name__ == "__main__"): ## code starts here ##

    try:
        totalCourse = int(input("numero total de creditos no seu curso (Fisica eh 164):"))
        print(" ")

        if(totalCourse < 80):#defaults to Physics basically
            totalCourse = 164
    except:
        totalCourse = 164
    
    filePath = askDataFilePath()

    studentData = CR_Calculator(filePath,totalCourse = totalCourse)

    CR = studentData.CR
    CR_sem = studentData.CR_sem
    CP = studentData.CP

    
    printCRTable(
                 studentData.CR,
                 studentData.CR_sem,
                 studentData.CP
                 )


    ####THE PLOTTING HAPPENS HERE

    plot(CP,CR_sem,"-o",color = 'b',label="CRS")
    plot(CP,CR,"-o",color = 'g',label="CR")

    xlabel("\n CP")
    title("Gráfico do CR e CRS em função do CP",loc = "center")
    yticks([0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1])
    xticks([0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1])
    #xticks(CP,xaxis,fontsize = 9, rotation ='20')
    grid(True)
    tight_layout()
    legend()
    show()
    

    ### FINALLY THIS ###
    askSaveCRTable(CR,CR_sem,CP)


