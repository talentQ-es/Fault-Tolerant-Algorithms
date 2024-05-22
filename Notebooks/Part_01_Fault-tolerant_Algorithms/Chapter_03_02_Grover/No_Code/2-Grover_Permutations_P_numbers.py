import Grover_Simulation_Functions as gsf
# from qiskit.visualization import plot_histogram

import argparse

################################################################################
###### Arguments: GPU and Shots
################################################################################

parser = argparse.ArgumentParser()

parser.add_argument('-p', dest='P', type = int,
                    help='''Number of numbers of which we want to calculate the 
                    permutations. Must be a power of 2.''')

parser.add_argument('-gpu', dest='gpu', type = str,
                    help='Enter True for use GPU, and False to use CPU')

parser.add_argument('-shots', dest='shots', type = int, 
                    help='''Number of shots in the execution. Type -1 to use 
                    the default value 100*2^8 ''')

parser.add_argument('-mqlg', dest='MQLG', type = str, 
                    help='''Choose between simulate using less qubit but more gates 
                     (False) or more qubits but less gates (True) ''')

args = parser.parse_args()

# If you do not pass any arguments to the script, it will ask you for them on the screen 
if args.shots == None and args.gpu == None and args.P == None and args.MQLG == None:
    
    print('Press Enter to choose the default options.')
    P = input('''- Number of numbers of which we want to calculate the permutations [Default = 4]: ''')

    if P == '':
        P = 4
    else:
        P = int(P)
    
    shots = input('- Number of shots [Default 100 x 2^#qubits]: ')

    if shots == '':
        shots = -1
    else:
        shots = int(shots)


    gpu = input('- Do you want to use GPU? (True, False). [Default = False]:  ')

    if gpu == 'True':
        gpu = bool(gpu)
    elif gpu != 'False':
        gpu = False
   
    '''
    gpu = -1
    
    while gpu != 0 and gpu != 1:
        gpu = int(input('Uso de GPU? (0 = No, 1 = Yes) = '))
    
    gpu = bool(gpu)
    '''

    MQLG = input('''- More Qubits Less Gates option (False, True). [Default = False]: ''')

    if MQLG == 'True':
        MQLG = bool(MQLG)
    elif MQLG != 'False':
        MQLG = False
   

# If you pass arguments
else:
    P = args.P
    if P == None:
        print('''\nERROR: You must specify the number of number of which you want 
        to calculate the permutations (-P)''')
        exit(1)

    # If you only pass as an argument the number of shots
    if args.gpu == None:
        gpu = False
    
    else:
        if args.gpu == 'True' or args.gpu == 1:
            gpu = True
        else:
            gpu = False

    # If you only pass as an argument the use of GPU
    if args.shots == None:
        shots =  -1
    
    else: 
        shots = args.shots

    if args.MQLG == None:
        MQLG = False
    else:
        MQLG = args.MQLG
        if MQLG == 'True' or MQLG == '1':
            MQLG = bool(MQLG)
        else:
            MQLG = False

################################################################################
###### CIRCUIT BUILDING, SIMULATION and PRINTING RESULTS
################################################################################

result = gsf.Grover_simulation_permutations_P_numbers(P, shots = shots, gpu = gpu,
                                        more_qubits_less_gates = MQLG,
                                        simulator_method = "statevector",
                                        print_result = True, 
                                        force_simulation = False)


