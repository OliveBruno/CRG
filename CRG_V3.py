#!/usr/bin/env python
# coding: utf-8

#all of this was done using jupyter notebook initally so it is really messy...


from numpy import genfromtxt
from matplotlib.pyplot import plot,title,xlabel,xticks,yticks,show,legend,grid
import seaborn as sns
sns.set()

def Getdatabase():#Gets the info from the data.txt and places everything
                #into separate vectors

    info = input("Nome do arquivo de dados: ")

    info += ".txt"
    
    disci = genfromtxt(info,dtype='str')#database of all disciplines

    disci_code = []
    disci_credits = []
    disci_AP = []
    disci_grades = []
    disci_CA = []
    disci_semester_pre = []
    disci_semester = []
    
    for i in range(len(disci[:,0])):#will ignore all disciplines with codes 8 or 9
        if(int(disci[i,6]) != 8 and int(disci[i,6]) != 9):
            disci_code.append(disci[i,0])
            disci_credits.append(int(disci[i,2]))
            disci_AP.append(disci[i,3])
            disci_grades.append(disci[i,4])
            disci_CA.append(int(disci[i,6]))
            disci_semester_pre.append(disci[i,7])


    #here I create the "semester vector" which will contain the info about what semester (the number) you coursed that discipline
    
    aux = disci_semester_pre[0]
    aux_num = 1
    for i in range(len(disci_semester_pre)):
        if(disci_semester_pre[i] == aux):
            disci_semester.append(aux_num)
        else:
            aux = disci_semester_pre[i]
            aux_num += 1
            disci_semester.append(aux_num)
    
    #here I set the "---" to "0" on the grades list
    
    for i in range(len(disci_grades)):
        if(disci_grades[i] == "---"):
            disci_grades[i] = 0
        else:
            disci_grades[i] = float(disci_grades[i])

    return disci_code,disci_credits,disci_AP,disci_grades,disci_CA,disci_semester

disci_code = []
disci_credits = []
disci_AP = []
disci_grades = []
disci_CA = []
disci_semester_pre = []
disci_semester = []

disci_code,disci_credits,disci_AP,disci_grades,disci_CA,disci_semester = Getdatabase()

def CR_calculator(disci_grades,disci_credits,disci_CA):
    
    CR = 0
    Total_cred = 0
    
    for i in range(len(disci_grades)):
        if(disci_CA[i] == 4 or disci_CA[i] == 5 or disci_CA[i] == 6):
            CR += (disci_grades[i])*(disci_credits[i])
            Total_cred += 10*disci_credits[i]
    
    return CR/Total_cred

def CP_calculator(disci_credits,disci_CA,disci_AP,Total_course):
    
    CP = 0
    
    for i in range(len(disci_credits)):
        if((disci_AP[i] == '+' or disci_AP[i] == '*') and (disci_CA[i] != 5 and disci_CA[i] != 6 and disci_CA[i] != 21 and disci_CA[i] != 0)):
            CP += disci_credits[i]
            
    return CP/Total_course

Total_course = int(input("numero total de creditos no seu curso (Fisica eh 164):"))
print(" ")


def Semester_calculator(disci_grades,disci_credits,disci_CA,disci_AP,Total_course,disci_semester):
    
    CR = [0]
    CR_sem = [0]
    CP = [0]
    
    start = 0
    end = start
    
    while(end<len(disci_semester)):
        
        while((end<len(disci_semester)) and (disci_semester[end] == disci_semester[start])):
            end += 1
        
        CR.append((CR_calculator(disci_grades[0:end],disci_credits[0:end],disci_CA[0:end])))        
        CR_sem.append(CR_calculator(disci_grades[start:end],disci_credits[start:end],disci_CA[start:end]))
        CP.append(CP_calculator(disci_credits[0:end],disci_CA[0:end],disci_AP[0:end],Total_course))
        
        start = end
    
    return CR,CR_sem,CP

CR = []
CR_sem = []
CP = []

CR,CR_sem,CP = Semester_calculator(disci_grades,disci_credits,disci_CA,disci_AP,Total_course,disci_semester)

print("SEM\t   CR\t         CR_sem\t           CP")

for i in range(len(CR)):
    print(i,"\t",'%.4f' % round(CR[i],4),"\t",'%.4f' % round(CR_sem[i],4),"\t",'%.4f' % round(CP[i],4))


print(" ")
print("CR atual =",'%.4f' % CR[len(CR)-1])
if(CP[len(CR)-1] == 1.0):
    print("CP atual =",'%.4f' % CP[len(CR)-1],"\o/ \o/ Parabéns, voce se formou!!! \o/ \o/")
else:
    print("CP atual =",'%.4f' % CP[len(CR)-1])


####THE PLOTTING HAPPENS HERE

xaxis = []

for i in range(len(CP)):
    xaxis.append(round(10000*CP[i]))
    xaxis[i] /= 100
    xaxis[i] = str(xaxis[i])
    xaxis[i] += "%"

plot(CP,CR_sem,"b",label="CRS")
plot(CP,CR,"g",label="CR")

xlabel("CP")
title("Gráfico do CR e CRS em função do CP",loc = "center")
yticks([0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1])
xticks(CP,xaxis,fontsize = 9, rotation ='20')
grid(True)
legend()
show()
