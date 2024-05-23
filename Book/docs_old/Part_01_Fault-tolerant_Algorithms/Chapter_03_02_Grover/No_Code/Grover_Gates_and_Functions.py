import numpy as np
#from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister

# ==============================================================================
# ============================== Initialization ================================
# ==============================================================================

def initialize_uniform_dist_Hadammads(circuit, target_reg):
	'''
	This function adds Hadammard gates to all the qubits in a given register.

	Inputs:
		- circuit: Quantum Circuit.
		
		- target_reg: Quantum register in which we are going to apply the gates.
		 	It must be one Quantum Register of the previus circuit. 
	
	'''
	for qubit in target_reg:
		circuit.h(qubit)






# ==============================================================================
# ================================== Gates =====================================
# ==============================================================================

def mcz(circuit, control_qubits, target_qubit):
	'''
	This funntion implements a multicontroled Z-gate. If all the control_qubits
	are in state |1>, a Z-gate is apply in the qubit called "target_qubit".

	To build this gate we use a multicontrolled Toffoli (mct) gate. To do this, 
	let's first remember that the mct gate is nothing more than a multicontrolled 
	CNOT, which only applies on the target qubit if all the control qubits are 1.

	So, we only need to use the property
		Z = H X H 
	In this way we only have to apply Hadammard gates on the target_qubit before
	and after the mct.

	In summary, the mcz gate adds a pi phase (Z gate) to the |11...1> state.

	Inputs:
		- circuit: Quantum Circuit where we have the "control_reg" and the 
			"target_qubit".
		
		- control_reg: Qubits that control the gate. It must be one Quantum 
			Register of the previus circuit.
		
		- target_qubit: Qubit in which we apply the Z gate. It must be one qubit
			of the previus circuit.

	'''
	circuit.h(target_qubit)
	circuit.mct(control_qubits, target_qubit)  # multi-controlled-toffoli
	circuit.h(target_qubit)







def XOR_2qubits(circuit, v1, v2, qubit_out):
	circuit.cx(v1, qubit_out)
	circuit.cx(v2, qubit_out)







def X_if_at_least_one_1(circuit, ancilla_reg, ancilla_2_qubit):
	'''
	This función apply several X gates (CNOT or MCT) in the qubit 
	"ancilla_2_qubit". If we have at least at least one 1 in the register 
	"ancilla_reg", then the number of X gates apply on "ancilla_2_qubit" are 
	odd. It is the same as apply only one X gate.

	If there are no 1's on "ancilla_reg", then the number of X gates apply
	in "ancilla_2_qubit" are even. It is the same as doing nothing.
	'''

	size = len(ancilla_reg)

	# Apply an X gate in ancilla_2_qubit if there are an even mumber of 1's
	for i in range(size):
		circuit.cnot(ancilla_reg[i], ancilla_2_qubit)
	
	# Apply an X gate in ancilla_2_qubit if there are an odd mumber of 1's
	circuit.x(ancilla_reg[0])
	for i in range(size):
		circuit.cnot(ancilla_reg[i], ancilla_2_qubit)
	circuit.x(ancilla_reg[0])

	# Undone the case |00...0>
	for i in range(size):
		circuit.x(ancilla_reg[i])

	circuit.mct(ancilla_reg, ancilla_2_qubit)

	for i in range(size):
		circuit.x(ancilla_reg[i])









# ==============================================================================
# ================================= Functions ==================================
# ==============================================================================

def Iterations_T(N, M):
	
	return int(np.pi/4 * np.sqrt(N/M)) # rounding by truncation




def int_to_n_bin(input_list, n):
	'''
	This function convert a list of integers into a list of binary numbers of 
	lenth n.

	Inputs:
		- input_list: Python list with the integers we want to convert to binary.

		- n: The lenght of the binary numbers (we fill with zeros to the left).

	Output:
		- Python list with binary numbers of lenght n in the same order as in 
			the input_list
	'''

	return [bin(m)[2:].zfill(n) for m in input_list]
