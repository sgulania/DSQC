#Sahil Gulania
#USC 2019

# Domain Specific Quantum Compiler
# Dynamic Simulations on Quantum Computers

import numpy as np
from qiskit import qiskit_code
from rigetti import rigetti_code
lineList = [line.rstrip('\n') for line in open("advance_gates.txt")]
count = len(lineList)

#Read the gate in right vector form
# G = Gate type
# TH = Angle of rotation ! if no angle rotation then TH = 0
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
 
  #print(G[i],TH[i],AC1[i],AC2[i])   


qiskit_code(G,TH,AC1,AC2,"qiskit_uncompressed.txt")
rigetti_code(G,TH,AC1,AC2,"rigetti_uncompressed.txt")

# Use CNOT = H CZ H 
i = 0
while G[i] != "MEASURE":
  if G[i] == "CNOT":
     G[i] = "CZ"
     G.insert(i+1,"H")
     TH = np.insert(TH,i+1,0) 
     AC1 = np.insert(AC1,i+1,AC2[i]) 
     AC2 = np.insert(AC2,i+1,0)
     G.insert(i,"H")
     TH = np.insert(TH,i,0) 
     AC1 = np.insert(AC1,i,AC2[i]) 
     AC2 = np.insert(AC2,i,0)
  i = i+1  

# Last and second last CNOT can be ommited  
maxq = max(max(AC1),max(AC2))
remember = np.zeros(shape=(2,maxq),dtype=np.int)
for mm in range (0,maxq+1):
 i = 0
 while G[i] != "MEASURE":
      if G[i] == "CZ" and AC1[i] == mm and AC2[i] == mm+1:
            j = i+1
            while G[j] != "MEASURE":
                  if G[j] == "CZ" and AC1[j] == mm and AC2[j] == mm+1:
                       remember[0][mm] = i; remember[1][mm] = j;
                  j = j+1
      i = i+1 

for nn in range (maxq-1,-1,-1):
 for mm in range (1,-1,-1):
#   print(mm,nn)
  del G[remember[mm][nn]];TH = np.delete(TH,remember[mm][nn]);
  AC1 = np.delete(AC1,remember[mm][nn]); AC2 = np.delete(AC2,remember[mm][nn])


# Use H*H = I but make sure it can only happen if no gate is 
# present in between 
i = 0
while G[i] != "MEASURE":
  if G[i] == "H":
    flag = 0
    #print(G[i],TH[i],AC1[i],AC2[i],"before start")
    j = i+1
    while G[j] != "MEASURE":
       if ((G[j] == "CZ" and AC1[j] == AC1[i]) or (G[j] == "CZ" and AC2[j] == AC1[i]) or (G[j] == "RZ" and AC1[j] == AC1[i])) :
          break
       if G[j] == G[i] and AC1[j] == AC1[i] :
          #print(G[i],TH[i],AC1[i],AC2[i],"before")
          del G[j]
          TH = np.delete(TH,j)
          AC1 = np.delete(AC1,j)
          AC2 = np.delete(AC2,j)
          #print(G[i],TH[i],AC1[i],AC2[i],"after")
          del G[i]
          TH = np.delete(TH,i)
          AC1 = np.delete(AC1,i)
          AC2 = np.delete(AC2,i)
          flag = 2
       j = j+1
       if flag ==2:
          break 
  i = i + 1



# Use CZ H RZ H CZ = RZ(pi/2) CZ RX(pi/2) RZ RX(-pi2) CZ RZ(-pi/2)
i = 0 
while G[i] != "MEASURE":
    if (G[i] == "CZ" and G[i+1] == "H" and AC2[i] == AC1[i+1] and G[i+2] == "RZ" and AC2[i] == AC1[i+2] and G[i+3] == "H" and AC2[i] == AC1[i+3] and G[i+4] == "CZ" and AC2[i] == AC2[i+4]):
          G[i+1] = "RX"; TH[i+1] = 1.57079632679; 
          G[i+3] = "RX"; TH[i+3] = -1.57079632679;
          G.insert(i+5,"RZ"); TH = np.insert(TH,i+5,-1.57079632679); 
          AC1 = np.insert(AC1,i+5,AC2[i]); AC2 = np.insert(AC2,i+5,0);
          G.insert(i,"RZ"); TH = np.insert(TH,i,1.57079632679); 
          AC1 = np.insert(AC1,i,AC2[i]); AC2 = np.insert(AC2,i,0);
    i = i+1


