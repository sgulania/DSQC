![python badge](https://img.shields.io/badge/python-3.4%2C%203.5%2C%203.6-brightgreen.svg)
# Domain Specific Quantum Compiler 
## University of Southern California, Los Angeles, CA 

![QC-reduction](https://github.com/sgulania/DSQC/blob/master/Qcircuit.gif)

Command to run :

python rigetti_dsqc.py /path/to/advance_gates.txt

or 

python ibm_dsqc.py /path/to/advance_gates.txt


The output contains both gates compressed and uncompressed scripts in OpenQASM, which is executable on IBM hardware and native Quil, which is executable on Rigetti's device.
