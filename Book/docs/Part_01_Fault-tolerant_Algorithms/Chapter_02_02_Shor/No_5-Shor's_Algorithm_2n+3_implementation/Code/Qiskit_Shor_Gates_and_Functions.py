""" Imports from qiskit"""
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit import execute, IBMQ, transpile

from qiskit.circuit.library import QFT


import sys

""" Imports to Python functions """
import math
import array
import fractions
import numpy as np

import random as rd

# ==============================================================================
# Gates
# ==============================================================================

"""Creation of the circuit that performs addition by a in Fourier Space"""
"""Can also be used for subtraction by setting the parameter f_inv = True """
def phiADD(f_circuit,f_target_reg,f_a,f_n,f_inv):
    '''
    phiADD(f_circuit,f_target_reg,f_a,f_n,f_inv)

    This gate is the adder gate (Drapper adder gate). This gate implements the 
    summation of a classical value to a Quantum value encode in a Quantum 
    Registes as its Quantum Fourier Transform.

    References: 
        - Beauregard, S. (2002). Circuit for Shor's algorithm using 2n+ 3 
          qubits. arXiv preprint https://arxiv.org/abs/quant-ph/0205095.

    In our case, this gate is applied on the first n qubits of the ancilla register

    Input:
        - f_circuit: It is the Quantum Circuit in which we are going to insert 
            the "cphiADD" gate. 
            In our case, this circuit have 3 Quantum Registers (we call they 
            down_reg, count_reg and ancilla_reg) and one Classical Register 
            (we call it count_classic), thus is: 
            QuantumCircuit(down_reg , count_reg , ancilla_reg, count_classic)

        - f_target_reg: It is the Quantum Register where we are going to apply 
            the gate "cphiADD". 
            In our case, it is the Quantum Register "ancilla_reg" mentioned in 
            the previous point (f_circuit). 

        - f_ctl: It one of the two control qubits of the this gate.
            In our case, it is the ancilla of the "ccphiADDmodN" gate.

        - f_a: It is the classical value "a" that we are going to use in
                "cphiADD(a) |phi(b)> = | phi((a + b))>"
            In our case, this value is f_a = (a^s * 2^i) mod N

        - f_n: The minimum number of bit (qubits) that we need to encode N in 
            binary.

        - f_inv: Boolean value. If it is False, we apply the double controlled 
            adder gate and if it is True, we apply the inverse of this gate.

    
    
    Developer's Note: I usually use "f_" at the begining of all the local 
    variables in my functions. In this way, I avoid unintentionally modifying 
    a global variable.
    '''
    assert type(f_inv) == bool
    f_angle = ((-1)**f_inv) * getAngles(f_a,f_n)
    for i in range(0,f_n):
        f_circuit.p(f_angle[i],f_target_reg[i])
        '''
        if inv==0:
            circuit.p(angle[i],q[i])
        else:
            circuit.p(-angle[i],q[i])
        '''
"""Single controlled version of the phiADD circuit"""
def cphiADD(f_circuit,f_target_reg,f_ctl,f_a,f_n,f_inv):
    '''
    cphiADD(f_circuit,f_target_reg,f_ctl,f_a,f_n,f_inv)

    This gate is the controled adder gate (Drapper adder gate). This gate
    implements the summation of a classical value to a Quantum value encode in a 
    Quantum Registes as its Quantum Fourier Transform.

    References: 
        - Beauregard, S. (2002). Circuit for Shor's algorithm using 2n+ 3 
          qubits. arXiv preprint https://arxiv.org/abs/quant-ph/0205095.

    In our case, this gate is applied on the first n qubits of the ancilla 
    register and its control qubit is the ancilla of the "ccphiADDmodN" gate 
    (the (n+1)-th qubit of the ancilla register).


    Input:
        - f_circuit: It is the Quantum Circuit in which we are going to insert 
            the "cphiADD" gate. 
            In our case, this circuit have 3 Quantum Registers (we call they 
            down_reg, count_reg and ancilla_reg) and one Classical Register 
            (we call it count_classic), thus is: 
            QuantumCircuit(down_reg , count_reg , ancilla_reg, count_classic)

        - f_target_reg: It is the Quantum Register where we are going to apply 
            the gate "cphiADD". 
            In our case, it is the Quantum Register "ancilla_reg" mentioned in 
            the previous point (f_circuit). 

        - f_ctl: It one of the two control qubits of the this gate.
            In our case, it is the ancilla of the "ccphiADDmodN" gate.

        - f_a: It is the classical value "a" that we are going to use in
                "cphiADD(a) |phi(b)> = | phi((a + b))>"
            In our case, this value is f_a = (a^s * 2^i) mod N

        - f_n: The minimum number of bit (qubits) that we need to encode N in 
            binary.

        - f_inv: Boolean value. If it is False, we apply the double controlled 
            adder gate and if it is True, we apply the inverse of this gate.

    Developer's Note: I usually use "f_" at the begining of all the local 
    variables in my functions. In this way, I avoid unintentionally modifying 
    a global variable.
    '''
    assert type(f_inv) == bool
    f_angle = ((-1)**f_inv) * getAngles(f_a,f_n)
    for i in range(0,f_n):
        f_circuit.cp(f_angle[i],f_ctl,f_target_reg[i])
        '''
        if f_inv==0:
            f_circuit.cp(f_angle[i],f_ctl,f_target_reg[i])
        else:
            f_circuit.cp(-f_angle[i],f_ctl,f_target_reg[i])
        '''

