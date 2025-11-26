class CalculatorException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class Calculator(object):
    def eval(self, string):
        buffer = ''
        digits = []
        operators = []
        list1 = []
        priority = {
        '+' : 1,
        '-' : 1,
        '*' : 2,
        '/' : 2
        }

        if '.' in string or ',' in string:
            raise CalculatorException("Calculatorul nu poate procesa numere reale")

        if string.count('(') != string.count(')'):
            raise CalculatorException("Parantezele nu sunt inchise corect")

        for char in string:
            if char not in "0123456789+-*/() ":
                raise CalculatorException("Expresia contine caractere invalide")

        for index, char in enumerate(string):
            if char.isdigit():
                buffer = buffer + char
            elif char == '-' and (index == 0 or string[index-1] in '(*+/-'):
                buffer = buffer + char
            else:
                if buffer != '':
                    list1.append(buffer)
                    buffer = ''
                list1.append(char)
        if buffer != '':
            list1.append(buffer)

        for char in list1[:]:
            if char.isspace():
                list1.remove(char)

        i = 0
        while i < len(list1):
            if list1[i] == '-' and (i == 0 or list1[i - 1] in '(*+-/'):
                list1.insert(i, '0')
                i += 1
            i += 1

        try:
            for i in list1:
                try:
                    digits.append(int(i))
                except ValueError:
                    if i in ['+','-','*','/','(']:
                        if i in ['(']:
                            operators.append(i)
                        else:
                            while operators and operators[-1] in priority and priority[operators[-1]]>=priority[i]:
                                self.applyOperation(digits,operators)
                            operators.append(i)
                    elif i in [')']:
                        while operators[-1]!='(':
                            self.applyOperation(digits,operators)
                        operators.pop()

            while operators:
                self.applyOperation(digits,operators)

            return digits[0]
        except (IndexError, ZeroDivisionError) as e:
            if isinstance(e, ZeroDivisionError):
                raise CalculatorException("Impartirea la zero nu este permisa")
            else:
                raise CalculatorException("Expresia este invalida")

    def applyOperation(self, digits,operators):
        digit1 = float(digits.pop())
        op = operators.pop()
        digit2 = float(digits.pop())

        if op == '+':
            result = digit1 + digit2
        elif op == '-':
            result = digit2 - digit1
        elif op == '*':
            result = digit1 * digit2
        elif op == '/':
            if digit1 == 0:
                raise ZeroDivisionError("Impartirea la zero nu este permisa")
            result = digit2 / digit1
        digits.append(result)

    def read(self):
        return input('> ')

    def loop(self):
        while (line := self.read()) != 'quit':
            try:
                result = self.eval(line)
                if result == int(result):
                    print(int(result))
                else:
                    print(result)
            except CalculatorException as e:
                print(f"Eroare: {e.message}")
            except Exception:
                print("Eroare: Calculatorul nu poate rezolva expresia data.")

if __name__ == '__main__':
    calculator = Calculator()
    calculator.loop()

