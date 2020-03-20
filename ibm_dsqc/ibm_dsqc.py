############################################                                  
## Title: IBM Domain-Specific Compiler    ##                                  
## Author: Sahil Gulania, Lindsay Bassman,##                                  
##         Connor Powers                  ##                                  
## Date: 03/19/2020 ########################                                  
                                                                                
import numpy as np                                                              
                                                                                
from qiskit import qiskit_code                                                  
from rigetti import rigetti_code

### This code assumes qubits are labeled 0,1,2,...,N and connected in that order ###

lineList = [line.rstrip('\n') for line in open("advance_gates.txt")]
count = len(lineList)

#Read the gate in right vector form
# G = Gate type
# TH = Angle of rotation ! if no angle rotation then TH = 0
# TH2 = 2nd angle of rotation (used in U2 and U3 gates)
# TH3 = 3rd angle of rotation (used in U3 gates)
# AC1 = qubit on which action is happening
# AC2 = qubit on which controlled action is happening

G = ["" for x in range(count)]
G = list(G)
AC1 = np.zeros(shape=(count),dtype=np.int) 
AC2 = np.zeros(shape=(count),dtype=np.int) 
TH = np.zeros(shape=(count))
for i in range (0,count):
  G[i] = 0
  TH[i] = 0
  AC1[i] = 0
  AC2[i] = 0 
  if lineList[i][0:1] == "H":
    G[i]="H"
    TH[i] = 0
    AC1[i] = lineList[i][2:3]
    AC2[i] = 0
  if lineList[i][0:2] == "RZ":
    G[i] = "RZ"
    TH[i] = lineList[i][lineList[i].find("(")+1:lineList[i].find(")")]
    AC1[i] = lineList[i][-1]
    AC2[i] = 0
  if lineList[i][0:4] == "CNOT":
    G[i] = "CNOT"
    TH[i] = 0
    AC1[i] = lineList[i][5:6] 
    AC2[i] = lineList[i][7:8]
  if lineList[i][0:7] == "MEASURE":
    G[i] = "MEASURE"
    TH[i] = 0
    AC1[i] = 0
    AC2[i] =0 

   
nqubits = max(max(AC1),max(AC2))
 
#Omit last and second-to-last CNOT for each qubit
for qub in range(0,nqubits+1):
    i=-1
    count=0
    while count<=1 and i>=-int(len(G)):
        if G[i] == "CNOT" and AC1[i]==qub and AC2[i]==qub+1:
            del G[i]
            TH=np.delete(TH,i)
            AC1=np.delete(AC1,i)
            AC2=np.delete(AC2,i)
            count=count+1
        i=i-1

#Omit last RZ for each qubit
for qub in range(0,nqubits+1):
    i=-1
    while i>=-int(len(G)):
        if G[i] == "H" and AC1[i]==qub:
            break
        if G[i] == "RZ" and AC1[i]==qub:
            G[i]  = "NULL"
            break
        i=i-1            
        
        
#Use CNOT (0,1) ->  H(0) H(1) CNOT(1,0) H(0) H(1)
i=0
while G[i] != "MEASURE":
    if G[i]=="CNOT" and (G[i+1]=="H" and G[i+2]=="H" and AC1[i+1]==AC1[i] and AC1[i+2]==AC2[i])==False:
        G[i]="H"
        flag1=int(AC1[i])
        flag2=int(AC2[i])
        AC2[i]=0
        G.insert(i,"H")
        TH=np.insert(TH,i,0)
        AC1=np.insert(AC1,i,flag2)
        AC2=np.insert(AC2,i,0)
        G.insert(i,"CNOT")
        TH=np.insert(TH,i,0)
        AC1=np.insert(AC1,i,flag2)
        AC2=np.insert(AC2,i,flag1)
        G.insert(i,"H")
        TH=np.insert(TH,i,0)
        AC1=np.insert(AC1,i,flag1)
        AC2=np.insert(AC2,i,0)
        G.insert(i,"H")
        TH=np.insert(TH,i,0)
        AC1=np.insert(AC1,i,flag2)
        AC2=np.insert(AC2,i,0)
    i=i+1

#Rearrange circuits to put successive Hadamard gates in order
i=0
while G[i] != "MEASURE":
    if G[i]=="H":
        flag=AC1[i]
        j=i+1
        boolean=0
        while G[j] != "MEASURE" and boolean ==0:
            if AC1[j]==flag and G[j] == "H":
                boolean=1
                del G[j]
                TH=np.delete(TH,j)
                AC1=np.delete(AC1,j)
                AC2=np.delete(AC2,j)
                G.insert(i,"H")
                TH=np.insert(TH,i,0)
                AC1=np.insert(AC1,i,flag)
                AC2=np.insert(AC2,i,0)
            if AC1[j]==flag and G[j] != "H":
                break
            j=j+1
    i=i+1


#Use successive Hadamard annihilation
i=0
while G[i]!= "MEASURE":
    if G[i]=="H" and G[i+1] == "H" and AC1[i]==AC1[i+1]:
        del G[i]
        TH=np.delete(TH,i)
        AC1=np.delete(AC1,i)
        AC2=np.delete(AC2,i)
        del G[i]
        TH=np.delete(TH,i)
        AC1=np.delete(AC1,i)
        AC2=np.delete(AC2,i)
        i=i-1
    i=i+1
    
    
