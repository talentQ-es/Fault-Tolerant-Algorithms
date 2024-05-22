'''
This script print the same circuit 4 times with diferent values of the varable
approximation_degree.
'''

from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit.circuit.library import QFT
import numpy as np

# Approximation_degree = 0
reg = QuantumRegister(4)
qc = QuantumCircuit(reg)
print('approximation_degree = 0')
qc.append(QFT(4, inverse=False, do_swaps=False, approximation_degree= 0).to_gate(), reg[:]) #do_swaps=False,
print(qc.decompose().decompose().draw(output = 'text'))

# Approximation_degree = 1
print('============================')
reg = QuantumRegister(4)
qc = QuantumCircuit(reg)
print('approximation_degree = 1')
qc.append(QFT(4, inverse=False, do_swaps=False, approximation_degree= 1).to_gate(), reg[:]) # do_swaps=False,
print(qc.decompose().decompose().draw(output = 'text'))

# Approximation_degree = 2
print('============================')
reg = QuantumRegister(4)
qc = QuantumCircuit(reg)
print('approximation_degree = 2')
qc.append(QFT(4, inverse=False, do_swaps=False, approximation_degree= 2).to_gate(), reg[:]) #do_swaps=False,
print(qc.decompose().decompose().draw(output = 'text'))

# Approximation_degree = 3
print('============================')
reg = QuantumRegister(4)
qc = QuantumCircuit(reg)
print('approximation_degree = 3')
qc.append(QFT(4, inverse=False, do_swaps=False, approximation_degree= 3).to_gate(), reg[:]) # do_swaps=False,
print(qc.decompose().decompose().draw(output = 'text'))



def create_QFT(circuit,up_reg,n,with_swaps):
    '''
    Nota_David: en principio, se sustituye por "qiskit.circuit.library.QFT()"
    '''
    
    i=n-1
    """ Apply the H gates and Cphases"""
    """ The Cphases with |angle| < threshold are not created because they do 
    nothing. The threshold is put as being 0 so all CPhases are created,
    but the clause is there so if wanted just need to change the 0 of the
    if-clause to the desired value """
    while i>=0:
        circuit.h(up_reg[i])        
        j=i-1  
        while j>=0:
            if (np.pi)/(pow(2,(i-j))) > 0:
                circuit.cp( (np.pi)/(pow(2,(i-j))) , up_reg[i] , up_reg[j] )
                j=j-1   
        i=i-1 

    """ If specified, apply the Swaps at the end """
    if with_swaps==1:
        i=0
        while i < ((n-1)/2):
            circuit.swap(up_reg[i], up_reg[n-1-i])
            i=i+1


print('============================')
print('Example with the QFT defined in the script gates_and_function (depleted)')

reg = QuantumRegister(4)
qc = QuantumCircuit(reg)
create_QFT(qc, reg, 4, False)

print(qc.draw(output = 'text'))