"""Doubly controlled version of the phiADD circuit"""      
def ccphiADD(f_circuit,f_target_reg,f_ctl1,f_ctl2,f_a,f_n,f_inv):
    '''
    ccphiADD(f_circuit,f_target_reg,f_ctl1,f_ctl2,f_a,f_n,f_inv)

    This gate is the double controled adder gate (Drapper adder gate). This gate
    implements the summation of a classical value to a Quantum value encode in a 
    Quantum Registes as its Quantum Fourier Transform.

    References: 
        - Beauregard, S. (2002). Circuit for Shor's algorithm using 2n+ 3 
          qubits. arXiv preprint https://arxiv.org/abs/quant-ph/0205095. 

    Double control means that it has two control qubits (f_ctl1 y f_ctl2) and 
    for this gate to act, both must be in the state |1>. This gate also needs an
    ancilla qubit. 
    
    In our case, this gate is applied on the first n qubits of the ancilla 
    register and its control qubits are the control qubits of the gate 
    "ccphiADDmodN" gate.


    Input:
        - f_circuit: It is the Quantum Circuit in which we are going to insert 
            the "ccphiADD" gate. 
            In our case, this circuit have 3 Quantum Registers (we call they 
            down_reg, count_reg and ancilla_reg) and one Classical Register 
            (we call it count_classic), thus is: 
            QuantumCircuit(down_reg , count_reg , ancilla_reg, count_classic)

        - f_target_reg: It is the Quantum Register where we are going to apply 
            the gate "ccphiADD". 
            In our case, it is the Quantum Register "ancilla_reg" mentioned in 
            the previous point (f_circuit). 

        - f_ctl1: It one of the two control qubits of the this gate. 
            In our case, this control qubit is the same control qubit as that of 
            the "ccphiADDmodN" gate. 

        - f_ctl2: It one of the two control qubits of the this gate. 
            In our case, this control qubit is the same control qubit as that of 
            the "ccphiADDmodN".

        - f_a: It is the classical value "a" that we are going to use in
                "ccphiADD(a) |phi(b)> = | phi((a + b))>"
            In our case, this value is f_a = (a^s * 2^i) mod N

        - f_n: The minimum number of bit (qubits) that we need to encode N in 
            binary.

        - f_inv: Boolean value. If it is False, we apply the double controlled 
            adder gate and if it is True, we apply the inverse of this gate.

    Developer's Note: I usually use "f_" at the begining of all the local 
    variables in my functions. In this way, I avoid unintentionally modifying 
    a global variable.
    '''
    assert type(f_inv) == bool
    f_angles = ((-1)**(f_inv)) * getAngles(f_a,f_n)

    for i in range(0,f_n):
        #ccphase(f_circuit,f_angle[i],f_ctl1,f_ctl2,f_target_reg[i])

        f_circuit.cp(f_angles[i]/2,f_ctl2,f_target_reg[i])
        f_circuit.cx(f_ctl1,f_ctl2)
        f_circuit.cp(-f_angles[i]/2,f_ctl2,f_target_reg[i])
        f_circuit.cx(f_ctl1,f_ctl2)
        f_circuit.cp(f_angles[i]/2,f_ctl1,f_target_reg[i])

        '''
        if inv==0:
            ccphase(f_circuit,f_angle[i],ctl1,ctl2,q[i])
        else:
            ccphase(f_circuit,-angle[i],ctl1,ctl2,q[i])
        '''
