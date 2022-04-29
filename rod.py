# -*- rod.py -*- coding: utf-8 -*-
"""
Created on Sun Apr 24 05:02:27 2022

@author: Tan Le Dinh
"""

import numpy as np
from tabulate import tabulate

"""
Variable - Describe:
nn ............ The number of nodes
ne ............ The number of elements
coord ......... The vector of node coordinates
absembly ...... The matrix of absembly
para .......... The matrix stores the geometric and material parameters
dcond ......... The condition of displacement
fcond ......... The condition of force
ke ............ The stiffness matrix of element
pe ............ The vector of element load
gk ............ The global stiffness matrix
gp ............ The global vector of load
q ............. The global vector of displacement
sigma ......... The vector of element stress
"""
#%% Preprocessing
nn = 3
ne = 2
coord = np.array([0, 10, 20])
absembly = np.array([[0, 1], [1, 2]])
para = np.array([[10, 2, 2*1e-6], [10, 1, 2e-6]])
fcond = np.array([2, 1000],dtype=np.int)
dcond = np.array([0, 0])

#%% Processing
gk = np.zeros([nn, nn])
gp = np.zeros([nn, 1])

# Compute the global stiffness matrix and the global load vector
for e in range(ne):
    i = absembly[e, 0] 
    j = absembly[e, 1]
    x1 = coord[i]
    x2 = coord[j]
    le = para[e, 0] # The length of rod of element e
    ae = para[e, 1] # The area of cross-section of element e
    ee = para[e, 2] # The Young modulus of element e
    # The element stiffness matrix
    ke = ae*ee/le*np.array([[1, -1], [-1, 1]])
    # Absembly the stiffness matrix
    gk[i, i] = gk[i, i] + ke[0, 0]
    gk[i, j] = gk[i, j] + ke[0, 1]
    gk[j, i] = gk[j, i] + ke[1, 0]
    gk[j, j] = gk[j, j] + ke[1, 1]
    # The element load vector
    pe = np.array([0, 0])
    # Absembly the load vector
    gp[i] = gp[i] + pe[0]
    gp[j] = gp[j] + pe[1]

# The condition of node
for i in range(fcond.shape[0]-1):
    gp[fcond[i]] = gp[fcond[i]] + fcond[i+1]
    
for i in range(dcond.shape[0]-1):
    for j in range(nn):
        gp[j] = gp[j] - gk[j, dcond[i]]*dcond[i+1]
    for j in range(nn):
        gk[dcond[i],j] = 0.0
        gk[j,dcond[i]] = 0.0
    gk[dcond[i],dcond[i]] = 1.0
    gp[dcond[i]] = dcond[i+1]
    
q = np.dot(np.linalg.pinv(gk), gp) # Or use q = np.linalg.solve(gk,gp)
#%% Post-processing
print('Results')
# Display the displacement
print('The displacement of nodes')
head = ['Node', 'Displacement']
data = np.concatenate((np.array([[1], [2], [3]]), q), axis = 1)
print(tabulate(data, headers=head, tablefmt='grid'))

# Display the stress
sigma=[]
for e in range(ne):
    sigma.append(para[e,2]*(q[absembly[e,1]]-q[absembly[e,0]])/para[e,0])
print('The stress of the element')
head_stress = ['Element','Stress']
data1 = np.hstack((np.array([[1], [2]]), sigma))
print(tabulate(data1, headers=head_stress, tablefmt='grid'))




    
    


















