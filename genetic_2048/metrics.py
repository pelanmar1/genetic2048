# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import copy

x = [[2, 2, 2, 2],
     [0, 0, 4, 4],
     [0, 0, 0, 0],
     [0, 0, 0, 0]]

def slide_r(listp):
    listc = copy.deepcopy(listp)
    n = len(listc)
    i=0
    while i< (n-1):
        a = listc[i]
        b = listc[i+1]
        if a != 0 and b == 0:
            listc[a] =
        if a == b:
            listc[i] = 0
            listc[i+1] = 2 * listc[i+1]
            i+=1
        i += 1
            
    return listc
            


    

temp = x[0]
print(temp)
temp = slide_r(temp)
print(temp)