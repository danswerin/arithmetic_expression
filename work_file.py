SYMBOLS = {'(': 'LBRC', ')': 'RBRC',
           '=': 'EQUAL', '+': 'PLUS', '-': 'MINUS', '*': 'MULT', '/': 'DIV',
           'div': 'REM_OF_DIV'}

TYPES = ['NUM_CONST', 'OPERATOR',
         'DELIMITER', 'IDENTIFIER']

operators = ['=', '+', '-', '*', '/', 'div']

delimiters = ['(', ')']


class Token:
    def __init__(self, value, _type):
        self.value = value
        if _type in [0, 3]:
            self.type = TYPES[_type]
        else:
            self.type = SYMBOLS[value]


class Lexer:

    def blank_space(self, item):
        return item == ' ' or item == '\n' or item == '\n' or item == '\r'

    def work(self):
        i = 0
        while i < len(text):
            # check if current symbol is the blank space
            if self.blank_space(text[i]):
                i += 1
                continue

            # check if current symbol is alpha
            if text[i].isalpha() or text[i] == '_':
                curr_word = ''
                while i < len(text) and (text[i].isalpha() or text[i].isdigit() or text[i] == '_'):
                    curr_word += text[i]
                    i += 1
                if curr_word == 'div':
                    self.tokens.append(Token(curr_word, 2))
                else:
                    self.tokens.append(Token(curr_word, 3))
                continue

            # check if current symbol is digit
            if text[i].isdigit():
                curr_word = ''
                while i < len(text):
                    if text[i].isdigit() or \
                            (text[i] == '.' and i + 1 < len(text) and text[i + 1].isdigit()):
                        curr_word += text[i]
                        i += 1
                    elif not text[i].isdigit():
                        if text[i] == '.':
                            print('ERROR')
                            exit()
                        else:
                            break
                self.tokens.append(Token(curr_word, 0))
                continue

            # check if current symbol is in operators
            if text[i] in operators:
                curr_word = text[i]
                if text[i + 1] in operators:
                    curr_word += text[i + 1]
                    if curr_word in operators:
                        self.tokens.append(Token(curr_word, 1))
                    else:
                        print('ERROR')
                        exit()
                else:
                    self.tokens.append(Token(curr_word, 1))
                i += len(curr_word)
                continue

            # check if current symbol is a delimiter
            if text[i] in delimiters:
                self.tokens.append(Token(text[i], 2))
                i += 1
                continue
            i += 1

    def __init__(self):
        self.tokens = []


# create new node
class NodeInTree:

    def __init__(self, value=None, _type=None, info=None,):
        self.value = value
        self.type = _type
        self.left = None
        self.right = None
        self.father = None
        # first son (from the left)
        self.son = None
        self._info_ = info
        self.nodeId = None


# the creation of the syntax tree
class SyntaxTree:

    def add_node(self, new_node, father=None):
        if not father:
            father = self.current
        new_node.father = father
        if not father.son:
            father.son = new_node
        else:
            curr_node = father.son
            while curr_node.right:
                curr_node = curr_node.right
            new_node.left = curr_node
            curr_node.right = new_node
        self.current = new_node

    def __init__(self):
        self.root = None
        self.current = None


