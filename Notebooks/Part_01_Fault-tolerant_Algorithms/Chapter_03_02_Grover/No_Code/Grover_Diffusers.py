from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister

from Grover_Gates_and_Functions import mcz

def Grover_Diffuser(circuit, target_reg):
	''' 
	This function apply the Grover's diffuser to a quantum register.

	Imputs:
		- circuit: It is the Quantum Circuit in which we are going to insert 
	        the diffuser gate. It must contain the Quantum Register target_reg.
	        It can be something like:
	        QuantumCircuit(target_reg, classic_reg)
		
		- target_reg: Quantum Register in witch we are going to apply the 
			diffuser. 

		- n: Number of qubits in the Quantum Register target_reg

	Output:
		The function has no output. It modiffy the original circuit.
	'''

	n = target_reg.size

	# Apply transformation |s> -> |00..0> (H-gates)
	for i in range(n):
		circuit.h(target_reg[i])

	# Apply transformation |00..0> -> |11..1> (X-gates)
	for i in range(n):
		circuit.x(target_reg[i])

	# Do multi-controlled-Z gate
	mcz(circuit, target_reg[list(range(n-1))], target_reg[n-1])

	# Apply transformation |11..1> -> |00..0>
	for i in range(n):
		circuit.x(target_reg[i])

	# Apply transformation |00..0> -> |s>
	for i in range(n):
		circuit.h(target_reg[i])

if __name__ == "__main__":

	n = 6

	quantum_reg = QuantumRegister(n)
	classic_reg = ClassicalRegister(n)

	circuit = QuantumCircuit(quantum_reg, classic_reg)

	Grover_Diffuser(circuit, quantum_reg)

	circuit.draw(output='mpl', filename = 'Fig_Imple_diffuser')