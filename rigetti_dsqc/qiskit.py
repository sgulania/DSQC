#Sahil Gulania
#USC 2019

# Domain Specific Quantum Compiler
# Dynamic Simulations on Quantum Computers

# Covert Rigetti high level code to OpenQASM

import numpy as np
def qiskit_code(G,TH,AC1,AC2,name):
  count = len(G)

  f = open(name, "w") 

  print("OPENQASM 2.0;",file=f)
  print("include \"qelib1.inc\";",file=f)

  print("",file=f)
  print(("qreg q[%s];"%(max(max(AC1),max(AC2))+1)),file=f)
  print(("creg c[%s];"%(max(max(AC1),max(AC2))+1)),file=f)
  print("",file=f)

  for i in range(0,count):
      if (G[i] == "H"):
          print(("h q[%s];"%(AC1[i])),file=f)
      if (G[i] == "RZ"):
          print(("rz (%s) q[%s];"%(TH[i],AC1[i] )),file=f)
      if (G[i] == "RX"):
          print(("rx (%s) q[%s];"%(TH[i],AC1[i] )),file=f)
      if (G[i] == "CZ"):
          print(("cz q[%s], q[%s];"%(AC1[i],AC2[i])),file=f)
      if (G[i] == "CNOT"): 
          print(("cx q[%s], q[%s];"%(AC1[i],AC2[i])),file=f)
  for j in range (0,max(max(AC1),max(AC2))+1):
      print(("measure q[%s] -> c[%s];"%(j,j)),file=f)
  f.close()