"""Circuit that implements doubly controlled modular addition by a"""
def ccphiADDmodN(f_circuit, f_target_reg, f_ctl1, f_ctl2, f_ancilla_qbit, 
    f_a, f_N, f_n, f_approx_QFT = 0):
    '''
    ccphiADDmodN(f_circuit, f_target_reg, f_ctl1, f_ctl2, f_ancilla_qbit, 
    f_a, f_N, f_n)

    This gate is the double controlled modulated adder gate. 

    This gate is the double control modular adder gate. This gate implements the
    modulo-N summation of a classical Value to a Quantum Value encoded in a 
    Quantum Register as its Quantum Fourier Transform. 

    References: 
        - Beauregard, S. (2002). Circuit for Shor's algorithm using 2n+ 3 
          qubits. arXiv preprint https://arxiv.org/abs/quant-ph/0205095. 

    Double control means that it has two control qubits (f_ctl1 y f_ctl2) and 
    for this gate to act, both must be in the state |1>. This gate also needs an
    ancilla qubit. 
    In our case, this gate is applied on the first n qubits of the ancilla 
    register and its control qubits are the control qubit of the gate 
    "cU_a_pow_s" and one of the qubits of the "target_reg· of the gate "cU_a_pow".


    Input:
        - f_circuit: It is the Quantum Circuit in which we are going to insert 
            the "ccphiADDmodN" gate. 
            In our case, this circuit have 3 Quantum Registers (we call they 
            down_reg, count_reg and ancilla_reg) and one Classical Register 
            (we call it count_classic), thus is: 
            QuantumCircuit(down_reg , count_reg , ancilla_reg, count_classic)

        - f_target_reg: It is the Quantum Register where we are going to apply 
            the gate "ccphiADDmodN". 
            In our case, it is the Quantum Register "ancilla_reg" mentioned in 
            the previous point (f_circuit). 

        - f_ctl1: It one of the two control qubits of the this gate. 
            In our case, this control qubit is the same control qubit as that of 
            the "cU_a_pow_s" gate. 

        - f_ctl2: It one of the two control qubits of the this gate. 
            In our case, this control qubit is one of the target qubits of the 
            previous gate, "cU_a_pow_s" (this is, one qubit from the "down_reg") 

        - f_ancilla_qbit = This qubit is an ancilla, i.e., a qubita that we are 
            going to use in intermediate calculations. This qubit have to start 
            from state |0> and at the end of the and at the end of the
            calculations we have to return them to the starting state. 
            In our case, it is one qubit from the ancilla_reg.

        - f_a: It is the classical value "a" that we are going to use in the gate 
                "ccphiADD(a)modN |phi(b)> = | phi((a + b) mod N)>. 
            In our case, f_a = (a^s * 2^i) mod N

        - f_N: The number that we want to factorize.

        - f_n: The minimum number of bit (qubits) that we need to encode N in 
            binary.

        - f_approx_QFT: Degree of aproximation in the QFTs. 
            If it is 0, there is no aproximation. 
            If it is 1, we obviate the lower angle gates (\pi/2^n) in the QFT, 
            where n is the number of qubits in which the QFT is applied. 
            If it is 2, we also skip the next lowest angle gates (\pi/2^{n-1}). 
            So, successively (3, 4, ...). 
            By default, it is 0, i.e., we use all the gates.

    Developer's Note: I usually use "f_" at the begining of all the local 
    variables in my functions. In this way, I avoid unintentionally modifying 
    a global variable.
    '''

    ccphiADD(f_circuit, f_target_reg, f_ctl1, f_ctl2, f_a, f_n, False)
    phiADD(f_circuit, f_target_reg, f_N, f_n, True)
    #create_inverse_QFT(f_circuit, f_target_reg, f_n, False)
    #f_circuit.compose(QFT(f_n, inverse=True, do_swaps=False), f_target_reg[:f_n])
    f_circuit.append(QFT(f_n, inverse=True, do_swaps=False, 
                          approximation_degree=f_approx_QFT).to_gate(), f_target_reg[:f_n])


    f_circuit.cx(f_target_reg[f_n-1], f_ancilla_qbit)
    #create_QFT(f_circuit, f_target_reg, f_n,False)
    #f_circuit.compose(QFT(f_n, inverse=False, do_swaps=False), f_target_reg[:f_n])
    f_circuit.append(QFT(f_n, inverse=False, do_swaps=False, 
                          approximation_degree=f_approx_QFT).to_gate(), f_target_reg[:f_n])
    cphiADD(f_circuit, f_target_reg, f_ancilla_qbit, f_N, f_n, False)
    
    ccphiADD(f_circuit, f_target_reg, f_ctl1, f_ctl2, f_a, f_n, True)
    #create_inverse_QFT(f_circuit, f_target_reg, f_n, False)
    #f_circuit.compose(QFT(f_n, inverse=True, do_swaps=False), f_target_reg[:f_n])
    f_circuit.append(QFT(f_n, inverse=True, do_swaps=False, 
                          approximation_degree=f_approx_QFT).to_gate(), f_target_reg[:f_n])
    f_circuit.x(f_target_reg[f_n-1])
    f_circuit.cx(f_target_reg[f_n-1], f_ancilla_qbit)
    f_circuit.x(f_target_reg[f_n-1])
    #create_QFT(f_circuit, f_target_reg, f_n, False)
    #f_circuit.compose(QFT(f_n, inverse=False, do_swaps=False), f_target_reg[:f_n])
    f_circuit.append(QFT(f_n, inverse=False, do_swaps=False, 
                          approximation_degree=f_approx_QFT).to_gate(), f_target_reg[:f_n])
    ccphiADD(f_circuit, f_target_reg, f_ctl1, f_ctl2, f_a, f_n, False)

