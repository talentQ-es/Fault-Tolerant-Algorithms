from Grover_Gates_and_Functions import XOR_2qubits, mcz, X_if_at_least_one_1



# ==============================================================================
# ================================= Trivial ====================================
# ==============================================================================

def Grover_Oracle_trivial(circuit, target_reg, M_list_bin_qiskit): # n, M_list_bin):
	'''
	This function implements a Grover oracle. We call it "trivial" because this
	oracle change the sign of some given states. That is, we know the solution 
	in advance. (For example, we want to find the states |101> and |110> among 
	the 8 possible ones. We know from the begining the states we want to find.)

	We can use the multicontrolled Z gate (mcz) we defined earlier to change the
	sign of any M_list_bin[i] state. Simply apply X gates before and after the 
	mcz on the qubits that are worth zero in M_list_bin[i].

	IMPORTANT !!!: Remember that if we deal with qiskit, the binary strings have
	to 	come upside	down (with the LEASTE SIGNIFICANT BIT AT THE BEGINNING !!!).

	Inputs:
		- circuit: Quantum Circuit

		- target_reg: Quantum Register (with n qubits) in which we are going to 
			search and change the sign of some given states. It must be one 
			Quantum Register of the previus circuit.
		
		- M_list_bin: Python List with the states that we want to find. The 
			states must be in binary and must have length n (that is, if our 
			"targer_reg" has 4 qubits and we want to find the state |2>, we have
			to pass in this list the number "0010", not "10" !!!)

	'''
	n = target_reg.size

	for m in M_list_bin_qiskit:
		for i in range(len(m)):
			if m[i] == '0':
				circuit.x(target_reg[i])

		mcz(circuit, target_reg[list(range(n-1))], target_reg[n-1])
	    
		for i in range(len(m)):
			if m[i] == '0':
				circuit.x(target_reg[i])










def Grover_Oracle_permutations_P_numbers_LQMG(circuit, var_reg, conditions_list, 
				                        ancilla_reg,  ancilla_2_reg,
										ancilla_out_qubit, print_oracle = 1):
	'''
	Grover oracle to compute all the permutations of P number (P=2^p). 
	The acronyms "LQMG" means "Less Qubits More Gates" because we offer another
	option with calla "MQLG" (More Qubits Less Gates):
		- MQLG: It use n + 3*num_conditions + 1 qubits
		- LQMG: It use n + 2 + num_conditions + 1
	where 
		num_conditions = (P-1)+(P-2)+...+1

	Inputs:
		- circuit: Quantum Circuit.
		
		- var_reg: Quantum Register when the numbers are stored. 
			It must be one Quantum Register of the previus circuit.
		
		- conditions_list: Python list with the "conditions". 
		 	Each condition is a Python lists with a pair of numbers. 
			Each number is Python list with the indexes of the qubits. 
			
			We call "condition" to a pair of numbers. What we are looking for 
			is for these numbers to be different. 
			
			Example (for P = 4)
				conditions_list = [[a,b], [a,c], [a,d], [b,c], [b,d], [c,d]]
			when     
				a = [0,1], b = [2,3], c = [4,5], d = [6,7] 

		- ancilla_reg: Quantum Register in the state |00...0>.
			It must have as much qubits as the number of qubit we need to 
			represent the numbers plus one. (For exaple, if we have 4 number 
			-0, 1, 2, 3- we need 2 qubits to represent them. So for P=4 we need
			3 qubits in this register.) 

			At the end of the function, this register is restore to the initial 
			state |00...0>.

			It must be one Quantum Register of the previus circuit.
		
		- ancilla_2_reg: Quantum Register in the state |00...0>. 
			It must have as much qubits as the number of condition. 
			For each condition met, we flip one qubit in this register to the 
			state |1>. 	If all conditions are met, all qubits are inverted.

			At the end of this function, this register is restore to the initial 
			state |00...0>.
			
			It must be one Quantum Register of the previus circuit.

		- ancilla_out_qubit: Qubit in the state |->. The function apply an X 
			gate in this qubit if all the conditicions are met (if all the 
			qubits in "ancilla_2_reg" were flipe to the state |1>).
	'''
	############################################################################
    ###### Oracle realization
    ############################################################################

	# Put "ancilla_2_reg" in the state |11..1> if all the conditions are met
	figures_of_each_P = len(conditions_list[0][0])
	i = 0
	for clause in conditions_list:
		circuit.barrier()

		# PART 1
		for j in range(figures_of_each_P):
			XOR_2qubits(circuit, var_reg[clause[0][j]], var_reg[clause[1][j]], 
			     		ancilla_reg[j])
		'''
		# PART 2
		circuit.mct(ancilla_reg[:2], ancilla_2_reg[i])
		XOR_2qubits(circuit, ancilla_reg[0], ancilla_reg[1], ancilla_2_reg[i])
		'''
		X_if_at_least_one_1(circuit, ancilla_reg, ancilla_2_reg[i])

		for j in range(figures_of_each_P):
			XOR_2qubits(circuit, var_reg[clause[0][j]], var_reg[clause[1][j]], 
			     		ancilla_reg[j])


		i += 1
	# Apply an X gate in the qubit "ancilla_out_qubit" if the register
	# "ancilla_2_reg" are in state |11...1>
	circuit.barrier()
	circuit.mct(ancilla_2_reg, ancilla_out_qubit)
	circuit.barrier()

	# Restore the register "ancilla_2_reg" into the state |00...0>.
	i = 0
	for clause in conditions_list:
		# PART 1
		for j in range(figures_of_each_P):
			XOR_2qubits(circuit, var_reg[clause[0][j]], var_reg[clause[1][j]], 
			     		ancilla_reg[j])
		'''
		# PART 2
		circuit.mct(ancilla_reg[:2], ancilla_2_reg[i])
		XOR_2qubits(circuit, ancilla_reg[0], ancilla_reg[1], ancilla_2_reg[i])
		'''
		X_if_at_least_one_1(circuit, ancilla_reg, ancilla_2_reg[i])
		
		for j in range(figures_of_each_P):
			XOR_2qubits(circuit, var_reg[clause[0][j]], var_reg[clause[1][j]], 
			     		ancilla_reg[j])
		i += 1
		circuit.barrier()

	if print_oracle == 0:
		total_qubits = var_reg.size + 2 + len(conditions_list) + 1
		try:
			circuit.draw(output = 'mpl',fold=-1, 
				filename = f'2-Fig_Oracle_permutations_{int(var_reg.size/figures_of_each_P)}_numbers_{total_qubits}_qubits.png')
		except:
			print('WARNING: Circuit to large to generate the image.')
			print('')









