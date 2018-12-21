#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 21 08:01:07 2018
@author: aamhabiby
"""
###################################################################################################
###################################################################################################
###################################################################################################
# 5G NR SSS generation is defined in 3GPP 38.211 
# The main SSS function depends on 2 sequences called x0 and x1 which depend upon the PSS and SSS id
# x0 and x1 are recursive sequences and take a long time for computation.
# so in this file, the original function is defined and then the values are computed and saved in 
# pandas dataframe for further uses to save the run time of the program
###################################################################################################
###################################################################################################
###################################################################################################


import pandas as pd
import matplotlib.pyplot as plt
import math
import numpy as np


def x0(m, depth):
    i = m - 7
    if (m == 6) or (m == 5) or (m == 4) or (m == 2) or (m == 1) or (m == 3):
        return 0
    elif (m == 0):
        return 1
    else:
        #print("Calling with x(", i+4, ") + x(", i, ")")
        return (x0(i + 4, depth+1) + x0(i, depth+1)) % 2
######################################################################################################
# The below lines can be used for generation of X0 values once and then they can be reused without computation
######################################################################################################
#x0_table = []
#for i in range(0, 127):
#    x0_table.append(x0(i, 1))
#    if ((i % 10) == 0):
#        print("There there.", i)
#
######################################################################################################

def x1(m, depth):
    i = m - 7
    #print("<M, I>", m, i, depth)
    if (m == 6) or (m == 5) or (m == 4) or (m == 2) or (m == 1) or (m == 3):
        return 0
    elif (m == 0):
        return 1
    else:
        #print("Calling with x(", i+4, ") + x(", i, ")")
        return (x1(i + 1, depth+1) + x1(i, depth+1)) % 2
				
######################################################################################################
# The below lines can be used for generation of C1 values once and then they can be reused without computation
######################################################################################################
#x1_table = []
#for i in range(0, 127):
#    x1_table.append(x1(i, 1))
#    if ((i % 10) == 0):
#        print("There there.", i)
######################################################################################################

def m0(NID1, NID2):
    assert (NID1 >= 0) and (NID1 <= 335)
    assert (NID2 >= 0) and (NID2 <= 2)
    return ((15 * math.floor( NID1 / 112)) + 5* (NID2))

def m1(NID1):
    assert (NID1 >= 0) and (NID1 <= 335)
    return ((NID1 % 112))

def d(n, NIDCELL):
    assert (NIDCELL >= 0) and (NIDCELL <= 1007)
    NID1 = math.floor(NIDCELL / 3)
    NID2 = NIDCELL % 3
    return (  (1 - (2 * df1.iloc[( (n + m0(NID1, NID2) ) % 127)].X0_of_M) ) 
            * (1 - (2 * df2.iloc[( (n + m1(NID1)       ) % 127)].X1_of_M) ))

def generate_d_n(NIDCELL):
    res = []
    for i in range(0, 127):
        res.append(d(i, NIDCELL))
    return res
            

def corr_SSS(sss):
    #we are only counting the elements which are equal in position and value for both sequences
    res = []
    for i in range(0, len(sss)):
        for j in range(i + 1, len(sss)):
            #print("Corr PCI ",j, i, np.sum( np.array(sss[j]) == np.array(sss[i])))
            res.append([i, j, np.sum( np.array(sss[i]) == np.array(sss[j])), np.correlate(sss[i], sss[j], 'valid')[0] ] )
    return res


df1 = pd.read_csv('X0_of_M.csv')
df2 = pd.read_csv('X1_of_M.csv')

SSS = []

for j in range(0, 1008):
    SSS.append(generate_d_n(j))

res = corr_SSS(SSS)
resExport = pd.DataFrame(res, columns=['PCI1', 'PCI2', 'CORRELATION', 'XCORR_LAG_0'])
print(resExport.head())
resExport.to_csv('PCI_SSS_Correlations.csv')