class Parser:

    def expression(self, father):
        priority = {'div': 5, '*': 4, '/': 4, '+': 3, '-': 3}

        curr_stack = []
        to_output_stack = []
        while self.index < len(self.tokens):
            curr_type = self.tokens[self.index].type
            curr_value = self.tokens[self.index].value

            # operators + brackets
            if curr_value in ['+', '-', '*', '/', 'div', '(', ')']:
                # print curr_value
                tree = SyntaxTree()
                tree.current = tree.root = NodeInTree(curr_value, curr_type)
                if curr_value == '(':
                    curr_stack.append(tree)
                elif curr_value == ')':
                    while curr_stack and curr_stack[-1].root.type != 'LBRC':
                        to_output_stack.append(curr_stack.pop())
                    if curr_stack:
                        curr_stack.pop()
                else:
                    # operator
                    flag = 0
                    while curr_stack and not flag:
                        if curr_stack[-1].current.value in ['+', '-', '*', '/', 'div']:
                            if priority[tree.current.value] <= priority[curr_stack[-1].current.value]:
                                to_output_stack.append(curr_stack.pop())
                            else:
                                flag = 1
                        else:
                            flag = 1

                    curr_stack.append(tree)
            # constants
            elif curr_type == 'NUM_CONST' or curr_type == 'IDENTIFIER':
                tree = SyntaxTree()
                tree.current = tree.root = NodeInTree(curr_value, curr_type)
                to_output_stack.append(tree)

            self.index += 1

        while curr_stack:
            to_output_stack.append(curr_stack.pop())

        for i in to_output_stack:
            print(i.root.value, i.root.type)

        curr_stack = []

        for item in to_output_stack:
            curr_value = item.root.value
            curr_type = item.root.type
            if item.root.value not in ['+', '-', '*', '/', '(', ')', 'div']:
                curr_stack.append(item)
            else:
                b = curr_stack.pop()
                a = curr_stack.pop()

                curr_tree = SyntaxTree()
                curr_tree.current = curr_tree.root = NodeInTree(curr_value, curr_type)
                curr_tree.add_node(a.root, curr_tree.root)
                curr_tree.add_node(b.root, curr_tree.root)

                curr_stack.append(curr_tree)
        self.tree.add_node(curr_stack[0].root, father)

    def work(self):
        father = self.tree.current = self.tree.root = NodeInTree('=', 'EQUAL')
        self.tree.add_node(NodeInTree(self.tokens[self.index].value, self.tokens[self.index].type), father)

        self.index = 2

        self.expression(self.tree.root)
        self.display(self.tree.root)

    def display(self, root):
        if not root:
            return 'There is your tree? :) ERROR IN DISPAY'

        father = root.father.value if root.father else None
        left = root.left.value if root.left else None
        right = root.right.value if root.right else None
        print('Self: %s | Type of self: %s | Father: %s | Left: %s | Right: %s' % (root.value, root.type, father, left,
                                                                                   right))
        self.tree_list.append({'value': root.value, 'type': root.type, 'father': father, 'left': left, 'right': right})
        child = root.son
        while child:
            self.display(child)
            child = child.right

    def __init__(self, tokens):
        self.index = 0
        self.tokens = tokens
        self.tree = SyntaxTree()
        self.tree_list = []


