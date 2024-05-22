'''
You can ran this script sending it to a queue system (like slurm) using the 
sentence 
    python Qiskit_Shor_2n_plus_3_Supercomputer.py 
        -N      -> number_to_factorize 
        -a      -> value_of_a (optinal. Default: a = random)
        -shots  -> shots_per_execution (optional. Default: shots = 3)
        -ashots -> number of global executions with the same a value (max_shots parameter)
        -approx -> approx_QFT (optional. Default approx_QFT = 0)
        -g      -> GPU support (optional. Default = 0 -> False)
        -cuQ    -> cuQuantum support (optional. Default = 0 -> False)

Exameples:
    python Qiskit_Shor_2n_plus_3.py -N 15 
    python Qiskit_Shor_2n_plus_3.py -N 15 -a 7
    python Qiskit_Shor_2n_plus_3.py -N 15 -a 7 -shots_execution 5
    python Qiskit_Shor_2n_plus_3.py -N 15 -approx 2
    python Qiskit_Shor_2n_plus_3.py -N 15 -shots 5 -approx 2

Otherwise, you can ran it with no parameter and you will be prompted to enter 
via the terminal the parameters.


Requirements:
    - Python 3.8 or higher
    - Qiskit 0.38.0 or higher (maybe with an older version it works) 
    - Qiskit_aer 0.11 or higher (maybe with an older version it works) 
'''


import Qiskit_Shor_Gates_and_Functions as gaf
import Qiskit_Shor_Simulation_Functions as sf

import argparse

################################################################################
###### Arguments
################################################################################

parser=argparse.ArgumentParser()
parser.add_argument('-N', dest='N', type = int,  
                     help='Enter the number to factorize')

parser.add_argument('-a', dest='a', type = int, 
                    # default = 0, #If we give a=0, the program choose a random value of a
                    help='Enter the number a')

parser.add_argument('-shots_execution', dest='shots_per_execution', type = int, 
                    # default = 3,
                    help='Enter the number of shots per execution')

parser.add_argument('-shots_per_a', dest='a_shots', type = int, # required=False,
                    #default = 3,
                    help='Enter the number of shots per execution')

parser.add_argument('-approx', dest='approx_QFT', type = int, 
                    # default = 0,
    help='''Enter de degree of aproximation in the QFTs. 
    If it is 0, there is no aproximation. 
    If it is 1, we obviate the lower angle gates (\pi/2^n) in the QFT, where n is 
    the number of qubits in which the QFT is applied. 
    If it is 2, we also skip the next lowest angle gates (\pi/2^{n-1}). 
    So, successively (3, 4, ...). 
    By default, it is 0, i.e., we use all the gates.''')

parser.add_argument('-g', dest='gpu', type = int, 
                    # default = 0, #If we give a=0, the program choose a random value of a
                    help='Enter 1 to use GPU support')

parser.add_argument('-cuQ', dest='cuQuantum', type = int,
                    # default = 0, #If we give a=0, the program choose a random value of a
                    help='Enter 1 to use cuQuantum library.')


args = parser.parse_args()

N = args.N
new_N = N
a = args.a
shots_per_execution = args.shots_per_execution
approx_QFT = args.approx_QFT
gpu = args.gpu
cuQuantum = args.cuQuantum
a_shots = args.a_shots




# If you do not pass any arguments to the script, it will ask you for them on the screen 
if N == None and a == None and shots_per_execution == None and \
    approx_QFT == None and gpu == None and cuQuantum == None and \
    a_shots == None :

    N = int(input('Type the number N that you want to factor: '))
    new_N = N
    print('input number was: {0}\n'.format(N), flush = True)

    # ====================================
    # Tests to see if it is an ease case
    gaf.test_simple_cases(N)

    print('Not an easy case, using the quantum circuit is necessary\n', flush = True)

    # ====================================
    ### Choose the value of a and do the simulation 
    
    a = int(input('Type 0 to use a random value of a. Otherwise, type the value of a: '))

    if a < 0 or a >=N: 
        print('The value of a must be 1>a>',N,'. Type a new one: ')
        exit(1)

    if a == 0: 
        print("\nChoose every how many shots you want to try with ")
        a_shots = int(input('a new value of "a". Type 0 to default (default N): '))

    else:
        print('The value of a is ', a, flush = True)

    # ====================================
    ### shots_per_execution
    print("\nThe algoritm do P shots and then review the posible answers.")
    print("If with these answers the algorithm has not yet found all the ")
    print("factors, it reruns the P shots.")
    shots_per_execution = int(input('Choose a number P: '))

    # ====================================
    ### GPU
    
    gpu = -1
    while gpu != 0 and gpu != 1:
        gpu = int(input('\nType 1 to use GPU. Type 0 otherwise: '))

    gpu = bool(gpu)
    print('Use GPU = ', gpu)

    # ====================================
    ### cuQuantum
    cuQuantum = -1
    while cuQuantum != 0 and cuQuantum != 1:
        cuQuantum = int(input('\nType 1 to use cuQuantum library. Type 0 otherwise: '))

    cuQuantum = bool(cuQuantum)
    print('Use GPU = ', cuQuantum)

    # ====================================
    # QFT approx
    print('''\nEnter de degree of aproximation in the QFTs. 
        If it is 0, there is no aproximation. 
        If it is 1, we obviate the lower angle gates (\pi/2^n) in the QFT, where n is 
        the number of qubits in which the QFT is applied. 
        If it is 2, we also skip the next lowest angle gates (\pi/2^{n-1}). 
        So, successively (3, 4, ...). ''', flush = True)

    approx_QFT = 0
    approx_QFT  = int(input('\nApproximation degree of the QFTs: '))



# If you pass arguments
else: 
    if N == None:
        print("You must specify the value of N to be factorize (example -N 15)")
        exit(1)

    print('input number was: {0}\n'.format(N), flush = True)

    # ====================================
    # Tests to see if it is an ease case
    gaf.test_simple_cases(N)

    print('Not an easy case, using the quantum circuit is necessary\n', flush = True)



    if a == None:
        a = 0
    
    if shots_per_execution == None:
        shots_per_execution = 3
    
    if approx_QFT == None: 
        approx_QFT = 0
    
    if gpu == 'True' or gpu == 1:
        gpu = True
    else:
        gpu = False

    if cuQuantum == 'True' or cuQuantum == 1:
        cuQuantum = True
    else:
        cuQuantum = False

    
    if a_shots == None:
        a_shots = 0



################################################################################
###### CIRCUIT BUILDING, SIMULATION and PRINTING RESULTS
################################################################################
factors = []

if a == 0 :
    No_factors = True
    while No_factors:
        a = gaf.get_value_a(new_N)
        No_factors, factors, new_N = sf.simulation_2n_plus_3(a,new_N, N, 
                                     factors, shots_per_execution, 
                                     max_shots = a_shots,
                                     approx_QFT = approx_QFT,
                                     gpu = gpu, cuQuantum = cuQuantum) #method      
else:
    No_factors = True
    while No_factors:

        gaf.test_a(a, new_N) # We see if the given a is coprime with N.

        No_factors, factors, new_N = sf.simulation_2n_plus_3(a, new_N, N, 
                                     factors, shots_per_execution , 
                                     max_shots = a_shots,
                                     approx_QFT = approx_QFT,
                                     gpu = gpu, cuQuantum = cuQuantum) #method