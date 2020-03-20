#Sahil Gulania
#USC 2019

# Domain Specific Quantum Compiler
# Dynamic Simulations on Quantum Computers

# Covert Rigetti high level code to Rigetti high level code 

import numpy as np
def rigetti_code(G,TH,AC1,AC2,name):
  count = len(G)

  f = open(name, "w") 

  print("RESET",file=f)
  print(("DECLARE ro BIT[%s]"%(max(max(AC1),max(AC2))+1)),file=f)

  for i in range(0,count):
      if (G[i] == "H"):
          print(("H %s"%(AC1[i])),file=f)
      if (G[i] == "RZ"):
          print(("RZ(%s) %s"%(TH[i],AC1[i] )),file=f)
      if (G[i] == "RX"):
          print(("RX(%s) %s"%(TH[i],AC1[i] )),file=f)
      if (G[i] == "CZ"):
          print(("CZ %s %s"%(AC1[i],AC2[i])),file=f)
      if (G[i] == "CNOT"): 
          print(("CNOT %s %s"%(AC1[i],AC2[i])),file=f)
  for j in range (0,max(max(AC1),max(AC2))+1):
      print(("MEASURE %s ro[%s]"%(j,j)),file=f)
  f.close()