"""Circuit that implements the inverse of doubly controlled modular addition by a"""
def ccphiADDmodN_inv(f_circuit, f_target_reg, f_ctl1, f_ctl2, f_ancilla_qbit, 
    f_a_inv, f_N, f_n, f_approx_QFT = 0):
    '''
    ccphiADDmodN_inv(f_circuit, f_target_reg, f_ctl1, f_ctl2, f_ancilla_qbit, 
    f_a_inv, f_N, f_n)

    This gate is inverse of the double controlled modulated adder door, i.e., 
    the invers of the "ccphiADDmodN" gate. 

    References: 
        - Beauregard, S. (2002). Circuit for Shor's algorithm using 2n+ 3 
          qubits. arXiv preprint https://arxiv.org/abs/quant-ph/0205095. 

    Double controled means that it has two control qubits (f_ctl1 y f_ctl2) and 
    for this gate to act, both must be in the state |1>. This gate also needs an
    ancilla qubit. 
    In our case, this gate is applied on the first n qubits of the ancilla 
    register and its control qubits are the control qubit of the gate 
    "cU_a_pow_s" and one of the qubits of the "target_reg· of the gate "cU_a_pow"

    Input:
        - f_circuit: It is the Quantum Circuit in which we are going to insert 
            the "ccphiADDmodN" gate. 
            In our case, this circuit have 3 Quantum Registers (we call they 
            down_reg, count_reg and ancilla_reg) and one Classical Register 
            (we call it count_classic), thus is: 
            QuantumCircuit(down_reg , count_reg , ancilla_reg, count_classic)

        - f_target_reg: It is the Quantum Register where we are going to apply 
            the gate "ccphiADDmodN". 
            In our case, it is the Quantum Register "ancilla_reg" mentioned in 
            the previous point (f_circuit). 

        - f_ctl1: It one of the two control qubits of the this gate. 
            In our case, this control qubit is the same control qubit as that of 
            the "cU_a_pow_s" gate. 

        - f_ctl2: It one of the two control qubits of the this gate. 
            In our case, this control qubit is one of the target qubits of the 
            previous gate, "cU_a_pow_s" (this is, one qubit from the "down_reg") 

        - f_ancilla_qbit = This qubit is an ancilla, i.e., a qubita that we are 
            going to use in intermediate calculations. This qubit have to start 
            from state |0> and at the end of the and at the end of the
            calculations we have to return them to the starting state. 
            In our case, it is one qubit from the ancilla_reg.

        - f_a_inv: It is the classical value "a^(-1)" that we are going to use in the gate 
                "ccphiADD(a^(-1))modN^(-1) |phi(b)> = |phi (b-a) mod N> if b>p"
                "ccphiADD(a^(-1))modN^(-1) |phi(b)> = |phi [2^(n+1)-(a-b)] mod N> if b>p"
            In our case, f_a is the modular inverse of (a^s * 2^i) mod N 

        - f_N: The number that we want to factorize.

        - f_n: The minimum number of bit (qubits) that we need to encode N in 
            binary.

        - f_approx_QFT: Degree of aproximation in the QFTs. 
            If it is 0, there is no aproximation. 
            If it is 1, we obviate the lower angle gates (\pi/2^n) in the QFT, 
            where n is the number of qubits in which the QFT is applied. 
            If it is 2, we also skip the next lowest angle gates (\pi/2^{n-1}). 
            So, successively (3, 4, ...). 
            By default, it is 0, i.e., we use all the gates.

    Developer's Note: I usually use "f_" at the begining of all the local 
    variables in my functions. In this way, I avoid unintentionally modifying 
    a global variable.
    '''

    ccphiADD(f_circuit, f_target_reg, f_ctl1, f_ctl2, f_a_inv, f_n, True)
    #create_inverse_QFT(f_circuit, f_target_reg, f_n, False)
    #f_circuit.compose(QFT(f_n, inverse=True, do_swaps=False), f_target_reg[:f_n])
    f_circuit.append(QFT(f_n, inverse=True, do_swaps=False, 
                          approximation_degree=f_approx_QFT).to_gate(), f_target_reg[:f_n])
    f_circuit.x(f_target_reg[f_n-1])
    f_circuit.cx(f_target_reg[f_n-1], f_ancilla_qbit)
    f_circuit.x(f_target_reg[f_n-1])
    #create_QFT(f_circuit, f_target_reg, f_n, False)
    #f_circuit.compose(QFT(f_n, inverse=False, do_swaps=False), f_target_reg[:f_n])
    f_circuit.append(QFT(f_n, inverse=False, do_swaps=False, 
                          approximation_degree=f_approx_QFT).to_gate(), f_target_reg[:f_n])
    ccphiADD(f_circuit, f_target_reg, f_ctl1, f_ctl2, f_a_inv, f_n, False)

    cphiADD(f_circuit, f_target_reg, f_ancilla_qbit, f_N, f_n, True)
    #create_inverse_QFT(f_circuit, f_target_reg, f_n, False)
    #f_circuit.compose(QFT(f_n, inverse=True, do_swaps=False), f_target_reg[:f_n])
    f_circuit.append(QFT(f_n, inverse=True, do_swaps=False, 
                          approximation_degree=f_approx_QFT).to_gate(), f_target_reg[:f_n])
    f_circuit.cx(f_target_reg[f_n-1], f_ancilla_qbit)

    #create_QFT(f_circuit, f_target_reg, f_n, False)
    #circuit.compose(QFT(f_n, inverse=False, do_swaps=False), f_target_reg[:f_n])
    f_circuit.append(QFT(f_n, inverse=False, do_swaps=False, 
                          approximation_degree=f_approx_QFT).to_gate(), f_target_reg[:f_n])
    phiADD(f_circuit, f_target_reg, f_N, f_n, False)
    ccphiADD(f_circuit, f_target_reg, f_ctl1, f_ctl2, f_a_inv, f_n, True)

