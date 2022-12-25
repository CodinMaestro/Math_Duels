import math


class Math_question:
    def __init__(self, line):
        self.problem = line
        self.question = ''
        self.numbers = {}
        self.numbers['1'] = 1
        self.numbers['0'] = 1
        self.operations = {'**': 0, '*': 0, '+': 0, '-': 0, '/': 0, '!': 0, 'V‾': 0}

    def checking_for_correctness(self):
        if len(self.question) > 100:
            return False
        for i in range(len(self.sym[::-3])):
            if len(self.sym) > 3:
                if self.sym[i] == self.sym[i + 1] == self.sym[i + 2] == self.sym[i + 3]:
                    return False
        symbols = self.question.split()
        for si in range(len(symbols)):
            if symbols[si].isdigit():
                if symbols[si] not in self.numbers:
                    self.numbers[symbols[int(si)]] = 1
                else:
                    return False
            if '!' in symbols[si]:
                symbols[si] = factorial(symbols[si][1:-2])
            if 'V‾' in symbols[si]:
                symbols[si] = root(symbols[si][3:-1])
        if len(symbols) > 0:
            if not symbols[0] is None:
                self.question = ''.join(symbols)
                return True

    def transformation(self):
        s = self.problem
        pr = ' '
        n = 0
        self.sym = []
        for i in range(len(self.problem)):
            if s[i].isdigit():
                self.question += s[i]
            elif not s[i].isalpha() or s[i] == 'V':
                if s[i] == '.':
                    self.question += s[i]
                elif s[i] == '*' and s[i + 1] == '*':
                    self.question += pr + '**' + pr
                    self.sym.append('**')
                    if s[i] in self.operations:
                        self.operations['**'] += 1
                elif s[i] in '+-/':
                    self.question = self.question + pr + s[i] + pr
                    self.sym.append(s[i])
                    if s[i] in self.operations:
                        self.operations[s[i]] += 1
                elif s[i] == '!':
                    self.sym.append(s[i])
                    self.question = self.question[:-1] + s[i]
                    if s[i] in self.operations:
                        self.operations[s[i]] += 1
                elif s[i] == 'V' and s[i + 1] == '‾':
                    self.sym.append('V‾')
                    self.question += ' V‾'
                    if s[i] in self.operations:
                        self.operations['V‾'] += 1
                elif s[i] in '()':
                    if s[i] == '(':
                        n += 1
                        pr = ''
                        self.question += pr + s[i]
                    if s[i] == ')':
                        n -= 1
                        if i + 1 < len(self.problem) and n == 0:
                            if s[i + 1] != ')':
                                pr = ' '
                        self.question += s[i] + pr
        return self.question

    def answer(self):
        return eval(self.question)

    def print_summ(self):
        summ = 0
        summ += self.operations['+']
        summ += self.operations['-'] * 2
        summ += self.operations['*'] * 3
        summ += self.operations['/'] * 4
        summ += self.operations['V‾'] * 6
        summ += self.operations['**'] * 5
        summ += self.operations['!'] * 4
        return summ


def root(question):
    p = Math_question(question)
    np = p.transformation()
    if p.checking_for_correctness():
        return str(math.sqrt(eval(np)))


def factorial(question):
    p = Math_question(question)
    np = p.transformation()
    if p.checking_for_correctness():
        return str(math.factorial(eval(np)))


n = input()
p = Math_question(n)
np = p.transformation()
s = p.checking_for_correctness()
if s:
    print(p.answer())
    print(p.print_summ())
else:
    print('Ошибка')
