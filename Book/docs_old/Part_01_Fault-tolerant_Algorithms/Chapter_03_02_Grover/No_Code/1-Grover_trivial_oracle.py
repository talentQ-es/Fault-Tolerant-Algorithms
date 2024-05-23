import Grover_Simulation_Functions as gsf

import argparse
#import cuquantum

############################################################################
###### Arguments: n, gpu, sols, shots
############################################################################

parser=argparse.ArgumentParser()

parser.add_argument('-n', dest='n_qubits', type = int, 
    help='Enter the number of qubits')

parser.add_argument('-gpu', dest='gpu', type = str, 
    help='Enter True for use GPU, and False to use CPU')

parser.add_argument('-sols', dest='sols', 
    help='Enter the numbers you want to find. ')

parser.add_argument('-shots', dest='shots', type = int,
    help='Enter the numbers you want to find. ')

args = parser.parse_args()

# ===========================================================
# If you do not pass any arguments to the script, 
# it will ask you for them on the screen 
# ===========================================================
if (args.n_qubits == None and args.sols == None 
    and args.shots == None and args.gpu == None):

    n = int(input('Number of qubits: '))
    sols = eval(input('Solutions that you want to find (from 0 to 2^n-1): ')) # List with solucions
    shots = int(input('Number of shots (type -1 to choose the default value): '))
    gpu = -1
    
    while gpu != 0 and gpu != 1:
        gpu = int(input('Uso de GPU? (0 = No, 1 = Yes) = '))
        
    gpu = bool(gpu)

# ===========================================================
# If you pass arguments. 
# You must pass at least -n and -sols
# ===========================================================
else:
    n = args.n_qubits # Number of qubits
    shots = args.shots

    if n == None:
        print('ERROR: You must specify the number of qubit (-n)')
        exit(1)
    if args.sols == None:
        print('ERROR: You must specify the desire solutions (-sols)')
        exit(2)
    else:
        sols = eval(args.sols) # List with solucions

    if shots == None:
        shots = -1

    if args.gpu == 'True':
        gpu = True
    else:
        gpu = False


############################################################################
###### CIRCUIT BUILDING, SIMULATION and PRINTING RESULTS
############################################################################

result = gsf.Grover_simulation_trivial_oracle(n, sols, gpu = gpu, 
                                            simulation_method = "statevector",
                                            shots = shots, 
                                            print_result = True)
