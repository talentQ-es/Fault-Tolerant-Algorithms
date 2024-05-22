In this folder you can find two implementation of the Grover's Algoritm.

You can run a simple (trivial) version of the algorithm using the script 

    1-Grover_trivial_oracle.py

You can run two version with more practical utility of the algorithm using the script

    2-Grover_Permutations_P_numbers.py

    3-Sudoku_2x2.py

The rest of the scripts contain functions that are called by these two. For this
reason, you must download all the files in this folder to be able to execute the
two scripts mentioned above.

# Requirement

The only requirement is to have [Qiskit](https://qiskit.org/documentation/getting_started.html) 
and [Qiskit_aer](https://pypi.org/project/qiskit-aer/). If you want to use the
GPU option you must install the version of Qiskit with GPU support.

# How to execute 

The script "3-Sudoku_2x2.py" doesn't have any special feature (it doesn't need any
parameter). You can execute then as any other python script.

We have some thing to comment about the other two scripts because they accept
user parameter. Both scripts follow the same logic for execution: if you execute
them from an integrated development environment (such as Spyder or VisualStudio
Code) or if you execute then in terminal with
    
    python 1-Grover_trivial_oracle.py
    python 2-Grover_Permutations_P_numbers.py

you will be prompted to enter via the terminal the parameters. On the other hand, 
these scripts can be executed in terminal by passing the parameters in the call 
itself. For example

    python 1-Grover_trivial_oracle.py -n 10 -sols 1,5,11,20 -gpu False -shots 20000
    python 2-Grover_Permutations_P_numbers.py -p 4 -shots 10000 -gpu False -mqlg False
   
The only parameters required are -n and -sols in the first one and -p in the second 
one. The rest can be omitted and will be assigned default values.

    python 1-Grover_trivial_oracle.py -n 10 -sols 1,5,11,20 
    python 2-Grover_Permutations_P_numbers.py -p 4 

This second option to execute the scripts is intended to send them to be executed in 
the queue system of a supercomputer without having to open an interactive session.
    

# About 1-Grover_trivial_oracle.py

This script takes a number of qubits (user defined) and some solutions (user 
defined) to search for and applies Grover's algorithm to find them. The solutions 
it looks for are nothing but integers between 0 and 2^n-1 (both included). 

The program accepts to search for one or several solutions. 

This is an implementation of the usual way Grover's algorithm is explained. That
is, knowing the solution, create an oracle that marks that solution. Precisely 
for this reason I call it "trivial".

# About 2-Grover_Permutations_P_numbers.py

This script calculates the permutations of P (user defined) numbers. For example, 
if we have P = 4, the script will calculate the permutations of 0,1,2 and 3, i.e.,

    0123, 0132, 1032, 1230, ...

This is a more advanced implementation because what the script does is to build 
an oracle that searches for those states that verify certain conditions. In this
case, what it looks for are those bit sequences that encode P different numbers,
resulting in all possible permutations of them. 

Note: The number P must be a power of 2. Moreover, since for P = 8 the required 
number of qubits is too large, the simulation cannot be carried out. However, 
the program builds the circuit without problems. I recommend use P = 4

