#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random

class Rubik:
    """Rubik's cube simulation class"""

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
        self._rotate_counter = 0;
        random.seed()

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
    
    def print_layout(self):
        # print U
        self._print_side(["U"], " " * 6)
        self._print_side(["L", "F", "R"], "")
        self._print_side(["D"], " " * 6)
        self._print_side(["B"], " " * 6)
        
    def get_rotate_count(self):
        return self._rotate_counter
        
    def reset_rotate_count(self):
        self._rotate_counter = 0
        
    def is_solved(self):
        for side in self._layout:
            sidecolor= self._layout[side][1][1]
            if len([self._layout[side][x][y] for x in range(3) for y in range(3) if self._layout[side][x][y] != sidecolor]) != 0: 
                return False
        return True
        
    def get_solve_percention(self):
        count = 0
        for side in self._layout:
            sidecolor= self._layout[side][1][1]
            count += len([self._layout[side][x][y] for x in range(3) for y in range(3) if self._layout[side][x][y] == sidecolor])
        return round(count / 54 * 100)
    
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
        self._rotate_counter += 1
    
    def rotate_side_random(self):
        self.rotate_side(random.choice(self._sides), 0.5 > random.random())
        
    def get_random_sequence(self, min_count = 100, max_count = 100):
        result = "";
        for i in range(random.randint(min_count, max_count) + 1):
            result += random.choice(self._sides) + random.choice(["", "'"]) + ","
        return result[:len(result)-1]
        
    def execute_sequence(self, sequence):
        count = 0
        for command in sequence.split(","):
            command = command.strip()
            print("'" + command + "'")
            if len(command) == 0:
                continue
            # silly check    
            if not command[0] in self._sides:
                break
            self.rotate_side(command[0], len(command) == 1)   
        return count    
    
rubik = Rubik();

rubik.print_layout();
print("solved on", rubik.get_solve_percention(), "%")
print("gettind some entropy ...")
rubik.execute_sequence(rubik.get_random_sequence())
print("solved on", rubik.get_solve_percention(), "%")
rubik.reset_rotate_count()
print("begin solving ...")
max_percent = 0
while not rubik.is_solved():
    rubik.rotate_side_random();
    if rubik.get_rotate_count() % 1000 == 0:
        cur_percent = rubik.get_solve_percention();
        max_percent = max(max_percent, cur_percent)
        print("solved on", cur_percent, "%, max", max_percent, "%, ", rubik.get_rotate_count(), "moves")
