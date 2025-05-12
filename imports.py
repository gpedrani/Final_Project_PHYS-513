# Imports 
from qiskit import QuantumCircuit
from qiskit.circuit.random import random_circuit
import matplotlib.pyplot as plt
import numpy as np 
from qiskit import transpile
from qiskit_aer import AerSimulator 
from qiskit.quantum_info import DensityMatrix, Statevector
from qiskit.quantum_info.states import partial_trace
import pandas as pd 
import scipy.linalg as la

def rand_real_circ(L, p, timesteps, flag=0):

    if flag == 1:
        qc = QuantumCircuit(L,L)
    
    #Randomly Select L*p qubits 
    meas = int(np.floor(L*p))
    
    for j in range(0, timesteps):

        s = np.random.choice([0,1,2], 1)
        qubits = [i for  i in range(0,L)]
        
        if s == 0:
            #Single Qubit Gates
            for i in range(0,L):
                v = np.random.randint(0,10, size=1)
                if v <= 5:
                    qc.h(i)
                elif v > 5:
                    qc.s(i)
            #Perform Random Measurement
            a = np.random.choice(qubits, size=meas)
            for i in a:
                qc.measure(i, i)
                
        elif s == 1:
            #Control-Target Gates: 
            for i in range(0, L):
                if i == L-1:
                    break
                else:
                    qc.cx(i,i+1)
                    
                #Perform Random Measurement
                a = np.random.choice(qubits, size=meas)
                for i in a:
                    qc.measure(i, i)

            
        elif s == 2:
            #Target-Control Gates: 
            for i in range(0, L):
                if i == L-1:
                    break
                else:
                    qc.cx(i+1,i)   

                #Perform Random Measurement
                a = np.random.choice(qubits, size=meas)
                for i in a:
                    qc.measure(i, i)
        
    return qc

def rand_sim_circ(L, timesteps, flag = 0):

    if flag == 1:
        qc = QuantumCircuit(L)

    for j in range(0, timesteps):
        
        s = np.random.choice([0,1,2], 1)
        
        if s == 0:
            #Single Qubit Gates
            for i in range(0,L):
                v = np.random.choice([0,1], 1)
                if v == 0:
                    qc.h(i)
                elif v == 1:
                    qc.s(i)
                    
        elif s == 1:
            #Control-Target Gates: 
            for i in range(0, L):
                if i == L-1:
                    break
            else:
                qc.cx(i,i+1)
                
        elif s == 2:
            #Target-Control Gates: 
            for i in range(0, L):
                if i == L-1:
                    break
                else:
                    qc.cx(i+1,i)
        
    return qc


def diagonalize(rho):
    u, D = la.eig(rho)
    return D 

def renyi(diags, n):
    assert n != None, "Please supply a value for n."
    assert n > 0, "Renyi Entropy is only analytical for n > 0."    
    
    if n != 1: 
        a = 1/(1-n) 
        b = np.trace(diags)**n
        return a * np.log2(b)
    elif n == 1:  
        return -np.sum(diags * np.log2(diags))

def find_subspaces(L):
    subspaces = []
    for i in range(0, L):
        for j in range(i,L): 
            a = list(range(i , j+1))
            subspaces.append(a)  
    subspaces.sort(key=len)
    subspaces = subspaces[0:-1]
    return subspaces

def rand_real_circ2(L, p, timesteps):
    
    qc = QuantumCircuit(L,L)
    
    #Randomly Select L*p qubits 
    meas = int(np.floor(L*p))
    qubits = [i for  i in range(0,L)]

    for i in range(0,L):
        qc.h(i)
    
    for j in range(0, timesteps):

        #Control-Target Gates: 
        for i in range(0, L):
            if i == L-1:
                break
            else:
                qc.cx(i,i+1)
        
        #Perform Random Measurement
        a = np.random.choice(qubits, size=meas)
        for i in a:
            qc.measure(i, i)        
        

        #Target-Control Gates: 
        for i in range(0, L):
            if i == L-1:
                break
            else:
                qc.cx(i+1,i)   

        #Perform Random Measurement
        a = np.random.choice(qubits, size=meas)
        for i in a:
            qc.measure(i, i)
            
        #Single Qubit Gates
        for i in range(0,L):
            if i % 2 == 0:
                qc.h(i)
            elif i % 2 == 1:
                qc.s(i)
        
        #Perform Random Measurement
        a = np.random.choice(qubits, size=meas)
        for i in a:
            qc.measure(i, i)

    return qc

def rand_real_circ3(L, p, timesteps):
    
    qc = QuantumCircuit(L,L)
    
    #Randomly Select L*p qubits 
    meas = int(np.floor(L*p))
    qubits = [i for  i in range(0,L)]
    a = [1,3] 

    for i in range(0,L):
        qc.h(i)
    
    for j in range(0, timesteps):

        #Control-Target Gates: 
        for i in range(0, L):
            if i == L-1:
                break
            else:
                qc.cx(i,i+1)
        
        #Perform  Measurement
        for i in a:
            qc.measure(i, i)        
        

        #Target-Control Gates: 
        for i in range(0, L):
            if i == L-1:
                break
            else:
                qc.cx(i+1,i)   

        #Perform Measurement
        for i in a:
            qc.measure(i, i)
            
        #Single Qubit Gates
        for i in range(0,L):
            if i % 2 == 0:
                qc.h(i)
            elif i % 2 == 1:
                qc.s(i)
        
        #Perform Measurement
        for i in a:
            qc.measure(i, i)

    return qc
