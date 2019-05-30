#!/usr/bin/env python
# -*- coding: utf-8 -*-
from rubik import Rubik

InitMoveRange = 10, 20

rubik = Rubik()
print("solved on", rubik.get_solution_percent())

InitialSequence = rubik.get_random_sequence(InitMoveRange[0], InitMoveRange[1])
print("sequence:", InitialSequence)

rubik.execute_sequence(InitialSequence)
print("solved on", rubik.get_solution_percent())

ReverseSequence = rubik.reverse_sequence(InitialSequence)
print("sequence:", ReverseSequence)

rubik.execute_sequence(ReverseSequence)
print("solved on", rubik.get_solution_percent())




