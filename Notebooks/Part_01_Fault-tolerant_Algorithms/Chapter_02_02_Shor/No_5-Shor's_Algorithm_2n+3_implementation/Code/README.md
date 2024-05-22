For the development of this code the github repository [ShorAlgQiskit](https://github.com/ttlion/ShorAlgQiskit)
has been used as a reference. The code has been rewritten practically from scratch but taking ideas from the
mentioned repository when implementing the functions that apply the doors.



In this folder you can find two implementation of the Shor's Algoritm.

    Qiskit_Shor_2n_plus_3.py
    Qiskit_Shor_4n_plus_2.py

The first one use 2n+3 qubits and the second one use 4n+2 qubits (where n
is the number of bit we need to encode the number N we want to factorize).

The rest of the scripts contain functions that are called by these two. For this
reason, you must download all the files in this folder to be able to execute the
two scripts mentioned above.

You can also find an example to see what the degree of approximation do in the
in the QFT in the file

    Example_QFT_Approx/Example_QFT_approx.py


# Requirement

The only requirement is to have [Qiskit](https://qiskit.org/documentation/getting_started.html) 
and [Qiskit_aer](https://pypi.org/project/qiskit-aer/). If you want to use the
GPU option you must install the version of Qiskit with GPU support.

# How to execute 

Both scripts follow the same logic for execution: if you execute
them from an integrated development environment (such as Spyder or VisualStudio
Code) or if you execute then in terminal with
    
    python Qiskit_Shor_2n_plus_3.py
    python Qiskit_Shor_4n_plus_2.py

you will be prompted to enter via the terminal the parameters. On the other hand, 
these scripts can be executed in terminal by passing the parameters in the call 
itself. For example

    python Qiskit_Shor_2n_plus_3.py -N 21 -shots_per_a 10
    python Qiskit_Shor_4n_plus_2.py -N 15 -a 7 -shots_execution 5
   
The only parameter required is -N. The rest can be omitted and will be assigned
default values.

    python Qiskit_Shor_2n_plus_3.py -N 21
    python Qiskit_Shor_4n_plus_2.py -N 15

This second option to execute the scripts is intended to send them to be executed in 
the queue system of a supercomputer without having to open an interactive session.
    
The avaliable parameter are:

    -N      -> number_to_factorize
    -a      -> value_of_a (optinal. Default: a = random)
    -shots  -> shots_per_execution (optional. Default: shots = 3)
    -ashots -> number of global executions with the same a value (max_shots parameter)
    -approx -> approx_QFT (optional. Default approx_QFT = 0)
    -g      -> GPU support (optional. Default = 0 -> False)
    -cuQ    -> cuQuantum support (optional. Default = 0 -> False)