def Grover_Oracle_permutations_P_numbers_MQLG(circuit, var_reg, conditions_list, 
				                        ancilla_reg,  ancilla_2_reg,
										ancilla_out_qubit, print_oracle = 1):
	'''
	Grover oracle to compute all the permutations of P number (P=2^p). 
	The acronyms "MQLG" means "More Qubits Less Gates" because we offer another
	option with calla "LQMG" (Less Qubits More Gates):
		- MQLG: It use n + 3*num_conditions + 1 qubits
		- LQMG: It use n + 2 + num_conditions + 1
	where 
		num_conditions = (P-1)+(P-2)+...+1


	This function puts in the state |1> all the qubits of the quantum register 
	"ancilla_2_reg" if all the pair of numbers in 	"conditions_list" are 
	diferent. Then, the function apply an X gate in the qubit "ancilla_out_qubit"
	if all the qubits in "ancilla_2_reg" are in state |1>. Finaly, the 
	function restore to the state |0> the qubits in the	registers 
	"ancilla_2_reg" and "ancilla_reg" to the state |0>

	In "PART 1" we compare two number of "conditions_list" qubit by qubit. 	For 
	each comparision we use two qubits of the "ancilla_reg" 	to store the 
	result. If the two numbers to compare are different, at least one qubit of 
	the two qubits from the "ancilla_reg" will be end in state |1>.

	In "PART 2" we use the results stored in "ancilla_reg" to see if the
	numbers are different. If one or both of the qubits in "ancilla_reg" are 
	in state |1>, we put one qubit of "ancilla_2_reg" in the state |1>.

	If all the pair of numbers in "conditions_list" are different, we will have 
	all the qubits in "ancilla_2_reg" in the state |1>.
	
	Actually, "conditions_list" is not a list of pairs of numbers, but a list 
	with the indexes of the qubits that represent those pairs of numbers in the 
	quantum register "var_reg".

	Inputs:
		- circuit: Quantum Circuit.
		
		- var_reg: Quantum Register when the numbers are stored. 
			It must be one Quantum Register of the previus circuit.
		
		- conditions_list: Python list with the "conditions". 
		 	Each condition is a Python lists with a pair of numbers. 
			Each number is Python list with the indexes of the qubits. 
			
			We call "condition" to a pair of numbers. What we are looking for 
			is for these numbers to be different. 
			
			Example (for P = 4):
				conditions_list = [[a,b], [a,c], [a,d], [b,c], [b,d], [c,d]]
			when     
				a = [0,1], b = [2,3], c = [4,5], d = [6,7] 

		- ancilla_reg: Quantum Register in the state |00...0>.
			It must have as much qubits as the number of condition times the 
			number of qubits necessary to encode the numbers. 

			At the end of the function, this register is restore to the initial 
			state |00...0>.

			It must be one Quantum Register of the previus circuit.
		
		- ancilla_2_reg: Quantum Register in the state |00...0>. 
			It must have as much qubits as the number of condition. 
			For each condition met, we flip one qubit in this register to the 
			state |1>.  If all conditions are met, all qubits are inverted.

			At the end of this function, this register is restore to the initial 
			state |00...0> .
			
			It must be one Quantum Register of the previus circuit.

		- ancilla_out_qubit: Qubit in the state |->. The function apply an X 
			gate in this qubit if all the conditicions are met (if all the 
			qubits in "ancilla_2_reg" were flipe to the state |1>).
	'''

	figures_of_each_P = len(conditions_list[0][0])
	# =========================================================
	# Put "ancilla_2_reg" in the state |11..1> if all the conditions are met
	i = 0
	for clause in conditions_list:
		circuit.barrier()

		# PART 1
		for j in range(figures_of_each_P):
			XOR_2qubits(circuit, var_reg[clause[0][j]], var_reg[clause[1][j]], 
					ancilla_reg[2*i+j])
		
		# PART 2
		'''
		circuit.mct(ancilla_reg[2*i:2*i+2], ancilla_2_reg[i])
		XOR_2qubits(circuit, ancilla_reg[2*i], ancilla_reg[2*i+1], 
					ancilla_2_reg[i])
		'''
		X_if_at_least_one_1(circuit, ancilla_reg[2*i:2*i+2], ancilla_2_reg[i])
		i += 1

	# =========================================================
	# Apply an X gate in the qubit "ancilla_out_qubit" if the register
	# "ancilla_2_reg" are in state |11...1>
	circuit.barrier()
	circuit.mct(ancilla_2_reg, ancilla_out_qubit)
	circuit.barrier()
	
	# =========================================================
	# Reset the "ancilla_reg" and "ancilla_2_reg" to state |00...0>
	i = len(conditions_list) - 1
	for clause in reversed(conditions_list):
		# PART 2
		'''
		XOR_2qubits(circuit, ancilla_reg[2*i], ancilla_reg[2*i+1], 
					ancilla_2_reg[i])
		circuit.mct(ancilla_reg[2*i:2*i+2], ancilla_2_reg[i])
		'''
		X_if_at_least_one_1(circuit, ancilla_reg[2*i:2*i+2], ancilla_2_reg[i])

		# PART 1
		for j in range(figures_of_each_P):
			XOR_2qubits(circuit, var_reg[clause[0][j]], var_reg[clause[1][j]], 
					ancilla_reg[2*i+j])
			
		circuit.barrier()
		
		i -= 1

		
	if print_oracle == 0:
		total_qubits = var_reg.size + 3*len(conditions_list)+1
		try:
			circuit.draw(output = 'mpl',fold=-1, 
				filename = f'2-Fig_Oracle_permutations_{int(var_reg.size/figures_of_each_P)}_numbers_{total_qubits}_qubits.png')
		except:
			print('WARNING: Circuit to large to generate the image.')
			print('')


def Grover_Oracle_Sudoku_2x2(circuit, conditions_list, ancilla_reg, 
			                 output_qubit, print_oracle = 1):
	'''
	This oracle solves the problem of a Sudoku 2x2. 
	'''
	# Compute clauses
	i = 0
	for clause in conditions_list:
		XOR_2qubits(circuit, clause[0], clause[1], ancilla_reg[i])
		i += 1

	# Flip 'output' bit if all clauses are satisfied
	circuit.mct(ancilla_reg, output_qubit)

	# Uncompute clauses to reset clause-checking bits to 0
	i = 0
	for clause in conditions_list:
		XOR_2qubits(circuit, clause[0], clause[1], ancilla_reg[i])
		i += 1

	if print_oracle == 0:
		circuit.draw(output='mpl', fold = -1, filename = '3-Fig_Oracle_Sudoku_2x2')