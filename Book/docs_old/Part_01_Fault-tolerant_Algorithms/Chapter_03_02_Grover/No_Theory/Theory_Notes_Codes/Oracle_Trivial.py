from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit

# We import functions from the scripts in ..\..\Code folder
import sys
sys.path.append("..\..\Code")
from Grover_Oracles import Grover_Oracle_trivial



n = 5

quantum_reg = QuantumRegister(n)
classic_reg = ClassicalRegister(n)

circuit = QuantumCircuit(quantum_reg, classic_reg)

M_list_bin = [ '01101', '11000']


Grover_Oracle_trivial(circuit, quantum_reg, M_list_bin)

circuit.draw(output='mpl', filename = 'Fig_Imple_oracle_trivial')