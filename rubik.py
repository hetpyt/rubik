#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pprint import pprint

class Rubik:
    """Rubik solving class"""

    _colors = "W", "Y", "B", "G", "R", "O"
    _sides = "F", "B", "U", "D", "R", "L"
    _linked = { "F": (("L", (2, 0), (2, 1), (2, 2)), ("U", (0, 0), (1, 0), (2, 0)), ("R", (0, 2), (0, 1), (0, 0)), ("D", (2, 2), (1, 2), (0, 2))),
                "B": (("L", (0, 2), (0, 1), (0, 0)), ("D", (0, 0), (1, 0), (2, 0)), ("R", (2, 0), (2, 1), (2, 2)), ("U", (2, 2), (1, 2), (0, 2))),
                "U": (("L", (2, 2), (1, 2), (0, 2)), ("B", (0, 0), (1, 0), (2, 0)), ("R", (2, 2), (1, 2), (0, 2)), ("F", (2, 2), (1, 2), (0, 2))),
                "D": (("L", (0, 0), (1, 0), (2, 0)), ("F", (0, 0), (1, 0), (2, 0)), ("R", (0, 0), (1, 0), (2, 0)), ("B", (2, 2), (1, 2), (0, 2))),
                "R": (("F", (2, 0), (2, 1), (2, 2)), ("U", (2, 0), (2, 1), (2, 2)), ("B", (2, 0), (2, 1), (2, 2)), ("D", (2, 0), (2, 1), (2, 2))),
                "L": (("B", (0, 2), (0, 1), (0, 0)), ("U", (0, 2), (0, 1), (0, 0)), ("F", (0, 2), (0, 1), (0, 0)), ("D", (0, 2), (0, 1), (0, 0)))
              }
    _layout = {}
    
    def __init__(self):
        self._layout = {self._sides[side] : [[self._colors[side] for x in range(3)] for y in range(3)] for side in range(6)}
 
    def _get_vector_data(self, vector):
        side= self._layout[vector[0]]
        return [side[cell[0]][cell[1]] for cell in vector[1:]]
    
    def _set_vector_data(self, vector, data):
        side= self._layout[vector[0]]
        for cell,color in zip(vector[1:],data):
            side[cell[0]][cell[1]] = color
    
    def _print_side(self, side, tab):

        for y in range(2, -1, -1):
            print(tab, end= "")
            for s in side:
                for x in range(3):
                    print(self._layout[s][x][y] + " ", end= "")
            print()
    
    def printLayout(self):
        # print U
        self._print_side(["U"], " " * 6)
        self._print_side(["L", "F", "R"], "")
        self._print_side(["D"], " " * 6)
        self._print_side(["B"], " " * 6)
        
        
        
    def isSolved(self):
        for side in self._layout:
            sidecolor= self._layout[side][1][1]
            if len([self._layout[side][x][y] for x in range(3) for y in range(3) if self._layout[side][x][y] != sidecolor]) != 0: 
                return False
        return True
    
    def rotate_side(self, side, CW = True):
        """Rotate one side of cube CW or CCW"""
        
        tside= self._layout[side][:]
        if CW:
            # rotate main side
            self._layout[side] = [[tside[x][y] for x in range(2, -1, -1)] for y in range(3)]
            # rotate adjoining parts of 4 perpendicular sides
            tlast= self._get_vector_data(self._linked[side][3])
            for i in range(3, 0, -1):
                self._set_vector_data(self._linked[side][i], self._get_vector_data(self._linked[side][i-1]))
            self._set_vector_data(self._linked[side][0], tlast)
                
        else:
            # rotate main side
            self._layout[side] = [[tside[x][y] for x in range(3)] for y in range(2, -1, -1)]
            # rotate adjoining parts of 4 perpendicular sides
            tfirst= self._get_vector_data(self._linked[side][0])
            for i in range(3):
                self._set_vector_data(self._linked[side][i], self._get_vector_data(self._linked[side][i+1]))
            self._set_vector_data(self._linked[side][3], tfirst)
                
    
rubik= Rubik();
pprint(rubik._layout, width= 25)
print("is solved:", rubik.isSolved())
rubik.printLayout();

rubik.rotate_side("L")

rubik.printLayout();