# Use H = RZ(pi/2) RX(pi/2) RZ(pi/2)
i = 0
while G[i] !="MEASURE":
    if (G[i] == "H"):
          flag = AC1[i]
          G[i] = "RZ"; TH[i] = 1.57079632679 ;
          G.insert(i,"RX");TH = np.insert(TH,i,1.57079632679);
          AC1 = np.insert(AC1,i,flag); AC2 = np.insert(AC2,i,0); 
          G.insert(i,"RZ");TH = np.insert(TH,i,1.57079632679); 
          AC1 = np.insert(AC1,i,flag); AC2 = np.insert(AC2,i,0); 
    i = i+1 


# Compress RZ gates
loop_flag = 0
for mm in range (0,1000):
 i = 0 
 while G[i] !="MEASURE": 
     if (G[i] == "RZ"):
           j = i+1
           flag = 0
           #print(flag,"flag")
           while G[j] !="MEASURE":
                 if (G[j] == "RX" and AC1[j] == AC1[i]):
                      flag = 2
                 if (G[j] == "RZ" and AC1[j] == AC1[i]):
                      TH[i] = TH[i]+TH[j]; 
                      del G[j];TH = np.delete(TH,j);
                      AC1 = np.delete(AC1,j); AC2 = np.delete(AC2,j) 
                      flag = 2
                      loop_flag = 3
                 j = j+1
                 if(flag == 2):
                      break
     if (G[i] == "RZ" and TH[i]== 0.0):
           del G[i];TH = np.delete(TH,i);
           AC1 = np.delete(AC1,i); AC2 = np.delete(AC2,i)
     i = i +1
 if(loop_flag == 0):
     break  
 if(mm ==1000 and loop_flag==3):
     print("more RZ compression are left be carefull!!")

# Use  -|----------------------------------|----RX(-pi/2)-   =  -RX(-pi/2)-|--RX(pi/2)--RZ(theta)--RX(-pi/2)--|---
#      -CZ-RX(pi/2)--RZ(theta)--RX(-pi/2)--CZ---RX(pi/2)--      -RX(pi/2)--CZ---------------------------------CZ--      

i = 0 
while G[i] != "MEASURE":
     if (G[i] == "RX" and TH[i] == 1.57079632679):
      i1 = i+1
      while G[i1] != "MEASURE":
       if (G[i1] == "RX" and AC1[i1] == AC1[i] or G[i1] == "CZ" and AC1[i1] == AC1[i] or G[i1] == "RZ" and TH[i1] != 3.14159265358 and AC1[i1] == AC1[i] or G[i1] == "CZ" and AC2[i1] == AC1[i]):
        break
       if (G[i1] == "RZ" and TH[i1] == 3.14159265358 and AC1[i1] == AC1[i]):
        #print("found",i,i1)
        
        i2 = i1+1
        while G[i2] != "MEASURE":
         if (G[i2] == "RX" and AC1[i2] == AC1[i] or G[i2] == "RZ" and AC1[i2] == AC1[i] ):
           break
         if (G[i2] == "CZ" and AC1[i2] == AC1[i] and G[i2+4] == "CZ" and AC1[i2+4] == AC1[i]):
           #print ("found",AC1[i2])
           #break
           i3 = i2 +5
           while G[i3] != "MEASURE":
             if(G[i3] == "RZ" and AC1[i3] == AC1[i]+1 or G[i3] == "CZ" and AC1[i3] == AC1[i]+1 or G[i3] == "RX" and TH[i3] != 1.57079632679 and AC1[i3] == AC1[i]+1 ):
               break 
             if(G[i3] == "RX" and TH[i3] == 1.57079632679 and AC1[i3] == AC1[i]+1) :
               #print ("found",AC1[i2],AC1[i3])
               
               i4 = i2 + 5
               while G[i4] != "MEASURE": 
                  if (G[i4] == "RZ" and AC1[i4] == AC1[i] or G[i4] == "CZ" and AC1[i4] == AC1[i] or G[i4] == "RX" and TH[i4] != 1.57079632679 and AC1[i4] == AC1[i] ):
                     break
                  if(G[i4] == "RX" and TH[i4] == 1.57079632679 and AC1[i4] == AC1[i]) :
                     #print ("found",AC1[i2],AC1[i3],AC1[4])
                     AC1[i2+1] = AC1[i];AC1[i2+2] = AC1[i];AC1[i2+3] = AC1[i]
                     G[i4] = "RZ"; TH[i4] = 3.14159265358; 
                     del G[i3];TH = np.delete(TH,i3)
                     AC1 = np.delete(AC1,i3); AC2 = np.delete(AC2,i3)
                     G.insert(i2,"RX")
                     TH = np.insert(TH,i2,1.57079632679)            
                     AC1 = np.insert(AC1,i2,AC2[i2]); AC2 = np.insert(AC2,i2,0)
                     del G[i1];TH = np.delete(TH,i1)
                     AC1 = np.delete(AC1,i1); AC2 = np.delete(AC2,i1)
                     del G[i];TH = np.delete(TH,i)
                     AC1 = np.delete(AC1,i); AC2 = np.delete(AC2,i)
                     
                     break

                  i4 = i4 +1

             i3 = i3 + 1

         i2 = i2 + 1 

       i1 = i1 + 1  

     i = i+1