class Assembler:

    def shift_stack(self, index):
        self.curr_stack[index] = {'type': 'TOTAL', 'value': 'TOTAL'}
        for i in range(index + 1, len(self.curr_stack) - 2):
            self.curr_stack[i] = self.curr_stack[i + 2]
        del self.curr_stack[-2:]

    def plus_func(self, index):
        if self.curr_stack[index + 1]['value'] == 'TOTAL':
            add = 2
            if self.curr_stack[index + 2]['value'] == 'TOTAL':
                add = 3
        elif self.curr_stack[index + 2]['value'] == 'TOTAL':
            add = 1
        else:
            add = 0
        if add == 1 or add == 2:
            line = ['mov', ' eax, ', self.curr_stack[index + add]['value']]
            self.total.append(line)
            line = ['pop', 'edx']
            self.total.append(line)
            line = ['xchg', ' eax, ', 'edx']
            self.total.append(line)
            line = ['add', ' eax, ', 'edx']
            self.total.append(line)
            line = ['push', ' aex']
            self.total.append(line)
        elif add == 0:
            line = ['mov', ' eax, ', self.curr_stack[index + 1]['value']]
            self.total.append(line)
            line = ['add', ' eax, ', self.curr_stack[index + 2]['value']]
            self.total.append(line)
            line = ['push', ' eax']
            self.total.append(line)
        else:
            line = ['pop', ' eax']
            self.total.append(line)
            line = ['pop', ' edx']
            self.total.append(line)
            line = ['xchg', ' eax, ', 'edx']
            self.total.append(line)
            line = ['add', ' aex, ', 'edx']
            self.total.append(line)
        self.shift_stack(index)

    def mult_func(self, index):
        if self.curr_stack[index + 1]['value'] == 'TOTAL':
            add = 2
            if self.curr_stack[index + 2]['value'] == 'TOTAL':
                add = 3
        elif self.curr_stack[index + 2]['value'] == 'TOTAL':
            add = 1
        else:
            add = 0
        if add == 1 or add == 2:
            line = ['mov', ' eax, ', self.curr_stack[index + add]['value']]
            self.total.append(line)
            line = ['pop', ' edx']
            self.total.append(line)
            line = ['xchg', ' eax, ', 'edx']
            self.total.append(line)
            line = ['mult', ' eax, ', 'edx']
            self.total.append(line)
            line = ['push', ' eax']
            self.total.append(line)
        elif add == 0:
            line = ['mov', ' eax, ', self.curr_stack[index + 1]['value']]
            self.total.append(line)
            line = ['mult', ' eax, ', self.curr_stack[index + 2]['value']]
            self.total.append(line)
            line = ['push', ' eax']
            self.total.append(line)
        else:
            line = ['pop', ' eax']
            self.total.append(line)
            line = ['pop', ' edx']
            self.total.append(line)
            line = ['xchg', ' eax, ', 'edx']
            self.total.append(line)
            line = ['mult', ' aex, ', 'edx']
            self.total.append(line)
            line = ['push', ' eax']
            self.total.append(line)
        self.shift_stack(index)

    def div_func(self, index):
        if self.curr_stack[index + 1]['value'] == 'TOTAL':
            add = 2
            if self.curr_stack[index + 2]['value'] == 'TOTAL':
                add = 3
        elif self.curr_stack[index + 2]['value'] == 'TOTAL':
            add = 1
        else:
            add = 0
        if add == 1 or add == 2:
            line = ['mov', ' eax, ', self.curr_stack[index + add]['value']]
            self.total.append(line)
            line = ['pop', ' edx']
            self.total.append(line)
            if add == 2:
                line = ['xchg', ' eax, ', 'edx']
                self.total.append(line)
            line = ['idiv', ' eax, ', 'edx']
            self.total.append(line)
            line = ['push', ' eax']
            self.total.append(line)
        elif add == 0:
            line = ['mov', ' eax, ', self.curr_stack[index + 1]['value']]
            self.total.append(line)
            line = ['idiv', ' eax, ', self.curr_stack[index + 2]['value']]
            self.total.append(line)
            line = ['push', ' eax']
            self.total.append(line)
        else:
            line = ['pop', ' eax']
            self.total.append(line)
            line = ['pop', ' edx']
            self.total.append(line)
            line = ['xchg', ' eax, ', 'edx']
            self.total.append(line)
            line = ['idiv', ' aex, ', 'edx']
            self.total.append(line)
            line = ['push', ' eax']
            self.total.append(line)
        self.shift_stack(index)

    def min_func(self, index):
        if self.curr_stack[index + 1]['value'] == 'TOTAL':
            add = 2
            if self.curr_stack[index + 2]['value'] == 'TOTAL':
                add = 3
        elif self.curr_stack[index + 2]['value'] == 'TOTAL':
            add = 1
        else:
            add = 0
        if add == 1 or add == 2:
            line = ['mov', ' eax, ', self.curr_stack[index + add]['value']]
            self.total.append(line)
            line = ['pop', ' edx']
            self.total.append(line)
            if add == 2:
                line = ['xchg', ' eax, ', 'edx']
                self.total.append(line)
            line = ['sub', ' eax, ', 'edx']
            self.total.append(line)
            line = ['push', ' eax']
            self.total.append(line)
        elif add == 0:
            line = ['mov', ' eax, ', self.curr_stack[index + 1]['value']]
            self.total.append(line)
            line = ['sub', ' eax, ', self.curr_stack[index + 2]['value']]
            self.total.append(line)
            line = ['push', ' eax']
            self.total.append(line)
        else:
            line = ['pop', ' eax']
            self.total.append(line)
            line = ['pop', ' edx']
            self.total.append(line)
            line = ['xchg', ' eax, ', 'edx']
            self.total.append(line)
            line = ['sub', ' aex, ', 'edx']
            self.total.append(line)
            line = ['push', ' eax']
            self.total.append(line)
        self.shift_stack(index)

    def expression(self, node=None):

        self.curr_stack = node
        arithm_oper = ['+', '-', '*', '/', 'div']
        index = 0

        while True:
            if self.curr_stack[index]['value'] in arithm_oper:
                if self.curr_stack[index]['value'] == '+' \
                        and self.curr_stack[index + 1]['type'] in ['IDENTIFIER', 'NUM_CONST', 'TOTAL'] \
                        and self.curr_stack[index + 2]['type'] in ['IDENTIFIER', 'NUM_CONST', 'TOTAL']:
                    self.plus_func(index)
                    index = 0
                    continue
                elif self.curr_stack[index]['value'] == '*' \
                        and self.curr_stack[index + 1]['type'] in ['IDENTIFIER', 'NUM_CONST', 'TOTAL'] \
                        and self.curr_stack[index + 2]['type'] in ['IDENTIFIER', 'NUM_CONST', 'TOTAL']:
                    self.mult_func(index)
                    index = 0
                    continue
                elif self.curr_stack[index]['value'] == "/" \
                        and self.curr_stack[index + 1]['type'] in ['IDENTIFIER', 'NUM_CONST', 'TOTAL'] \
                        and self.curr_stack[index + 2]['type'] in ['IDENTIFIER', 'NUM_CONST', 'TOTAL']:
                    self.div_func(index)
                    index = 0
                    continue
                elif self.curr_stack[index]['value'] == "-" \
                        and self.curr_stack[index + 1]['type'] in ['IDENTIFIER', 'NUM_CONST', 'TOTAL'] \
                        and self.curr_stack[index + 2]['type'] in ['IDENTIFIER', 'NUM_CONST', 'TOTAL']:
                    self.min_func(index)
                    index = 0
                    continue

            index += 1
            if index == len(self.curr_stack):
                break

    def shift_node(self, node, index, step, next_step):
        for i in range(index + step, len(node) - next_step):
            node[i] = node[i + next_step]
        del node[-next_step:]

    def optimization(self, node=None):
        index = 0
        oper = ['idiv', 'add', 'sub', 'mult']
        print('BEFORE')
        print('________________________________')
        for i in self.total:
            print(i)
        print('________________________________')
        while True:
            if index + 5 < len(node) and node[index][0] == 'push' and node[index + 1][0] == 'mov' \
                    and node[index + 2][0] == 'pop' and node[index + 3][0] == 'xchg' and node[index + 4][0] in oper:
                node[index] = ['mov', ' edx, ', node[index + 1][2]]
                node[index + 1] = [node[index + 4][0], node[index + 4][1], node[index + 4][2]]
                self.shift_node(node, index, 2, 3)
                print('CURR_INDEX', index)
                print('________________________________')
                for i in self.total:
                    print(i)
                print('________________________________')
                index = 0

                continue

            # mov + operation
            if index + 1 < len(node) and node[index][0] == 'mov' and node[index + 1][0] in oper \
                    and node[index][1] == ' edx, ':
                node[index] = [node[index + 1][0], node[index + 1][1], node[index][2]]
                self.shift_node(node, index, 1, 1)
                print('CURR_INDEX', index)
                print('________________________________')
                for i in self.total:
                    print(i)
                print('________________________________')
                index = 0
                continue

            if index + 2 < len(node) and node[index][0] == 'push' and node[index + 1][0] == 'pop' \
                    and node[index + 2][0] == 'pop':

                node[index] = node[index + 2]
                for i in range(index + 1, len(node) - 2):
                    node[i] = node[i + 2]
                del node[-2:]
                print('CURR_INDEX', index)
                print('________________________________')
                for i in self.total:
                    print(i)
                print('________________________________')
                index = 0

                # self.shift_node(node, index, 1, 2)
                continue

            if index + 1 < len(node) and node[index][0] == 'xchg' and node[index + 1][0] in ['mult', 'add']:
                node[index] = node[index + 1]
                self.shift_node(node, index, 1, 1)
                print('CURR_INDEX', index)
                print('________________________________')
                for i in self.total:
                    print(i)
                print('________________________________')
                index = 0
                continue

            # push + mov + pop + operation
            if index + 3 < len(node) and node[index][0] == 'push' and node[index + 1][0] == 'mov' and \
                    node[index + 2][0] == 'pop' and node[index + 3][0] in oper:
                node[index] = ['mov', ' edx, ', node[index + 1][2]]
                if node[index + 1][1] == node[index + 3][1]:
                    node[index + 1] = ['xchg', ' eax, ', 'edx']
                    node[index + 2] = node[index + 3]
                    self.shift_node(node, index, 3, 1)
                else:
                    node[index + 1] = node[index + 3]
                    for i in range(index + 2, len(node) - 2):
                        node[i] = node[i + 1]
                    del node[-2:]

                print('CURR_INDEX', index)
                print('________________________________')
                for i in self.total:
                    print(i)
                print('________________________________')

                index = 0
                continue

            # last rows push + mov
            if node[-2][0] == 'push' and node[-1][0] == 'mov':
                node[-2] = node[-1]
                del node[-1:]

                print('DELETE LAST PUSH', index)
                print('________________________________')
                for i in self.total:
                    print(i)
                print('________________________________')

                index = 0
                continue

            index += 1
            if index == len(node):
                break

    def work(self, node=None):
        self.expression(node[2:])
        self.total.append(['mov', '%s, aex' % node[1]['value']])
        self.optimization(self.total)
        self.display()

    def display(self):
        for i in self.total:
            print(i)

    def __init__(self, tree):
        # self.index = 0
        self.tree = tree
        self.curr_stack = []
        self.total = []


f = open('text.txt', 'r')
text = f.read()
L = Lexer()
L.work()
for i in L.tokens:
    print(i.type, i.value)

print('\n')
P = Parser(L.tokens)
P.work()
print('\n')


Asmbl = Assembler(P.tree_list)
Asmbl.work(Asmbl.tree)
