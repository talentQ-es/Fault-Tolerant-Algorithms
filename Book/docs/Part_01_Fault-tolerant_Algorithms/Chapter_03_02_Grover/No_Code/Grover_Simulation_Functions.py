# Import my custom functions
import Grover_Gates_and_Functions as ggaf
from Grover_Diffusers import Grover_Diffuser

from Grover_Oracles import Grover_Oracle_trivial
from Grover_Oracles import Grover_Oracle_permutations_P_numbers_MQLG
from Grover_Oracles import Grover_Oracle_permutations_P_numbers_LQMG


# Import qiskit
from qiskit import transpile
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit_aer import AerSimulator

import numpy as np

import multiprocessing as mp


def Grover_simulation_trivial_oracle(n, M_list, gpu = False, 
                                     simulation_method = "statevector",
                                     shots = -1,
                                     print_result = True):

    '''
    This function build circuit and execute the simulation. It is an example of
    a trivial application of the Grover's algorithm. We give to the function the
    states we want to find and the function generates th circuit with the 
    Grover's oracle that mark the desire states. 

    We call it trivial because we know the solucions we want to find.

    Inputs:
        - n: number of qubits in the circuit.

        - M_lit: Python list (or a tuple or a single number) with the solutions 
            (numbers in decimal) that we want to find. We can search for any 
            integer between 0 and 2^n.

        - gpu: Boolean variable. 
            True  -> The simulation is exexuted on GPU
            False -> The simulation is executed on CPU

        - simulation_method: Simulation method (or backend). It can be any
            method of qiskit's AerSimulator simulator. We must remember that not
            all simulation methods are available if we decide to use GPU.

            Default= "statevector"
        
        - shots: The number of shot we use in the execution of the simulation.

            Default: -1 --> 100*M*2**n

        - print_results: Boolean variable.
            True  -> The function print the len(M_list)+2 states with the most 
                     counts after simulation.
            False -> No results printouts.

            Default: True
    
    Outputs:
        - results: Result object that returns the qiskit AerSimulator. That is:
                result = sim.run(t_circuit, shots = shots).result()

    '''

    ############################################################################
    ###### SOME PRE-CIRCUIT CALCULATIONS 
    ############################################################################
       
    if type(M_list) != list and type(M_list) != tuple:
        M_list = [M_list]
    
    M_list = set(M_list) # We eliminate repeated values

    N=2**n

    M=len(M_list)  # Number M of solutions that we want to find

    # Default number of shots.
    if shots == -1:
        shots = 100*M*2**n

    # ======================================================
    # Some error messages

    if M > N:
        print('\nERROR: M > N (más soluciones que valores en el dataset)')
        exit(1)

    if max(M_list) >= N:
        print('\nERROR: El valor M = %d es mayor que N - 1 = 2^%d - 1 = %d' 
               %(max(M_list), n, N-1))
        exit(2)

    for m in M_list:
        if type(m) != int:
            print('\nERROR: A value of M is not integer.')
            exit(3)


    # ======================================================
    # We put the solutions in binary

    #M_list_bin=[bin(m)[2:].zfill(n) for m in M_list]
    M_list_bin = ggaf.int_to_n_bin(M_list, n)
    # We flip the binary strings because the notation of qiskit is reversed. 
    # In qiskit, the first bit is the least significant bit.
    M_list_bin_qiskit=[ m[::-1] for m in M_list_bin]

    ############################################################################
    ###### PRINTS
    ############################################################################
    
    print('\n====================================================')
    print(f'Number of qubits = {n}')
    print(f'We are looking for {M} solutions : ')
    print(f'   - Decimal: {M_list}')
    print(f'   - Binary: {M_list_bin}')
    print(f'Number of shots = {shots} (default = 100 * M * 2**n)')
    print(f'GPU use = {gpu}')

    ############################################################################
    ###### CIRCUIT
    ############################################################################

    # ======================================================
    # We build the citcuit with the quantum registers
    quantum_reg = QuantumRegister(n)
    classic_reg = ClassicalRegister(n)
    circuit = QuantumCircuit(quantum_reg, classic_reg)
    
    # ======================================================
    # We apply the initialization function. This time we use H^n
    ggaf.initialize_uniform_dist_Hadammads(circuit, quantum_reg)

    # ======================================================
    # Number of iterations
    T = ggaf.Iterations_T(N, M)
       
    # ======================================================
    # We add the grover oracle and diffuser T times

    for _ in range(T):
        Grover_Oracle_trivial(circuit, quantum_reg, M_list_bin_qiskit)
        Grover_Diffuser(circuit, quantum_reg)

    # ======================================================
    # Measure all qubits on the quantum_reg into the classic_reg

    circuit.measure(quantum_reg, classic_reg)

    # ======================================================
    print(f'The circuit has been built ({n} qubits)')
    print(f'\nNumber of Grover iteration: {T}')
    print('====================================================')

    ############################################################################
    ###### SIMULATION
    ############################################################################

    sim = AerSimulator(method = simulation_method) 
    
    if gpu:    
        sim.set_options(device='GPU')
    else:
        sim.set_options(device='CPU')

    
    t_circuit = transpile(circuit, backend = sim) #, optimization_level = 3)
    result = sim.run(t_circuit, shots = shots).result()

    ############################################################################
    ###### PRINTING THE RESULTS 
    ############################################################################
    if print_result == True:

        counts = result.get_counts()

        # ======================================================
        # We order the states from most counts to least

        # keys = list(counts.keys())

        keys_bin = list(counts.keys())
        keys = [int(keys_bin[i],2) for i in range(len(keys_bin))] 

        values = list(counts.values())
        zip_list = zip(keys,values)
        zip_sorted = list(sorted(zip_list, key = lambda x: -x[1]))
        keys, values = zip(*list(zip_sorted))
        
        num_sols = len(list(zip_sorted))
        
        print_range = M + 2 
        if num_sols < print_range:
            print_range = num_sols

        print(f'\nThe algorithm found {num_sols} results.')
        print(f'The {print_range} results with more counts are:')
        print('\n   Result | Counts')
        for i in range(print_range):
            print('   ',list(zip_sorted)[i])
    
    ############################################################################
    ###### RETURN
    ############################################################################

    return result