"""Circuit that implements single controlled modular multiplication by a"""
def cU_a_pow_s(f_circuit, f_target_reg, f_ctl, f_ancilla_reg, 
               f_a, f_s, f_N, f_n, f_approx_QFT = 0):
    '''
    cU_a_pow_s(f_circuit, f_target_reg, f_ctl, f_ancilla_reg, f_a, f_s, f_N, f_n)

    This is the gate that apply the controled modular exponential cU_{a^s}. 
    This gate first apply the cMULT(a)mod(N) gate, next the Swap gate and finaly
    the cMULT(a^{-1})mod(N)^{-1} gate.

    References: 
        - Beauregard, S. (2002). Circuit for Shor's algorithm using 2n+ 3 
          qubits. arXiv preprint https://arxiv.org/abs/quant-ph/0205095. 

    Input:
        - f_circuit: It is the Quantum Circuit in which we are going to insert 
            the "cU_a_pow_s" door. 
            In our case, this circuit have 3 Quantum Registers (we call they 
            down_reg, count_reg and ancilla_reg) and one Classical Register 
            (we call it count_classic), thus is: 
            QuantumCircuit(down_reg , count_reg , ancilla_reg, count_classic)

        - f_target_reg: It is the Quantum Register, from the previous circuit, 
            where we are going to apply the gate "cU_a_pow_s". 
            In our case, it is the Quantum Register "down_reg". 

        - f_ctl: It is the control qubit of the "cU_a_pow_s" gate. 
            In our case, this qubit is the k-th qubit (starting to count from 0) 
            from the count register ("count_reg[k]").

        - f_ancilla_reg: The qubits from this Quantum Register are ancillas, 
            that is, qubits that we are going to use in intermediate calculations.
            These qubits have to start from state |0> and at the end of the and 
            at the end of the calculations we have to return them to the starting 
            state. 
            In our case, they are the ancilla_reg.

        - f_a: It is the classical value "a" that we are going to 
            use in the controled modular exponential operator 
                "cU_{a^s} |ctl>|x> = |ctl>|x a^s mod N>" (if ctl = 1). 

        - f_s: It is the exponent "s" of "a" in 
                "cU_{a^s} |ctl>|x> = |ctl>|x a^s mod N>" (if ctl = 1). 
            In our case, we have "s = 2^k" where "k" the index of the 
            control qubit (starting to count from 0). 

        - f_N: The number that we want to factorize.

        - f_n: The minimum number of bit (qubits) that we need to encode N in 
            binary.

        - f_approx_QFT: Degree of aproximation in the QFTs. 
            If it is 0, there is no aproximation. 
            If it is 1, we obviate the lower angle gates (\pi/2^n) in the QFT, 
            where n is the number of qubits in which the QFT is applied. 
            If it is 2, we also skip the next lowest angle gates (\pi/2^{n-1}). 
            So, successively (3, 4, ...). 
            By default, it is 0, i.e., we use all the gates.

    Developer's Note: I usually use "f_" at the begining of all the local 
    variables in my functions. In this way, I avoid unintentionally modifying 
    a global variable.
    '''
    f_a_pow_s = int(pow(f_a,f_s))
    # =======================================
    # cMULT(a)mod(N) gate

    #create_QFT(f_circuit,f_ancilla_reg,f_n+1,0)
    #f_circuit.compose(QFT(f_n+1, inverse=False, do_swaps=False), f_ancilla_reg[:f_n+1])
    f_circuit.append(QFT(f_n+1, inverse=False, do_swaps=False, 
                          approximation_degree=f_approx_QFT).to_gate(), f_ancilla_reg[:f_n+1])

    for i in range(0, f_n):
        f_as_2i = pow(2,i)*f_a_pow_s % f_N # (a^s * 2^i) mod N
        ccphiADDmodN(f_circuit, f_ancilla_reg, f_ctl, f_target_reg[i], f_ancilla_reg[f_n+1], 
                     f_as_2i ,f_N, f_n+1, f_approx_QFT) 
    
    #create_inverse_QFT(f_circuit, f_ancilla_reg, f_n+1, 0)
    #f_circuit.compose(QFT(f_n+1, inverse=True, do_swaps=False), f_ancilla_reg[:f_n+1])
    f_circuit.append(QFT(f_n+1, inverse=True, do_swaps=False, 
                          approximation_degree=f_approx_QFT).to_gate(), f_ancilla_reg[:f_n+1])

    # =======================================
    # C-SWAP gate
    for i in range(0, f_n):
        f_circuit.cswap(f_ctl,f_target_reg[i],f_ancilla_reg[i])


    # =======================================
    # cMULT(a^{-1})mod(N)^{-1} gate

    #f_classic_val_inv = modinv(f_a, f_N)
    f_a_pow_s_inv = pow(f_a_pow_s, -1, f_N) # This way to compute the modular 
                            # multiplicative inverse only works in python 3.8+

    #create_QFT(f_circuit, f_ancilla_reg, f_n+1, 0)
    #f_circuit.compose(QFT(f_n+1, inverse=False, do_swaps=False), f_ancilla_reg[:f_n+1])
    f_circuit.append(QFT(f_n+1, inverse=False, do_swaps=False, 
                          approximation_degree=f_approx_QFT).to_gate(), f_ancilla_reg[:f_n+1])
    
    i = f_n-1
    while i >= 0:
        f_as_inv_2i = pow(2,i)*f_a_pow_s_inv % f_N
        ccphiADDmodN_inv(f_circuit, f_ancilla_reg, f_ctl, f_target_reg[i],  f_ancilla_reg[f_n+1], 
                          f_as_inv_2i, f_N, f_n+1, f_approx_QFT) # pow(2,i)*f_classic_val_inv % f_N,
        i -= 1
    #create_inverse_QFT(f_circuit, f_ancilla_reg, f_n+1, 0)
    #f_circuit.compose(QFT(f_n+1, inverse=True, do_swaps=False), f_ancilla_reg[:f_n+1])
    f_circuit.append(QFT(f_n+1, inverse=True, do_swaps=False, 
                          approximation_degree=f_approx_QFT).to_gate(), f_ancilla_reg[:f_n+1])


