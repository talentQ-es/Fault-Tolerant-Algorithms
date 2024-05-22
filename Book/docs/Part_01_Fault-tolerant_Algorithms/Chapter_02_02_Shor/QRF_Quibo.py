import numpy as np
from qibo import Circuit, gates
def create_QFT(circuit, n, with_swaps):
    """ Creates a circuit for the quantum fourier transform of up_reg """
    i=n-1
    """ Apply the H gates and Cphases"""
    """ The Cphases with |angle| < threshold are not created because they do
    nothing. The threshold is put as being 0 so all CPhases are created,
    but the clause is there so if wanted just need to change the 0 of the
    if-clause to the desired value """
    while i>=0:
        circuit.add(gates.H(i))# Apply the H-gate to each qubit
        j=i-1
        while j>=0: # Do the controlled rotations
            if (np.pi)/(pow(2,(i-j))) > 0:
                circuit.add(gates.CU1( i , j, (np.pi)/(pow(2,(i-j))) ))
                j=j-1
        i = i - 1
    """ If specified, apply the Swaps at the end """
    if with_swaps== True:
        i=0
        while i < ((n-1)/2):
            circuit.add(gates.SWAP(i, n-1-i))
            i=i+1

print('============================')
#print('Example with the QFT defined in the script gates_and_function (depleted)')


qc = Circuit(4)
create_QFT(qc, 4, True)
print(qc.draw())