def Grover_simulation_permutations_P_numbers(P, shots =  -1, 
                                        more_qubits_less_gates = False,
                                        gpu = False, 
                                        simulator_method = "statevector",
                                        print_result = True,
                                        force_simulation = False):
    '''
    This function build circuit and execute the simulation. This function finds
    the 24 possible permutations of the four numbers 0, 1, 2 and 3. That is:
        0123, 0132, 0213,...
        
    Inputs:
        - P: Number of numbers of which we want to calculate the permutations. 
            Must be a power of 2.
    
        - shots: The number of shot we use in the execution of the simulation.

            Default: 100*2**n

        - more_qubits_less_gates: Boolean. The function has two ways of 
            construct the circuit. One of then use Less Qubits but More Gates 
            and the other one use More Qubits but Less  Gates.
              False -> Less Qubits but More Gates
              True  -> More Qubits but Less Gates


        - gpu: Boolean variable. 
            True  -> The simulation is exexuted on GPU
            False -> The simulation is executed on CPU

        - simulation_method: Simulation method (or backend). It can be any
            method of qiskit's AerSimulator simulator. We must remember that not
            all simulation methods are available if we decide to use GPU.

            Default= "statevector"
        
        - print_results: Boolean variable.
            True  -> The function print the len(M_list)+2 states with the most 
                     counts after simulation.
            False -> No results printouts.

            Default: True

        - force_simulation: Boolean.
            False: The simulation does not run if the circuit has more than 
                30 qbits.
            True:  The simulation will always try to run
    
    Outputs:
        - results: Result object that returns the qiskit AerSimulator. That is:
                result = sim.run(t_circuit, shots = shots).result()

    '''
    
    ############################################################################
    ###### SOME PRE-CIRCUIT CALCULATIONS (NUMBERS AND CONDITIONS)
    ############################################################################

    # ======================================================
    # Number of qubits (2 per number):
    P_aux = P
    figures_of_each_P = 0 
    while P_aux >1:
        P_aux = P_aux/2
        figures_of_each_P += 1

    if 2**figures_of_each_P != P:
        print('\nERROR: P must be a power of 2')
        exit(1)

    n = P*figures_of_each_P 
    N = 2**n  # states

    if shots == -1:
        shots = 100*2**n


    # Our list of numbers: [a, b, c, d, ...]
    numbers = [ [ i*figures_of_each_P+j for j in range(int(figures_of_each_P))]  
            for i in range(P)]
    

    # ======================================================
    # Number of solutions
    M = np.math.factorial(P)
 
    # ======================================================
    # Number of iterations
    T = ggaf.Iterations_T(N, M)

    # ======================================================
    # Conditions

    # Each condition of the form [a,b] means that "a" must be diferent from "b".
    # As we want the permutations of 4 numbers, each number must be different from the others
    conditions_list = []

    for i in range(P-1):
        for j in range(i+1,P):
            conditions_list.append([numbers[i], numbers[j]])

    num_conditions = len(conditions_list)

    ############################################################################
    ###### CIRCUIT
    ############################################################################

    # ======================================================
    # Quantum Registers

    # Quantum register when we are going to have the  variables (answer). We measure it
    var_reg = QuantumRegister(n, name='v') 
    classic_reg = ClassicalRegister(n, name='classic_reg')


    # "Conditions" Quantum register. We use them to make sure that the var_reg meets the conditions
    if more_qubits_less_gates == False:
        ancilla_reg = QuantumRegister(figures_of_each_P, name = 'c')
    else:
        ancilla_reg = QuantumRegister(figures_of_each_P*num_conditions, name='c')
    
    ancilla_2_reg = QuantumRegister(num_conditions, name='c_out')
    ancilla_out_qubit = QuantumRegister(1, name='out')

    # ======================================================
    # Circuit
    circuit = QuantumCircuit(var_reg, ancilla_reg,  ancilla_2_reg, 
                            ancilla_out_qubit, classic_reg)

    # ======================================================
    # Initialization
    
    # Initialize qubits in the var_reg.  This time we use H^n
    ggaf.initialize_uniform_dist_Hadammads(circuit, var_reg)

    # Initialize 'ancilla_out_qubit' in state |->
    circuit.x(ancilla_out_qubit)
    circuit.h(ancilla_out_qubit)

    # ======================================================
    # We add the grover oracle and diffuser T times

    for i in range(T):
        if more_qubits_less_gates == False:
            Grover_Oracle_permutations_P_numbers_LQMG(circuit, var_reg, 
                conditions_list, ancilla_reg,  
                ancilla_2_reg, ancilla_out_qubit, print_oracle = i)
        else:
            Grover_Oracle_permutations_P_numbers_MQLG(circuit, var_reg, 
                conditions_list, ancilla_reg,  
                ancilla_2_reg, ancilla_out_qubit, print_oracle = i)


        circuit.barrier()  # for visual separation
        # circuit.append(diffuser(8), [0,1,2,3,4,5,6,7])
        Grover_Diffuser(circuit, var_reg)

    # ======================================================
    # Measure qubits on the var_reg into the classic_reg
    circuit.measure(var_reg, classic_reg)
    #circuit.measure_all()


    ############################################################################
    ###### PRINTS and DRAW
    ############################################################################
    
    
    print('\n====================================================')
    numbers_decimal = [i for i in range(P)]
    print(f'We are looking for the permutations of {P} number {numbers_decimal}.')

    if more_qubits_less_gates == False:
        total_qubits = n+2+num_conditions+1
        print(f'The circuit has been built ({total_qubits} qubits)')
    else:
        total_qubits = n+3*num_conditions+1
        print(f'The circuit has been built ({total_qubits} qubits)')
    
    try:
        circuit.draw(output = 'mpl',fold=-1, 
            filename = f'2-Fig_permutations_{P}_numbers_{total_qubits}_qubits.png')
    except:
        print('WARNING: Circuit to large to generate the image.')
        print('')
    


    if n+2+num_conditions+1 > 30:
        print('\nERROR: Too much qubits. We better not continue with the simulation.')
        print('If ypu want to continue add the argument "force_simulation = True"')
        print('to the call of the function.')
        if force_simulation != True:        
            exit(3)

    print(f'Executing simulation with {shots} shots.')
    print(f'Use of GPU = {gpu}.')
    print(f'MQLG option = {more_qubits_less_gates}.')
    ############################################################################
    ###### SIMULATION
    ############################################################################

    if gpu:
        sim = AerSimulator(method = simulator_method, device = "GPU") 
    else:
        sim = AerSimulator(method = simulator_method, 
                           max_parallel_threads = mp.cpu_count()/2) 

    tqc = transpile(circuit, backend = sim) # optimization_level = 3

    
    result = sim.run(tqc, shots = shots).result()


    ############################################################################
    ###### PRINTING THE RESULTS 
    ############################################################################

    if print_result == True:

        counts = result.get_counts()
        keys_bin = list(counts.keys())
        # ===================================
        # We make the results beautiful

        
        def split_4(keys_bin,n,P):
            lista = [int(keys_bin[i:i+int(n/P)],2) for i in range(0,n,int(n/P))]
            numero = ''.join(map(str, lista))
            numero_formateado = str(numero).zfill(P)
            return numero_formateado


        keys = [split_4(keys_bin[i],n,P) for i in range(len(keys_bin))]
        
        #keys = counts_all.keys()
        
        values = list(counts.values())
        zip_list = zip(keys,values)
        zip_sorted = list(sorted(zip_list, key = lambda x: -x[1]))
        keys, values = zip(*list(zip_sorted))

        num_sols = len(list(zip_sorted))
        print_range = M +2 
        if num_sols < print_range:
            print_range = num_sols

        print(f'\nThe algorithm found {num_sols} results')
        print(f'The {print_range} results with more counts')
        print('\nPermutations | Counts')
        for i in range(print_range):
            print(list(zip_sorted)[i])

    ############################################################################
    if P == 2:
        print('\nAs you can see, for P = 2 the algorithm doesn\' work. It is because')
        print('M = N/2 and the algorithm can\'t amplify' )
        print('(where M = num_solutions)')

    ############################################################################
    ###### RETURN
    ############################################################################

    return result


































































