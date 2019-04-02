# arithmetic_expression
code generation for arithmetic expressions, project 2017

### Пример
В качестве примера возьмем следующее арифмитическое выражение.
```
A = (3 + B) * 4 + [2 * (C + D)]
```
Перед машинной генерацией кода удобно построить дерево, в состав которого входят вершины (которые либо хранят идентификатор/константу, являющиеся листьями, либо хранят информацию о двух потомках и арифмическую операцию).
Дерево не содержит скобок, отражает всю информацию о приоритетах операторов и позволяет однозначно восстановить и вычислить значение выражения.

```
Self: = | Type of self: EQUAL | Father: None | Left: None | Right: None
Self: A | Type of self: IDENTIFIER | Father: = | Left: None | Right: +
Self: + | Type of self: PLUS | Father: = | Left: A | Right: None
Self: * | Type of self: MULT | Father: + | Left: None | Right: *
Self: + | Type of self: PLUS | Father: * | Left: None | Right: 4
Self: 3 | Type of self: NUM_CONST | Father: + | Left: None | Right: B
Self: B | Type of self: IDENTIFIER | Father: + | Left: 3 | Right: None
Self: 4 | Type of self: NUM_CONST | Father: * | Left: + | Right: None
Self: * | Type of self: MULT | Father: + | Left: * | Right: None
Self: 2 | Type of self: NUM_CONST | Father: * | Left: None | Right: +
Self: + | Type of self: PLUS | Father: * | Left: 2 | Right: None
Self: C | Type of self: IDENTIFIER | Father: + | Left: None | Right: D
Self: D | Type of self: IDENTIFIER | Father: + | Left: C | Right: None
```
В итоге, получается следующая генерация кода:
```
['mov', ' eax, ', '3']
['add', ' eax, ', 'B']
['push', ' eax']
['mov', ' eax, ', '4']
['pop', ' edx']
['xchg', ' eax, ', 'edx']
['mult', ' eax, ', 'edx']
['push', ' eax']
['mov', ' eax, ', 'C']
['add', ' eax, ', 'D']
['push', ' eax']
['mov', ' eax, ', '2']
['pop', ' edx']
['xchg', ' eax, ', 'edx']
['mult', ' eax, ', 'edx']
['push', ' eax']
['pop', ' eax']
['pop', ' edx']
['xchg', ' eax, ', 'edx']
['add', ' aex, ', 'edx']
['mov', 'A, aex']
```
Упростим данную генерацию:
```
['mov', ' eax, ', '3']
['add', ' eax, ', 'B']
['mult', ' eax, ', '4']
['push', ' eax']
['mov', ' eax, ', 'C']
['add', ' eax, ', 'D']
['mult', ' eax, ', '2']
['pop', ' edx']
['add', ' aex, ', 'edx']
['mov', 'A, aex']
```