# ==============================================================================
# Functions
# ==============================================================================

def is_prime(n):
    for i in range(2,int(math.sqrt(n))+1):
        if (n%i) == 0:
            return False
    return True

""" Function to check if N is of type q^p"""
def check_if_power(N):  # Nota_David: Ver si hay mejores funciones https://stackoverflow.com/questions/39190815/how-to-make-perfect-power-algorithm-more-efficient
    """ Check if N is a perfect power in O(n^3) time, n=ceil(logN) """
    b=2
    while (2**b) <= N:
        a = 1
        c = N
        while (c-a) >= 2:
            m = int( (a+c)/2 )

            if (m**b) < (N+1):
                p = int( (m**b) )
            else:
                p = int(N+1)

            if int(p) == int(N):
                print('N is {0}^{1}'.format(int(m),int(b)), flush = True)
                return True

            if p<N:
                a = int(m)
            else:
                c = int(m)
        b=b+1

    return False


def test_simple_cases(N): 
    # Check if N==1 or N==0
    if N==1 or N==0: 
        print('Please put an N different from 0 and from 1', flush = True)
        exit(1)

    # Check if N is even
    if (N%2)==0:
        print('N is even, so does not make sense!', flush = True)
        exit(1)

    # Check if N is a perfect power in O(n^3) time
    if check_if_power(N)==True:
        print('N is a perfect power')
        exit(1)


