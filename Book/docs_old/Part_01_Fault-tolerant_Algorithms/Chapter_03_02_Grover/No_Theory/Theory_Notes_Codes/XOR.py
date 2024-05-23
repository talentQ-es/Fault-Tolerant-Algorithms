from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister

import sys
sys.path.append("..\..\Code")
from Grover_Gates_and_Functions import XOR_2qubits


in_qubits = QuantumRegister(2, name='input')
out_qubit = QuantumRegister(1, name='output')
qc = QuantumCircuit(in_qubits, out_qubit)
XOR_2qubits(qc, in_qubits[0], in_qubits[1], out_qubit)
qc.draw(output = 'mpl', filename = 'Fig_Imple_xor')