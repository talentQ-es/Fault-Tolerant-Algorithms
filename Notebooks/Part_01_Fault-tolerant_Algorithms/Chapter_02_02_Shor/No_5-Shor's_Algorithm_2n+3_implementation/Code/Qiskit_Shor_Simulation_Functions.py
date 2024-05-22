import Qiskit_Shor_Gates_and_Functions as gaf


""" Imports from qiskit"""
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit import execute, IBMQ, transpile
from qiskit.circuit.library import QFT
from qiskit_aer import AerSimulator

""" Imports to Python functions """
import math

#import fractions
import numpy as np
import random as rd





def simulation_aux(circuit,Shots_per_execution,method, max_shots, N, N_old, a, 
                   n, factors,  gpu, cuQuantum, case_4n_plus_2 = False):

    sim = AerSimulator(method = method)

    if gpu:
        sim.set_options(device='GPU')
    if cuQuantum:
        #import cuquantum
        sim.set_options(cuStateVec_enable=True)

    tqc = transpile(circuit, backend = sim)
    
    N_aux = 1 
    Total_shot = 0
    print(' ', flush = True)
    print('Uso de GPU = ', gpu)
    print('Uso de cuQuantum = ',cuQuantum)

    print(' ', flush = True)
    print('====================================', flush = True)
    print('Executing the circuit the first ', Shots_per_execution,' time(s)\n', flush = True)
    
    new_factors = []

    while True:

        sim_run = sim.run(tqc, shots = Shots_per_execution)
        sim_result=sim_run.result()
        counts_result = sim_result.get_counts(circuit)
        
        for i in range(len(counts_result)):

            print('-> Result \"{0}\" happened {1} times out of {2}'.format(
                  list(sim_result.get_counts().keys())[i],
                  list(sim_result.get_counts().values())[i],Shots_per_execution), 
                  flush = True)

        for i in range(len(counts_result)):
            
            if case_4n_plus_2 == True:
                output_desired = list(sim_result.get_counts().keys())[i]
                phase = int(output_desired, 2)
            else:
                all_registers_output = list(sim_result.get_counts().keys())[i]  
                output_desired = all_registers_output.split(" ")[1]
                phase = int(output_desired, 2)


            
            print(' ', flush = True)
            print("--> Analysing result {0}. ".format(output_desired), flush = True)

            """ Print the final phase to user """
            print('---> In decimal, phase value for this result is: {0}'.format(phase), flush = True)

            """ Get the factors using the x value obtained """   
            new_factors_aux = gaf.find_factors(phase, N, a, n) 
            
            for j in range(len(new_factors_aux)):
                if new_factors_aux[j] in new_factors:
                    continue
                else:
                    new_factors.append(new_factors_aux[j])

        if len(new_factors) > 0:
            new_factors_multi = 1
            for i in range(len(new_factors)):
                new_factors_multi*= new_factors[i]
                factors.append(new_factors[i])

            new_N = int(N/new_factors_multi)

            if gaf.is_prime(new_N):
                if new_N != 1:
                    factors.append(new_N)
                print('The factors of N = ', N_old, ' that we have found are ', factors, flush = True)
                return False, factors, 1
            else:
                return True, factors, new_N 


        Total_shot += Shots_per_execution
        if Total_shot > max_shots:
            print('Reached the maximun number of shots. Try with another value of a', flush = True)
            return True, factors, N
            #break

        print('The factors of N = ', N_old, ' that we have found until now are ', factors, flush = True)
        print('No all factors found. Executing the circuit another ',
            Shots_per_execution, ' time(s)\n', flush = True)
        
        print('====================================', flush = True)