def get_value_a(N):
    '''
    get_value_a(N)

    This function takes the value to be factored (N) and return a random value 
    1 > a > N and coprime with N. This value a is going to be the number that we 
    are going to use in our modular exponential f(x) = a^x mod N. 

    Inputs:
        - N: number to be factored
    Outputs:
        - a: number that we are going to use in the modular exponential f(x) = a^x mod N
    '''
 
    a = int((N-2)*rd.random())+2 #With this we are sure that a \in [2,N-1]
    assert a < N
    while math.gcd(a,N)!=1:
        a = int((N-2)*rd.random())+2
    print('The random value of a is a = ', a, flush = True)
    return a

    '''
    Nota_David: Puede hacerse una función que dea varios (o todos) los números coprimos de N.
    '''

def test_a(a_to_test,N):
    '''
    test_a(a_to_test,N)

    This function takes the values a_to_test and N and return a ValueError if 
    they are not coprimes.

    Inputs:
        a_to_test 
        N
    '''

    '''
    while math.gcd(a_to_test ,N)!=1:
        a_to_test = int(input('The given value of a is not coprime with N. Type a new one: '))
    '''
    if math.gcd(a_to_test ,N)!=1:
        raise ValueError ('The given value of a is not coprime with N.')


def find_factors(phase, N, a, n):
    '''
    find_factors(phase, N, a, n)

    This function takes the phase that we estimate with the QPE (Quantum Phase 
    Estimation) algorithm and compute the period r. With this value of r,
    we try to compute the factors of N (try_factor_plus, try_factor_minus). 

    Inputs:
        - phase: The value that we estimate with the QPE (Quantum Phase Estimation) 
        algorithm (with the factor 2^{2n}, that is, we have to divide by 2^{2n}). This 
        value takes the form [2^{2n} s/r].

        - N: The number that we want to factorize. 

        - a: Number that we are going to use in the modular exponential f(x) = a^x mod N.

        - n: The minimum number of bit (qubits) that we need to encode N in binary.
    
    Outputs: 
        Our output is a list, but we have three options:
            - []: If we haven't found any non-trivial factor, our output is an 
            empty list.

            - [factor]: If we found only one factor, our output is a list with 
            one element (our factor).

            - [factor, factor]: If we found the two factors, our output is a 
            list with two elements (our two factors).

    '''
    if phase == 0:
        return []

    frac = fractions.Fraction(phase/2**(2*n)).limit_denominator(N)

    r = frac.denominator
    print('Estimated value of r', r, flush = True)

    if (r%2) == 1:
        return []

    exponential = pow(a , int(r/2))

    # Guesses for factors are gcd(x^{r/2} ±1 , 15)
    #guesses = [math.gcd(a**(r//2)-1, N), math.gcd(a**(r//2)+1, N)]
    guesses = [math.gcd(exponential-1, N), math.gcd(exponential+1, N)]
    guesses_is_prime = [is_prime(guesses[0]), is_prime(guesses[1])]

    new_factors = []
    for i in range(2):
        if guesses[i] not in [1,N] and (N % guesses[i]) == 0 and guesses_is_prime[i]: # Check to see if guess is a factor
            print("*** Non-trivial factor found: %i ***" % guesses[i], flush = True)
            new_factors.append(guesses[i])

    return new_factors 

