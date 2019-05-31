#!/usr/bin/env python
# -*- coding: utf-8 -*-
from rubik import Rubik

### ПАРАМЕТРЫ

# диапазон длины начальной комбинации для "разборки" кубика
InitMoveRange = 10, 20
# диапазон для генерации случайных последовательностей
RandomSequenceRange = 1, 5
# максимальное количество проверенных комбинаций, не приведших к учеличению индекса решенности
# по достижении данной величины происходит возврат состояния кубика к предыдущему сохраненному состоянию
#MaxUngoodSequences = 100000
MaxUngoodSequences = 0
for i in range(RandomSequenceRange[0], RandomSequenceRange[1] + 1):
    MaxUngoodSequences += 12 ** i * 2

### ИНИЦИАЛИЗАЦИЯ

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
# начальный индекс решенности
CurrentSolutionIndex = rubik._get_solution_index()
# печать процента решенности кубика
print("solved on", rubik.get_solution_percent(), "%")
# сброс счетчика движений
rubik.reset_rotate_count()

# начало поиска
print("begin solving ...")
# текущее количество шагов - удачных комбинаций
StepsCount = 0
# список состояний кубика, в которых произошло увеличение индекса решенности
GoodLayouts = []
# список списков тупиковых комбинаций для каждого состояния
DeadendSequences = [[]]
# решение
Solution = []
# количество проверенных комбинаций c последнего увеличения индекса решенности
SequencesCountFromGoodLayout = 0
while True:
    # генерируем случайную последовательность и применяем ее
    # если после этого процент решенности возрос, то считаем последовательность успешной и продолжаем
    # в противном случае откатываемся назад и пробуем другую последовательность
    
    # сохраняем текущее состояние кубика
    CurrentLayout = rubik._get_layout()
    # генерируем последовательность
    CurrentSequence = rubik.get_random_sequence(RandomSequenceRange[0], RandomSequenceRange[1])
    # проверяем нет ли этой последовательности в списке тупиковых для текущего шага
    if CurrentSequence in DeadendSequences[len(DeadendSequences) - 1]:
        continue
    # выполняем последователность
    rubik.execute_sequence(CurrentSequence)
    # проверяем стало ли лучше
    NewSolutionIndex = rubik._get_solution_index()
    if NewSolutionIndex > CurrentSolutionIndex:
        StepsCount += 1
        DeadendSequences.append([])
        # состояние улучшилось - считаем ход удачным, записываем в решение
        Solution.append(CurrentSequence)
        # сохраним состояние кубика
        #GoodLayouts.append(rubik._get_layout())
        # сохраняем состояние до текущих изменений
        GoodLayouts.append(CurrentLayout)
        # сброс количества комбинаций
        SequencesCountFromGoodLayout = 0
        # устанавливаем текущим индексом решенности новый
        CurrentSolutionIndex = NewSolutionIndex
        
        print("+", StepsCount, "SP", CurrentSolutionIndex * 100, "%, SL", len(",".join(Solution).split(",")), ", Mv", rubik.get_rotate_count(), ",", Solution[len(Solution) - 1])

        # проверяем вдруг решен
        if CurrentSolutionIndex == 100.0:
            break;
    else:
        # если состояние не улучшилось, то возвращаем к предыдущему состоянию
        rubik._set_layout(CurrentLayout)
        # увеличиваем количество проверенных комбинаций не приведших к увеличению индекса решенности
        SequencesCountFromGoodLayout += 1
        # проверяем не превысило ли количество допустимый порог
        if SequencesCountFromGoodLayout >= MaxUngoodSequences:
            # сбрасываем счетчик последовательностей
            SequencesCountFromGoodLayout = 0
            # восстанавливаем последнюю удачную комбинацию, если такова существует
            if len(GoodLayouts):
                print("rollback to previous state")
                StepsCount -= 1
                # удаляем текущее состояние и берем предыдущее
                rubik._set_layout(GoodLayouts.pop())
                # удаляем последний список для тупоковой последовательности
                DeadendSequences.pop()
                # добавляем тупиковую последовательность в списко тупиковых последовательностей предыдущего шага
                # заодно удаляем тупиковую последовательность из решения
                DeadendSequences[len(DeadendSequences) - 1].append(Solution.pop())
                CurrentSolutionIndex = rubik._get_solution_index()
                print("-", StepsCount, "SP", CurrentSolutionIndex * 100, "%, SL", len(",".join(Solution).split(",")), ", Mv", rubik.get_rotate_count())


    # вывод статистики каждые N комбинаций
    #if rubik.get_rotate_count() % 10000 == 0:
        #print("SP", CurrentSolutionIndex * 100, "%, SL", len(",".join(Solution).split(",")), ", BC", SequencesCountFromGoodLayout, ", Mv", rubik.get_rotate_count())
        
# если вдруг решение найдено то выведем его
print("-" * 80)
print("for initial sequence:", InitialSequence)
print("found solution:", ",".join(Solution))