def simulation_4n_plus_2(a, N, N_old, factors,Shots_per_execution = 1,method="statevector",
    max_shots = 0, approx_QFT = 0, gpu = False, cuQuantum = False):
    
    if max_shots == 0:
        max_shots = N

    """ Get n value used in Shor's algorithm, to know how many qubits are used """
    n = math.ceil(math.log(N,2))
    
    print('Total number of qubits used: {0}\n'.format(4*n+2), flush = True)

    """ Create quantum and classical registers """

    """auxilliary quantum register used in addition and multiplication"""
    ancilla_reg = QuantumRegister(n+2)

    '''Count register, i.e., the Quantum Register where we are going to store 
    the phases computed with the Quantum Phase Estimation (QPE) algorithm (thus
    is, we use qubits from this register to control the gates that apply the 
    modular exponential). It is also the quantum register where the sequential 
    QFT is performed. '''
    count_reg = QuantumRegister(2*n)
    
    """quantum register where we apply the modular exponential."""
    down_reg = QuantumRegister(n)
    
    """classical register where the measured values of the QFT are stored"""
    count_classic = ClassicalRegister(2*n)

    """ Create Quantum Circuit """
    circuit = QuantumCircuit(down_reg , count_reg , ancilla_reg, count_classic)

    """ Initialize down register to 1 and create maximal superposition in count register """
    circuit.h(count_reg)
    circuit.x(down_reg[0])

    """ Apply the multiplication gates as showed in the report in order to create the exponentiation """
    for k in range(0, 2*n):
        gaf.cU_a_pow_s(circuit, down_reg, count_reg[k],  ancilla_reg, a, pow(2,k), N, n, approx_QFT)

    """ Apply inverse QFT """
    #create_inverse_QFT(circuit, count_reg, 2*n ,1)
    #circuit.compose(QFT(2*n, inverse=True, do_swaps=True), count_reg)
    circuit.append(QFT(2*n, inverse=True, do_swaps=True, 
                          approximation_degree=approx_QFT).to_gate(), count_reg)

    """ Measure the top qubits, to get x value"""
    circuit.measure(count_reg, count_classic)

    No_factors, factors, new_N = simulation_aux(circuit,Shots_per_execution,method,max_shots, N,
        N_old, a, n, factors, gpu, cuQuantum, case_4n_plus_2 = True)
    return No_factors, factors, new_N


def get_Angle(a, N):
    """convert the number a to a binary string with length N"""
    s=bin(int(a))[2:].zfill(N) 
    angle = 0
    for i in range(0, N):
        """if the digit is 1, add the corresponding value to the angle"""
        if s[N-1-i] == '1': 
            angle += math.pow(2, -(N-i))
    angle *= np.pi
    return angle

def simulation_2n_plus_3(a,N,N_old,factors,Shots_per_execution = 1,method="statevector",
    max_shots = 0, approx_QFT = 0,gpu = False, cuQuantum = False):
    
    if max_shots == 0:
        max_shots = N

    """ Get n value used in Shor's algorithm, to know how many qubits are used """
    n = math.ceil(math.log(N,2))
    
    print('Total number of qubits used: {0}\n'.format(2*n+3), flush = True)

    """ Create quantum and classical registers """

    """auxilliary quantum register used in addition and multiplication"""
    ancilla_reg = QuantumRegister(n+2)

    '''Count register, i.e., the Quantum Register where we are going to store 
    the phases computed with the Quantum Phase Estimation (QPE) algorithm (thus
    is, we use qubits from this register to control the gates that apply the 
    modular exponential). It is also the quantum register where the sequential 
    QFT is performed. '''
    count_reg = QuantumRegister(1)
    
    """quantum register where we apply the modular exponential."""
    down_reg = QuantumRegister(n)
    
    """classical register where the measured values of the QFT are stored"""
    count_classic = ClassicalRegister(2*n)

    """classical bit used to reset the state of the top qubit to 0 if the previous measurement was 1"""
    ancilla_classic = ClassicalRegister(1)



    """ Create Quantum Circuit """
    circuit = QuantumCircuit(down_reg , count_reg , ancilla_reg, 
                             count_classic, ancilla_classic)

    """ Initialize down register to 1 and create maximal superposition in count register """
    circuit.x(down_reg[0])


    """ Cycle to create the Sequential QFT, measuring qubits and applying the right gates according to measurements """
    for i in range(0, 2*n):
        """reset the top qubit to 0 if the previous measurement was 1"""
        circuit.x(count_reg).c_if(ancilla_classic, 1)
        circuit.h(count_reg)
        gaf.cU_a_pow_s(circuit, down_reg, count_reg[0],  ancilla_reg, a, pow(2,(2*n-1-i)), N, n, approx_QFT)
        """cycle through all possible values of the classical register and apply the corresponding conditional phase shift"""
        for j in range(0, 2**i):
            """the phase shift is applied if the value of the classical register matches j exactly"""
            circuit.p(get_Angle(j, i), count_reg[0]).c_if(count_classic, j)
        circuit.h(count_reg)
        circuit.measure(count_reg[0], count_classic[i])
        circuit.measure(count_reg[0], ancilla_classic[0])


    No_factors, factors, new_N = simulation_aux(circuit,Shots_per_execution,method,max_shots, N,
        N_old, a, n, factors,  gpu, cuQuantum)
    return No_factors, factors, new_N