"""

def Grover_simulation_permutations_4_num_27_qubits(shots =  100*2**8, gpu = False, 
                                        simulator_method = "statevector",
                                        print_result = True):
    '''
    This function build circuit and execute the simulation. This function finds
    the 24 possible permutations of the four numbers 0, 1, 2 and 3. That is:
        0123, 0132, 0213,...
    It use 27 qubits but less gates than the 17 qubit version.
    
    Inputs:
        
        - shots: The number of shot we use in the execution of the simulation.

            Default: 100*2**8

        - gpu: Boolean variable. 
            True  -> The simulation is exexuted on GPU
            False -> The simulation is executed on CPU

        - simulation_method: Simulation method (or backend). It can be any
            method of qiskit's AerSimulator simulator. We must remember that not
            all simulation methods are available if we decide to use GPU.

            Default= "statevector"
        
        - print_results: Boolean variable.
            True  -> The function print the len(M_list)+2 states with the most 
                     counts after simulation.
            False -> No results printouts.

            Default: True
    
    Outputs:
        - results: Result object that returns the qiskit AerSimulator. That is:
                result = sim.run(t_circuit, shots = shots).result()

    '''
    
    ############################################################################
    ###### SOME PRE-CIRCUIT CALCULATIONS (NUMBERS AND CONDITIONS)
    ############################################################################

    # ======================================================
    # Number of qubits (2 per number):
    n = 8     # qubits
    N = 2**n  # states

    # Our list of four numbers: [a, b, c, d]
    a = [0, 1]  # 'a' is encoded in qubits 0 and 1
    b = [2, 3]  # 'b' is encoded in qubits 2 and 3
    c = [4, 5]  # 'c' is encoded in qubits 4 and 5
    d = [6, 7]  # 'd' is encoded in qubits 6 and 7
    

    # ======================================================
    # Number of solutions
    M = 24 # We have 4 number, so the permutations are 4! = 4*3*2*1 = 24
 
    # ======================================================
    # Number of iterations
    T = ggaf.Iterations_T(N, M)

    # ======================================================
    # Conditions

    # Each condition of the form [a,b] means that "a" must be diferent from "b".
    # As we want the permutations of 4 numbers, each number must be different from the others
    conditions_list = [[a,b], [a,c], [a,d],   # a different from b, c, d
                       [b,c], [b,d],          # b different from c, d
                       [c,d]]                 # c different from d

    num_conditions = len(conditions_list)


    ############################################################################
    ###### CIRCUIT
    ############################################################################

    # ======================================================
    # Quantum Registers

    # Quantum register when we are going to have the  variables (answer). We measure it
    var_reg = QuantumRegister(n, name='v') 
    classic_reg = ClassicalRegister(n, name='classic_reg')

    # "Conditions" Quantum register. We use them to make sure that the var_reg meets the conditions
    conditions_reg = QuantumRegister(2*num_conditions, name='c')
    conditions_out_reg = QuantumRegister(num_conditions, name='c_out')
    ancilla_out_qubit = QuantumRegister(1, name='out')

    # ======================================================
    # Circuit
    circuit = QuantumCircuit(var_reg, conditions_reg,  conditions_out_reg, 
                            ancilla_out_qubit, classic_reg)

    # ======================================================
    # Initialization
    
    # Initialize qubits in the var_reg.  This time we use H^n
    ggaf.initialize_uniform_dist_Hadammads(circuit, var_reg)

    # Initialize 'ancilla_out_qubit' in state |->
    circuit.x(ancilla_out_qubit)
    circuit.h(ancilla_out_qubit)

    # ======================================================
    # We add the grover oracle and diffuser T times

    for _ in range(T):
        go.Grover_Oracle_permutations_4_oracle_27_qubits(circuit, var_reg, 
                conditions_list, conditions_reg, 
                conditions_out_reg, ancilla_out_qubit)
        
        circuit.barrier()  # for visual separation
        # circuit.append(diffuser(8), [0,1,2,3,4,5,6,7])
        Grover_Diffuser(circuit, var_reg)

    # ======================================================
    # Measure qubits on the var_reg into the classic_reg
    circuit.measure(var_reg, classic_reg)


    ############################################################################
    ###### PRINTS and DRAW
    ############################################################################
    
    circuit.draw(output = 'mpl',fold=-1, 
                 filename = '2-1_Fig_permutations_4_numbers_27_qubits')

    print('\n====================================================')
    print('We are looking for the permutations of 4 number (0, 1, 2, 3).')
    print(f'The circuit has been built ({n+3*num_conditions+1} qubits)')
    print(f'Executing simulation with {shots} shots.')
    print(f'Use of GPU = {gpu}.')
    print('\n====================================================')

    ############################################################################
    ###### SIMULATION
    ############################################################################

    if gpu:
        sim = AerSimulator(method = simulator_method, device = "GPU") 
    else:
        sim = AerSimulator(method = simulator_method, 
                           max_parallel_threads = mp.cpu_count()/2) 

    tqc = transpile(circuit, backend = sim) # optimization_level = 3

    
    result = sim.run(tqc, shots = shots).result()


    ############################################################################
    ###### PRINTING THE RESULTS 
    ############################################################################

    if print_result == True:

        counts = result.get_counts()

        # ===================================
        # We make the results beautiful

        keys_bin = list(counts.keys())

        def split_4(Value):
            lista = [int(Value[i:i+2],2) for i in range(0,8,2)]
            numero = ''.join(map(str, lista))
            numero_formateado = "{:0>4}".format(numero)
            return numero_formateado


        keys = [split_4(keys_bin[i]) for i in range(len(keys_bin))]

        values = list(counts.values())
        zip_list = zip(keys,values)
        zip_sorted = list(sorted(zip_list, key = lambda x: -x[1]))
        keys, values = zip(*list(zip_sorted))

        num_sols = len(list(zip_sorted))
        print_range = M +2 
        if num_sols < print_range:
            print_range = num_sols

        print(f'\nThe algorithm found {num_sols} results')
        print(f'The {print_range} results with more counts')
        print('\nPermutations | Counts')
        for i in range(print_range):
            print(list(zip_sorted)[i])

    ############################################################################
    ###### RETURN
    ############################################################################

    return result

"""







