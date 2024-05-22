from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, transpile
from qiskit.visualization import plot_histogram
from qiskit_aer import AerSimulator

from Grover_Diffusers import Grover_Diffuser
from Grover_Oracles import Grover_Oracle_Sudoku_2x2 
from Grover_Gates_and_Functions import Iterations_T

import numpy as np

conditions_list = [ [0,1],  [0,2],  [1,3],  [2,3] ]

n = 4
N = 2**n # Total number of states
M = 2    # Number of solutions


var_reg = QuantumRegister(n, name='v')
ancilla_reg = QuantumRegister(len(conditions_list), name='c')
output_qubit = QuantumRegister(1, name='out')
classic_reg = ClassicalRegister(n, name='cbits')
circuit = QuantumCircuit(var_reg, ancilla_reg, output_qubit, classic_reg)

# Initialize 'out0' in state |->
circuit.x(output_qubit)
circuit.h(output_qubit)

# Initialize qubits in state |s>
circuit.h(var_reg)
circuit.barrier()  # for visual separation

T = Iterations_T(N,M)

for i in range(T):
    Grover_Oracle_Sudoku_2x2(circuit, conditions_list, ancilla_reg, 
                             output_qubit, print_oracle = i)
    circuit.barrier()  # for visual separation
    Grover_Diffuser(circuit, var_reg)


# Measure the variable qubits
circuit.measure(var_reg, classic_reg)


circuit.draw(output='mpl', fold = -1, filename = '3-Fig_Sudoku_2x2')

sim = AerSimulator(method = 'statevector')
tcircuit = transpile(circuit, sim)
result = sim.run(tcircuit).result()

counts = result.get_counts()

keys_bin = list(counts.keys())


values = list(counts.values())
zip_list = zip(keys_bin,values)
zip_sorted = list(sorted(zip_list, key = lambda x: -x[1]))
keys_bin, values = zip(*list(zip_sorted))

num_sols = len(list(zip_sorted))

print_range = 2 + 2 
if num_sols < print_range:
    print_range = num_sols

print('Solving the sudoku 2x2:')
print('    v0  v1')
print('    v2  v3')
print('The results takes the form: v0v1v2v3')
print(f'\nThe algorithm found {num_sols} results.')
print(f'The {print_range} results with more counts are:')
print('\n   Result | Counts')
for i in range(print_range):
    print('  ',list(zip_sorted)[i])

fig = plot_histogram(result.get_counts())

fig.tight_layout()

fig.savefig('3-Fig_Sudoku_2x2_Histogram')