''' 
Nota_David: tenemos la QFT de qiskit (qiskit.circuit.library.QFT()) que tambien 
admite una versión aproximada usando el parámetro "approximation_degree". 
Ver https://qiskit.org/documentation/stubs/qiskit.circuit.library.QFT.html?highlight=qft#qiskit.circuit.library.QFT

CLASS QFT(num_qubits=None, approximation_degree=0, do_swaps=True, inverse=False, insert_barriers=False, name=None)
'''


""" Function to create QFT """
def create_QFT(circuit,up_reg,n,with_swaps):
    '''
    Nota_David: en principio, se sustituye por "qiskit.circuit.library.QFT()"
    '''
    
    i=n-1
    """ Apply the H gates and Cphases"""
    """ The Cphases with |angle| < threshold are not created because they do 
    nothing. The threshold is put as being 0 so all CPhases are created,
    but the clause is there so if wanted just need to change the 0 of the
    if-clause to the desired value """
    while i>=0:
        circuit.h(up_reg[i])        
        j=i-1  
        while j>=0:
            if (np.pi)/(pow(2,(i-j))) > 0:
                circuit.cp( (np.pi)/(pow(2,(i-j))) , up_reg[i] , up_reg[j] )
                j=j-1   
        i=i-1 

    """ If specified, apply the Swaps at the end """
    if with_swaps==1:
        i=0
        while i < ((n-1)/2):
            circuit.swap(up_reg[i], up_reg[n-1-i])
            i=i+1

""" Function to create inverse QFT """
def create_inverse_QFT(circuit,up_reg,n,with_swaps):
    '''
    Nota_David: en principio, se sustituye por "qiskit.circuit.library.QFT(inverse = True)"
    '''
    
    """ If specified, apply the Swaps at the beggining"""
    if with_swaps==1:
        i=0
        while i < ((n-1)/2):
            circuit.swap(up_reg[i], up_reg[n-1-i])
            i=i+1
    
    """ Apply the H gates and Cphases"""
    """ The Cphases with |angle| < threshold are not created because they do 
    nothing. The threshold is put as being 0 so all CPhases are created,
    but the clause is there so if wanted just need to change the 0 of the
    if-clause to the desired value """
    i=0
    while i<n:
        circuit.h(up_reg[i])
        if i != n-1:
            j=i+1
            y=i
            while y>=0:
                 if (np.pi)/(pow(2,(j-y))) > 0:
                    circuit.cp( - (np.pi)/(pow(2,(j-y))) , up_reg[j] , up_reg[y] )
                    y=y-1   
        i=i+1

"""Function that calculates the array of angles to be used in the addition in Fourier Space"""
def getAngles(f_a,f_n):
    '''
    getAngles(f_a,f_n)

    This function takes the classical value "a" and return the angles that we 
    need to apply the adder gate of Drapper.

    Inputs:

        - f_a: It is the clasical value that we want to sum using the adder gate

        - f_n: The minimum number of bit (qubits) that we need to encode N in 
            binary.

    Outputs:
        - f_angles: The angles that we need in the adder gate

    Developer's Note: I usually use "f_" at the begining of all the local 
    variables in my functions. In this way, I avoid unintentionally modifying 
    a global variable.
    '''
    f_s=bin(int(f_a))[2:].zfill(f_n) 
    f_angles=np.zeros([f_n])
    for i in range(0, f_n):
        for j in range(i,f_n):
            if f_s[j]=='1':
                f_angles[f_n-i-1]+=math.pow(2, -(j-i))
        f_angles[f_n-i-1]*=np.pi
    return f_angles