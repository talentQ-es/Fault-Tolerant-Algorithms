import sys
import shutil
import os
import time
import argparse

# Get the number of sbatch files to generate from argument
# Example:
# python3 lanza_gestor_slurm.py -experiment-name prueba -iters 2 -N 15 -a 

parser=argparse.ArgumentParser()

parser.add_argument('-experiment_name', dest='name', type = str, required=True, 
                            help='Enter the name')

#The aim of iters is to loop over diferent settings....
parser.add_argument('-jobs', dest='num_sbatch', type = int, required=True, 
                             help='Enter the number to factorize')


parser.add_argument('-N', dest='N', type = int, required=True, 
                             help='Enter the number to factorize')

parser.add_argument('-a', dest='a', type = int, required=False,
                            default = 0, help='Enter a, need the same a for all the experiments')

parser.add_argument('-shots', dest='shots_per_execution', type = int, required=False,
                            default = 3,
                                                help='Enter the number of shots per execution')

parser.add_argument('-shots_per_a', dest='ashots', type = int, required=False,
                            default = 3,
                                                help='Enter the number of shots per execution')
parser.add_argument('-approx', dest='approx_QFT', type = int, required=False,
                            default = 0,
                                help='''Enter de degree of aproximation in the QFTs. 
                                    If it is 0, there is no aproximation. 
                                    If it is 1, we obviate the lower angle gates (\pi/2^n) in the QFT, where n is 
                                    the number of qubits in which the QFT is applied. 
                                    If it is 2, we also skip the next lowest angle gates (\pi/2^{n-1}). 
                                    So, successively (3, 4, ...). 
                                    By default, it is 0, i.e., we use all the gates.''')

parser.add_argument('-g', dest='gpu', type = int, required=False,
                            default = 0, #If we give a=0, the program choose a random value of a
                                                help='Enter 1 to use GPU support')

parser.add_argument('-cuQ', dest='cuQuantum', type = int, required=False,
                            default = 0, #If we give a=0, the program choose a random value of a
                                                help='Enter 1 to use cuQuantum library.')



#collect the arguments
args = parser.parse_args()

num_sbatch = args.num_sbatch
name = args.name
ashots=args.ashots
N=args.N
shots_per_execution = args.shots_per_execution
approx_QFT = args.approx_QFT

gpu = args.gpu
cuQuantum = args.cuQuantum

a = args.a


if not os.path.exists("experiments"):
    os.mkdir("experiments")

# Get the name of the directory from the command line argument

dir_name = "experiments/"+name

# Check if the directory already exists
if os.path.exists(dir_name):
    print("Directory already exists. Aborting.")
    sys.exit()

# Create the directory
os.mkdir(dir_name)
os.mkdir(dir_name+"/results")
shutil.copy2(str(sys.argv[0]), dir_name+"/"+str(sys.argv[0]))
print("Directory created:", dir_name)

# Create sbatch files
for i in range(num_sbatch+1):
    filename = dir_name+ "/" +str(name)+"_sbatch_" + str(i) + ".sbatch"
    with open(filename, "w") as f:
        f.write("#!/bin/bash\n")
        #f.write("#SBATCH -J job_" + str(i) + "\n")
        f.write("#SBATCH -o "+ dir_name + "/results/" + str(i) + "_output.txt\n")
        f.write("#SBATCH -e "+ dir_name + "/results/" + str(i) + "_error.txt\n")
        #f.write("#SBATCH --cpus-per-task=1 \n")
        #f.write("#SBATCH --ntasks=" + str(i) + "\n")
        #f.write("#SBATCH -t 10\n")
        f.write("date +%s\n")
        f.write("python Qiskit_Shor_2n_plus_3_Supercomputer.py " + " -N "+str(N)+ " -a "+ str(a) +" -shots "+ str(shots_per_execution)+ " -approx "+ str(i) + " -shots_per_a " + str(ashots) + " -g "+ str(gpu) + " -cuQ "+str(cuQuantum) + "\n")
        f.write("date +%s\n") # get the end time


    # Submit sbatch file to slurm scheduler
    os.system("sbatch " + filename)
