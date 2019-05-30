#!/usr/bin/env python
# -*- coding: utf-8 -*-
from rubik import Rubik

# диапазон длины начальной комбинации для "разборки" кубика
InitMoveRange = 10, 20
# диапазон для генерации случайных последовательностей
RandomSequenceRange = 1, 10
# создание объекта класса Rubik 
rubik = Rubik();
# печать процента решенности кубика
print("solved on", rubik.get_solution_percent(), "%")
# случайная перестановка граней кубика 
print("gettind some entropy ...")
InitialSequence = rubik.get_random_sequence(InitMoveRange[0], InitMoveRange[1])
#print("initial sequence:", InitialSequence)
print("random moves count", rubik.execute_sequence(InitialSequence))
# печать развертки кубика
rubik.print_layout();
CurrentSolutionIndex = rubik._get_solution_index()
# печать процента решенности кубика
print("solved on", rubik.get_solution_percent(), "%")
# сброс счетчика движений
rubik.reset_rotate_count()
# начало поиска
print("begin solving ...")
# максимальный процент решенности кубика
MaxPercent = 0
# решение
Solution = ""
# количество проверенных комбинаций
CombinationsCount = 0
while True:
    # генерируем случайную последовательность и применяем ее
    # если после этого процент решенности возрос, то считаем последовательность успешной и продолжаем
    # в противном случае откатываемся назад и пробуем другую последовательность
    
    # сохраняем текущее состояние кубика
    CurrentLayout = rubik._get_layout()
    # генерируем последовательность
    CurrentSequence = rubik.get_random_sequence(RandomSequenceRange[0], RandomSequenceRange[1])
    # выполняем последователность
    rubik.execute_sequence(CurrentSequence)
    # проверяем стало ли лучше
    NewSolutionIndex = rubik._get_solution_index()
    if NewSolutionIndex > CurrentSolutionIndex:
        # состояние улучшилось - считаем ход удачным, записываем в решение
        Solution += CurrentSequence + ","
        CurrentSolutionIndex = NewSolutionIndex
        if CurrentSolutionIndex == 100.0:
            break;
    else:
        # если состояние ухудшилось, то возвращаем к предыдущему состоянию
        rubik._set_layout(CurrentLayout)
    
    # вывод статистики каждые N комбинаций
    if rubik.get_rotate_count() % 1000 == 0:
        print("solution percent", CurrentSolutionIndex * 100, "%,", rubik.get_rotate_count(), "moves")
        
# если вдруг решение найдено то выведем его
print("-" * 80)
print("for initial sequence:", InitialSequence)
print("found solution:", Solution)