"""
def Grover_simulation_permutations_4_num_17_qubits(shots =  100*2**8, gpu = False, 
                                        simulator_method = "statevector",
                                        print_result = True):
    '''
    This function build circuit and execute the simulation. This function finds
    the 24 possible permutations of the four numbers 0, 1, 2 and 3. That is:
        0123, 0132, 0213,...
    It use 17 qubits but more gates than the 27 qubit version.
    
    Inputs:
        
        - shots: The number of shot we use in the execution of the simulation.

            Default: 100*2**8

        - gpu: Boolean variable. 
            True  -> The simulation is exexuted on GPU
            False -> The simulation is executed on CPU

        - simulation_method: Simulation method (or backend). It can be any
            method of qiskit's AerSimulator simulator. We must remember that not
            all simulation methods are available if we decide to use GPU.

            Default= "statevector"
        
        - print_results: Boolean variable.
            True  -> The function print the len(M_list)+2 states with the most 
                     counts after simulation.
            False -> No results printouts.

            Default: True
    
    Outputs:
        - results: Result object that returns the qiskit AerSimulator. That is:
                result = sim.run(t_circuit, shots = shots).result()

    '''
    
    ############################################################################
    ###### SOME PRE-CIRCUIT CALCULATIONS (NUMBERS AND CONDITIONS)
    ############################################################################

    # ======================================================
    # Number of qubits (2 per number):
    n = 8     # qubits
    N = 2**8  # states

    # Our list of four numbers: [a, b, c, d]
    a = [0, 1]  # 'a' is encoded in qubits 0 and 1
    b = [2, 3]  # 'b' is encoded in qubits 2 and 3
    c = [4, 5]  # 'c' is encoded in qubits 4 and 5
    d = [6, 7]  # 'd' is encoded in qubits 6 and 7
    

    # ======================================================
    # Number of solutions
    M = 24 # We have 4 number, so the permutations are 4! = 4*3*2*1 = 24
 
    # ======================================================
    # Number of iterations
    T = ggaf.Iterations_T(N, M)

    # ======================================================
    # Conditions

    # Each condition of the form [a,b] means that "a" must be diferent from "b".
    # As we want the permutations of 4 numbers, each number must be different from the others
    conditions_list = [[a,b], [a,c], [a,d],   # a different from b, c, d
                       [b,c], [b,d],          # b different from c, d
                       [c,d]]                 # c different from d

    num_conditions = len(conditions_list)


    ############################################################################
    ###### CIRCUIT
    ############################################################################

    # ======================================================
    # Quantum Registers

    # Quantum register when we are going to have the  variables (answer). We measure it
    var_reg = QuantumRegister(n, name='v') 
    classic_reg = ClassicalRegister(n, name='classic_reg')


    # "Conditions" Quantum register. We use them to make sure that the var_reg meets the conditions
    #conditions_reg = QuantumRegister(2*num_conditions, name='c')
    ancilla_reg = QuantumRegister(2, name = 'c')
    # conditions_out_reg = QuantumRegister(num_conditions, name='c_out')
    ancilla_2_reg = QuantumRegister(num_conditions, name='c_out')
    ancilla_out_qubit = QuantumRegister(1, name='out')

    # ======================================================
    # Circuit
    circuit = QuantumCircuit(var_reg, ancilla_reg,  ancilla_2_reg, 
                            ancilla_out_qubit, classic_reg)

    # ======================================================
    # Initialization
    
    # Initialize qubits in the var_reg.  This time we use H^n
    ggaf.initialize_uniform_dist_Hadammads(circuit, var_reg)

    # Initialize 'ancilla_out_qubit' in state |->
    circuit.x(ancilla_out_qubit)
    circuit.h(ancilla_out_qubit)

    # ======================================================
    # We add the grover oracle and diffuser T times

    for _ in range(T):
        go.Grover_Oracle_permutations_4_oracle_17_qubits(circuit, var_reg, 
                conditions_list, ancilla_reg,  
                ancilla_2_reg, ancilla_out_qubit)
        
        circuit.barrier()  # for visual separation
        # circuit.append(diffuser(8), [0,1,2,3,4,5,6,7])
        Grover_Diffuser(circuit, var_reg)

    # ======================================================
    # Measure qubits on the var_reg into the classic_reg
    circuit.measure(var_reg, classic_reg)


    ############################################################################
    ###### PRINTS and DRAW
    ############################################################################
    
    circuit.draw(output = 'mpl',fold=-1, 
                 filename = '2-2_Fig_permutations_4_numbers_17_qubits')

    print('\n====================================================')
    print('We are looking for the permutations of 4 number (0, 1, 2, 3).')
    print(f'The circuit has been built ({n+2+num_conditions+1} qubits)')
    print(f'Executing simulation with {shots} shots.')
    print(f'Use of GPU = {gpu}.')
    print('\n====================================================')

    ############################################################################
    ###### SIMULATION
    ############################################################################

    if gpu:
        sim = AerSimulator(method = simulator_method, device = "GPU") 
    else:
        sim = AerSimulator(method = simulator_method, 
                           max_parallel_threads = mp.cpu_count()/2) 

    tqc = transpile(circuit, backend = sim) # optimization_level = 3

    
    result = sim.run(tqc, shots = shots).result()


    ############################################################################
    ###### PRINTING THE RESULTS 
    ############################################################################

    if print_result == True:

        counts = result.get_counts()
        keys_bin = list(counts.keys())
        # ===================================
        # We make the results beautiful

        
        def split_4(Value):
            lista = [int(Value[i:i+2],2) for i in range(0,8,2)]
            numero = ''.join(map(str, lista))
            numero_formateado = "{:0>4}".format(numero)
            return numero_formateado


        keys = [split_4(keys_bin[i]) for i in range(len(keys_bin))]
        
        #keys = counts_all.keys()

        values = list(counts.values())
        zip_list = zip(keys,values)
        zip_sorted = list(sorted(zip_list, key = lambda x: -x[1]))
        keys, values = zip(*list(zip_sorted))

        num_sols = len(list(zip_sorted))
        print_range = M +2 
        if num_sols < print_range:
            print_range = num_sols

        print(f'\nThe algorithm found {num_sols} results')
        print(f'The {print_range} results with more counts')
        print('\nPermutations | Counts')
        for i in range(print_range):
            print(list(zip_sorted)[i])

    ############################################################################
    ###### RETURN
    ############################################################################

    return result

"""