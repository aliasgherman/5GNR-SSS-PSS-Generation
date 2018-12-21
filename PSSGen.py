#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 20 21:56:19 2018

@author: aamhabiby
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def x(m, depth):
    i = m - 7
    #print("<M, I>", m, i, depth)
    if (m == 6) or (m == 5) or (m == 4) or (m == 2) or (m == 1):
        return 1
    elif (m == 0) or (m == 3):
        return 0
    else:
        #print("Calling with x(", i+4, ") + x(", i, ")")
        return (x(i + 4, depth+1) + x(i, depth+1)) % 2
        


def m(n, NID2):
    return (n + 43*NID2) % 127

#print("Returned ", x(50,1))
#########################################################
# We have pre-computed the results of x(m) for m = 0 to 126
# inside a dataframe (x_of_m_calculated.csv)    
#x_table = []
#for i in range(0, 127):
#    x_table.append(x(i, 1))
#    if ((i % 10) == 0):
#        print("There there.", i)
#    #print(i, m(i, 0), x(m(i, 0), 1))
####################################################


df = pd.read_csv('x_of_m_calculated.csv')

def precomputed_x(m):
    if (m < 0) or (m > 126):
        print("Error in m value.", m)
        
    else:
        return df.iloc[m].X_of_M
    
def generate_d_n(NID2):
    #NID2 is the PSS ID which can be 0, 1 or 2
    seq = []
    for i in range(0, 127):
        seq.append(1 - 2 * (precomputed_x( m(i, NID2))))
    return seq



def corr_PSS(pss):
    #we are only counting the elements which are equal in position and value for both sequences
    res = []
    for i in range(0, len(pss)):
        for j in range(i + 1, len(pss)):
            print("Corr PCI ",j, i, np.sum( np.array(pss[j]) == np.array(pss[i])))
            res.append([j, i, np.sum( np.array(pss[j]) == np.array(pss[i])) ])
    return res


PSS = []
for i in range(0, 3):
    PSS.append( generate_d_n(i) )
    
res = corr_PSS(PSS)

resExport = pd.DataFrame(res, columns=['PSS 0', 'PSS 1', 'CORR', 'XCORR_LAG_0'])
print(resExport.head(10))
resExport.to_csv('PCI_PSS_Correlations.csv')
