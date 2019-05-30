#!/usr/bin/env python
# -*- coding: utf-8 -*-
from rubik import Rubik

# поиск алгоритма бога для случайного состояния кубика
# создание объекта класса Rubik 
rubik = Rubik();
# печать процента решенности кубика
print("solved on", rubik.get_solution_percent(), "%")
# случайная перестановка граней кубика 
print("gettind some entropy ...")
InitialSequence = rubik.get_random_sequence()
#print("initial sequence:", InitialSequence)
print("random moves count", rubik.execute_sequence(InitialSequence))
# печать развертки кубика
rubik.print_layout();
# печать процента решенности кубика
print("solved on", rubik.get_solution_percent(), "%")
InitialLayout = rubik._get_layout()
# сброс счетчика движений
rubik.reset_rotate_count()
# начало поиска
print("begin solving ...")
# максимальный процент решенности кубика
MaxPercent = 0
# количество проверенных комбинаций
CombinationsCount = 0
while not rubik.is_solved():
    # восстанавливаем исходное состояние кубика
    rubik._set_layout(InitialLayout)
    # генерируем случайную комбинацию из 26 движений (число бога)
    CurrentSequence = rubik.get_random_sequence(rubik.get_god_number(), rubik.get_god_number())
    # увеличиваем счетчик комбинаций
    CombinationsCount += 1
    # выполняем комбинацию
    rubik.execute_sequence(CurrentSequence)
    # получаем процент решенности и вычисляем максимум
    MaxPercent = max(MaxPercent, rubik.get_solution_percent())
    # вывод статистики каждые N комбинаций
    if CombinationsCount % 1000 == 0:
        print("max solution percent", MaxPercent, "%, ", CombinationsCount, "combinations")
        
# если вдруг решение найдено то выведем его
print("-" * 80)
print("for initial sequence:", InitialSequence)
print("found God's algoritm:", CurrentSequence)