#Convert HRZ(theta)H to RZ(pi/2)RX(pi/2)RZ(theta+pi)RX(pi/2)RZ(pi/2)
i=0
while G[i] != "MEASURE":
    if (G[i] == "H" and G[i+1] == "RZ" and G[i+2]=="H" and AC1[i] == AC1[i+1] and AC1[i+1]== AC1[i+2]):
        theta = TH[i+1]
        q = AC1[i]
        G[i]="RZ"
        TH[i]=1.57079632679
        del G[i+1]
        TH=np.delete(TH,i+1)
        AC1=np.delete(AC1,i+1)
        AC2=np.delete(AC2,i+1)
        del G[i+1]
        TH=np.delete(TH,i+1)
        AC1=np.delete(AC1,i+1)
        AC2=np.delete(AC2,i+1)
        G.insert(i,"RX")
        TH=np.insert(TH,i,1.57079632679)
        AC1=np.insert(AC1,i,q)
        AC2=np.insert(AC2,i,q)
        G.insert(i,"RZ")
        TH=np.insert(TH,i,theta+(2.0*1.57079632679))
        AC1=np.insert(AC1,i,q)
        AC2=np.insert(AC2,i,q)
        G.insert(i,"RX")
        TH=np.insert(TH,i,1.57079632679)
        AC1=np.insert(AC1,i,q)
        AC2=np.insert(AC2,i,q)
        G.insert(i,"RZ")
        TH=np.insert(TH,i,1.57079632679)
        AC1=np.insert(AC1,i,q)
        AC2=np.insert(AC2,i,q)

        #move leftmost RZ of set across control bit if possible
        for j in range(i-1,0,-1):
            if AC1[j] == AC1[i]:
                if G[j] == "CNOT":
                    for k in range(j-1,0,-1):
                        if AC1[k] == AC1[i]:
                            if G[k] == "RZ":
                                TH[k]=TH[k]+TH[i]
                                del G[i]
                                TH=np.delete(TH,i)
                                AC1=np.delete(AC1,i)
                                AC2=np.delete(AC2,i)
                            else: break
                else: break
                    
        #move rightmost RZ of set across control bit if possible
        for j in range(i+4,len(G)):
            if AC1[j] == AC1[i+3]:
                if G[j] == "CNOT":
                    for k in range(j+1,len(G)):
                        if AC1[k] == AC1[i+3]:
                            if G[k] == "RZ":
                                TH[k]=TH[k]+TH[i+3]
                                del G[i+3]
                                TH=np.delete(TH,i+3)
                                AC1=np.delete(AC1,i+3)
                                AC2=np.delete(AC2,i+3)
                            else: break
                        if AC2[k] == AC1[i+3]:
                            break
                else: break
                    
                    
    i=i+1

#convert remaining HRZ or H to native gates
i=0
while G[i] != "MEASURE":
    if G[i]=="H":
        q = AC1[i]
        j=i+1
        flag = 1
        while G[j] != "MEASURE":
            if AC1[j] == AC1[i]:
                #change HRZ to native gates
                if G[j]=="RZ":
                    G[i] = "RZ"
                    theta = TH[j]
                    TH[i]=1.57079632679
                    del G[j]
                    TH=np.delete(TH,j)
                    AC1=np.delete(AC1,j)
                    AC2=np.delete(AC2,j)
                    G.insert(i+1,"RX")
                    TH=np.insert(TH,i+1,1.57079632679)
                    AC1=np.insert(AC1,i+1,q)
                    AC2=np.insert(AC2,i+1,0)
                    G.insert(i+2,"RZ")
                    TH=np.insert(TH,i+2,theta+1.57079632679)
                    AC1=np.insert(AC1,i+2,q)
                    AC2=np.insert(AC2,i+2,0)
                    flag = 0
                    break
                else: break
            j=j+1
        #change H to native gates    
        if (flag):
            G[i] = "RZ"
            TH[i]=1.57079632679
            G.insert(i+1,"RX")
            TH=np.insert(TH,i+1,1.57079632679)
            AC1=np.insert(AC1,i+1,q)
            AC2=np.insert(AC2,i+1,0)
            G.insert(i+2,"RZ")
            TH=np.insert(TH,i+2,1.57079632679)
            AC1=np.insert(AC1,i+2,q)
            AC2=np.insert(AC2,i+2,0)  
        #compress successive RZs
        if (G[i-1] == "RZ" and AC1[i-1] == AC1[i]):
            TH[i-1] = TH[i-1]+TH[i]
            del G[i]
            TH=np.delete(TH,i)
            AC1=np.delete(AC1,i)
            AC2=np.delete(AC2,i)
        #if (G[i+3] == "RZ"):
        #    TH[i+2] = TH[i+2]+TH[i+3]
        #    del G[i+3]
        #    TH=np.delete(TH,i+3)
        #    AC1=np.delete(AC1,i+3)
        #    AC2=np.delete(AC2,i+3)
       
    i=i+1
    
#Omit first RZs
for qub in range(0,nqubits):
    i=0
    while G[i] != "MEASURE":
        if G[i]=="RZ" and AC1[i]==qub:
            del G[i]
            TH=np.delete(TH,i)
            AC1=np.delete(AC1,i)
            AC2=np.delete(AC2,i)
        if (G[i]=="RX" and AC1[i]==qub) or (G[i]=="CNOT" and (AC1[i]==qub or AC2[i]==qub)):
            break
        i=i+1
    
#Omit last RZ for each qubit
for qub in range(0,nqubits+1):
    i=-1
    while i>=-int(len(G)):
        if G[i] == "H" and AC1[i]==qub:
            break
        if G[i] == "RZ" and AC1[i]==qub:
            G[i]  = "NULL"
            break
        i=i-1  

#build output circuit
qiskit_code(G,TH,AC1,AC2,"qiskit_compressed.txt")                           
