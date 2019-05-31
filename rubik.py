#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
from copy import deepcopy

class Rubik:
    """Rubik's cube simulation class"""

    # аббревиатуры цветов граней кубика (wite, yellow, blue, green, red, orange)
    _colors = "W", "Y", "B", "G", "R", "O"
    # аббревиатуры граней кубика (front, back, up, down, right, left)
    _sides = "F", "B", "U", "D", "R", "L"
    # словарь прилежащих граней к какждой грани кубика с указанием относительных координат прилегающих ячеек (для второй части операции поворота грани)
    _linked = { "F": (("L", (2, 0), (2, 1), (2, 2)), ("U", (0, 0), (1, 0), (2, 0)), ("R", (0, 2), (0, 1), (0, 0)), ("D", (2, 2), (1, 2), (0, 2))),
                "B": (("L", (0, 2), (0, 1), (0, 0)), ("D", (0, 0), (1, 0), (2, 0)), ("R", (2, 0), (2, 1), (2, 2)), ("U", (2, 2), (1, 2), (0, 2))),
                "U": (("L", (2, 2), (1, 2), (0, 2)), ("B", (0, 0), (1, 0), (2, 0)), ("R", (2, 2), (1, 2), (0, 2)), ("F", (2, 2), (1, 2), (0, 2))),
                "D": (("L", (0, 0), (1, 0), (2, 0)), ("F", (0, 0), (1, 0), (2, 0)), ("R", (0, 0), (1, 0), (2, 0)), ("B", (2, 2), (1, 2), (0, 2))),
                "R": (("F", (2, 0), (2, 1), (2, 2)), ("U", (2, 0), (2, 1), (2, 2)), ("B", (2, 0), (2, 1), (2, 2)), ("D", (2, 0), (2, 1), (2, 2))),
                "L": (("B", (0, 2), (0, 1), (0, 0)), ("U", (0, 2), (0, 1), (0, 0)), ("F", (0, 2), (0, 1), (0, 0)), ("D", (0, 2), (0, 1), (0, 0)))
              }
    # состояние кубика (инициализируется при создании объекта)
    _layout = {}
    
    def __init__(self):
        # построение начального (решенного) состояния кубика Рубика 3х3х3
        # формирует словарь, где ключи - буквы из _sides обозначающие грани, а значения - двуменрые списки содержащие буквы цветов из _colors
        self._layout = {self._sides[side] : [[self._colors[side] for x in range(3)] for y in range(3)] for side in range(6)}
        # счетчик поворотов (движений) граней кубика
        self._rotate_counter = 0;
        # инициализация ГПСЧ
        random.seed()

    def _get_vector_data(self, vector):
        side= self._layout[vector[0]]
        return [side[cell[0]][cell[1]] for cell in vector[1:]]
    
    def _set_vector_data(self, vector, data):
        side= self._layout[vector[0]]
        for cell,color in zip(vector[1:],data):
            side[cell[0]][cell[1]] = color
    
    def _get_layout(self):
        return deepcopy(self._layout)
        
    def _set_layout(self, layout):
        self._layout = deepcopy(layout)
        
    def _print_side(self, side, tab):
        for y in range(2, -1, -1):
            print(tab, end= "")
            for s in side:
                for x in range(3):
                    print(self._layout[s][x][y] + " ", end= "")
            print()
            
    def _get_solution_index(self):
        count = 0
        for side in self._layout:
            # центральная клетка стороны является "неподвижной", поэтому берем ее за эталон
            sidecolor= self._layout[side][1][1]
            # подсчитываем количество клеток с цветом равным цвету эталонной для всех сторон
            count += len([self._layout[side][x][y] for x in range(3) for y in range(3) if self._layout[side][x][y] == sidecolor])
        # подсчитываем процент как отношение числа "правильных" цветов к общему количеству клеток
        return (count / 54)
        
    def get_god_number(self):
        # возвращает число Бога - количество поворотов граней кубика Рубика необходимое для его решения из любого состояния
        # для кубика Рубика размерности 3х3х3 число Бога равно 20 при разрешенных движениях на 180 градусов
        # если движения на 180 градусов не разрешены (в данном случае), то число Бога равно 26
        return 26
    
    def print_layout(self):
        # печать развертки кубика
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
            # центральная клетка стороны является "неподвижной", поэтому берем ее за эталон
            sidecolor= self._layout[side][1][1]
            # подсчитываем количество клеток с цветом не равным цвету эталонной для всех сторон, и если есть такие то кубик не решен
            if len([self._layout[side][x][y] for x in range(3) for y in range(3) if self._layout[side][x][y] != sidecolor]) != 0: 
                return False
        return True
        
    def get_solution_percent(self):
        return round(self._get_solution_index() * 100)
    
    def rotate_side(self, side, CW = True):
        """Rotate one side of cube CW or CCW"""
        # временная копия вращаемой стороны
        tside= self._layout[side][:]
        if CW:
            # поворот основной стороны по часовой стрелке
            self._layout[side] = [[tside[x][y] for x in range(2, -1, -1)] for y in range(3)]
            # сдвиг прилегающих частей перпендикулярных к текущей сторон 
            tlast= self._get_vector_data(self._linked[side][3])
            for i in range(3, 0, -1):
                self._set_vector_data(self._linked[side][i], self._get_vector_data(self._linked[side][i-1]))
            self._set_vector_data(self._linked[side][0], tlast)
                
        else:
            # поворот основной стороны против часовой стрелки
            self._layout[side] = [[tside[x][y] for x in range(3)] for y in range(2, -1, -1)]
            # сдвиг прилегающих частей перпендикулярных к текущей сторон 
            tfirst= self._get_vector_data(self._linked[side][0])
            for i in range(3):
                self._set_vector_data(self._linked[side][i], self._get_vector_data(self._linked[side][i+1]))
            self._set_vector_data(self._linked[side][3], tfirst)
        self._rotate_counter += 1
    
    def rotate_side_random(self):
        # поворот случайной стороны в случайном направлении
        self.rotate_side(random.choice(self._sides), 0.5 > random.random())
        
    def get_random_sequence(self, min_count = 100, max_count = 100):
        result = ""
        for i in range(random.randint(min_count, max_count)):
            result += random.choice(self._sides) + random.choice(["", "'"]) + ","
        return result[:len(result)-1]
    
    def reverse_sequence(self, sequence):
        result = ""
        commands_list = sequence.split(",")
        for i in range(len(commands_list)-1, -1, -1):
            command = commands_list[i].strip()
            if len(command) == 0:
                continue
            if len(command) == 1:
                result += command + "',"
            else:
                result += command[0] + ","
        return result[:len(result)-1]
        
    def execute_sequence(self, sequence):
        count = 0
        for command in sequence.split(","):
            command = command.strip()
            if len(command) == 0:
                continue
            # проверка допустимости команды    
            if not command[0] in self._sides:
                break
            self.rotate_side(command[0], len(command) == 1) 
            count += 1
        return count    