# Compress RZ gates                                                             
loop_flag = 0                                                                   
for mm in range (0,1000):                                                       
 i = 0                                                                          
 while G[i] !="MEASURE":                                                        
     if (G[i] == "RZ"):                                                         
           j = i+1                                                              
           flag = 0                                                             
           #print(flag,"flag")                                                  
           while G[j] !="MEASURE":                                              
                 if (G[j] == "RX" and AC1[j] == AC1[i]):                        
                      flag = 2                                                  
                 if (G[j] == "RZ" and AC1[j] == AC1[i]):                        
                      TH[i] = TH[i]+TH[j];                                      
                      del G[j];TH = np.delete(TH,j);                            
                      AC1 = np.delete(AC1,j); AC2 = np.delete(AC2,j)            
                      flag = 2                                                  
                      loop_flag = 3                                             
                 j = j+1                                                        
                 if(flag == 2):                                                 
                      break                                                     
     if (G[i] == "RZ" and TH[i]== 0.0):                                         
           del G[i];TH = np.delete(TH,i);                                       
           AC1 = np.delete(AC1,i); AC2 = np.delete(AC2,i)                       
     i = i +1                                                                   
 if(loop_flag == 0):                                                            
     break                                                                      
 if(mm ==1000 and loop_flag==3):                                                
     print("more RZ compression are left be carefull!!")


# Use RZ(theta) RX RZ(pi) = RZ(theta-pi) RX(-pi2)
i = 0 
while G[i] != "MEASURE":
     if (G[i] == "RZ"):
        loop_breaker = 0
        i1 = i+1
        while G[i1] != "MEASURE":
          if (G[i1] == "RX" and TH[i1] != 1.57079632679 and AC1[i1] == AC1[i]):
             break
          if (G[i1] == "RX" and TH[i1] == 1.57079632679 and AC1[i1] == AC1[i]):
             i2 = i1 + 1
             while G[i2] != "MEASURE":
                if (G[i2] == "RZ" and TH[i2] == 3.14159265358 and AC1[i2] == AC1[i]):
                     TH[i] = TH[i]+TH[i2]
                     TH[i1] = -TH[i1]
                     del G[i2];TH = np.delete(TH,i2);
                     AC1 = np.delete(AC1,i2); AC2 = np.delete(AC2,i2);
                     #print("inside",i,i1,i2)
                     loop_breaker = 3
                     break
                elif (G[i2] == "RZ" and TH[i2] != 3.14159265358 and AC1[i2] == AC1[i]):
                     loop_breaker = 3 
                     break
                i2 = i2 + 1                          
          if (loop_breaker == 3):
                break
          i1 = i1 + 1
     i = i + 1


qiskit_code(G,TH,AC1,AC2,"qiskit_compressed.txt")
rigetti_code(G,TH,AC1,AC2,"rigetti_compressed.txt")  
