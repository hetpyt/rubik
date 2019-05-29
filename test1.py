#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pprint import pprint

matrix= [[1,2,3],
        [4,5,6],
        [7,8,9]]

pprint(matrix, width= 20)
print()
matrix1= [[row[i] for row in matrix] for i in range(2, -1, -1)]
print()
pprint(matrix1, width=20)
matrix2= [[matrix[row][i] for row in range(2, -1, -1)] for i in range(3)]
print()
pprint(matrix2, width=20)