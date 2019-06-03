#!/usr/bin/env python
# -*- coding: utf-8 -*-
from rubik import Rubik

InitMoveRange = 1, 5

rubik = Rubik()
print("solved on", rubik.get_solution_percent())

for i in range(20):
    InitialSequence = rubik.get_random_sequence(InitMoveRange[0], InitMoveRange[1])
    print(InitialSequence)




