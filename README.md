# 5GNR-SSS-PSS-Generation
Python Functions to generate the sequences for 5G NR PSS and SSS and correlate

# Disclaimer
The code here is not written to be fast. It is written so that it is understandable when comparing the 3GPP specs which means there are certain loops and recursion in the code which could have been avoided.

Kindly report any problems to aliasgherman@gmail.com


# File Name : PSSGen.py
PSS generation depends on sequence functions as defined in 3GPP 38.211 which include
  x(m)
  m(n)
  d(n)
All these are included in the file so that the final output can be gathered by calling the function 
  generate_d_n( <VALUE of PSS> )
    where <VALUE OF PSS> can be 0, 1 or 2

Another function tries to check for correlation using same sequence values on same index (to get an idea of interference between two specific values of PSS). This is for some research but you may use / modify as per your usage.

# File Name : SSSGen.py
SSS generation depends on sequence functions as defined in 3GPP 38.211 which include
  x0(m)
  x1(m)
  m0(PSS, SSS)
  m1(SSS, m0)
  d(n)
All these are included in the file so that the final output can be gathered by calling the function
  generate_d_n(<VALUE OF PCI>)
    where <VALUE OF PCI> is from 0 to 1007
  
Another function tries to check for correlation using same sequence values on same index to get correlation between different PCI values.

# File Name : x_of_m_calculated.csv
These include calcualted values for the PSS sequence x(m) for m between 0 to 127

# File Name : X0_of_M.csv
These include calculated values for the SSS sequence x0(m) for m between 0 to 127

# File Name : X1_of_M.csv
These include calculated values for the SSS sequence x1(m) for m between 0 to 127

# File Name : PCI_SSS_Correlations.csv
This file includes results of each PCI value compared to all other PCI values and the number of entries which were same on same index. (Same subcarrier and same value of transmission. Higher the value, higher the interference)
  
