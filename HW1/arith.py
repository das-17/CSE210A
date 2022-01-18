import sys
#References: 'https://ruslanspivak.com/lsbasi-part1/' , 'https://ruslanspivak.com/lsbasi-part7/'

#Token Class: To represent different characters we come across in the string.
#Token types: INTEGER,ADD,SUB,MUL,DIV,MOD
class Token:

    #Token "constructor"
    def __init__(self, type,value):
        self.type = type
        self.value = value

    #Display Token for debugging purposes
    def printToken(self):
          print(Token({type}, {value}).format(type=self.type, value=repr(self.value)))

#Lexer Class:Converts the string to Tokens
class Lexer:

    #Constructor for the lexer
    def __init__(self, expression):
        self.expression = expression
        self.index = 0
        self.current = self.expression[self.index]

    def __getitem__(self, index):
        return self.index

    #Iterates through the next character in the string
    def nextChar(self):
        self.index += 1
        if(self.index) > len(self.expression) - 1:
            self.current = None#'None'
        else:
            self.current = self.expression[self.index]

    #Multi-digits also taken into account
    def intVal(self):
        operand = ''
        while self.current is not None and self.current.isdigit():
            operand += self.current
            self.nextChar()

        return int(operand)



    #Checking for negative numbers
    def negativeInt(self):
        if self.current == '-' and self.expression[self.index + 1].isdigit():
            self.nextChar()
            value = self.intVal() * -1
        return value

    #Iterating through expression and converting into tokens
    def exprToToken(self):
        while self.current is not None:
            if self.current.isdigit():
                return Token('Integer', self.intVal())

            if self.current == '-' and self.expression[self.index + 1].isdigit():
                return Token('Integer', self.negativeInt())

            if self.current == '+':
                self.nextChar()
                return Token('Add', '+')

            if self.current == '-' and self.expression[self.index + 1].isspace():
                self.nextChar()
                return Token('Sub', '-')

            if self.current == '*':
                self.nextChar()
                return Token('Mul', '*')
            if self.current == '/':
                self.nextChar()
                return Token('Div', '/')
            if self.current == '%':
                self.nextChar()
                return Token('Mod', '%')

            #Removes white spaces
            if self.current.isspace():
                self.nextChar()
                continue

        return Token('EOF', None)

class BinOP(object):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right

class Num(object):
    def __init__(self, token):
        self.token = token
        self.value = token.value


#Parser Class:Reads the output from the Lexer and forms the AST
class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        # sets current token to the first token taken from the input
        self.current_token = self.lexer.exprToToken()

    def verifyType(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.exprToToken()
        else:
            raise Exception('Invalid Syntax')

    def factor(self):
        token = self.current_token
        if token.type == 'Integer':
            self.verifyType('Integer')
            return Num(token)

    def term(self):
        node = self.factor()

        while self.current_token.type in ('Mul','Div','Mod'):
            token = self.current_token #move to next tokens
            if token.type == 'Mul':
                self.verifyType('Mul')
            elif token.type == 'Div':
                self.verifyType('Div')
            elif token.type == 'Mod':
                self.verifyType('Mod')

            node = BinOP(left=node, op=token, right=self.factor())
        return node

    def expr(self):
        node = self.term()

        while self.current_token.type in ('Add','Sub'):
            token = self.current_token
            if token.type == 'Add':
                self.verifyType('Add')
            elif token.type == 'Sub':
                self.verifyType('Sub')

            node = BinOP(left=node, op=token, right=self.term())

        return node

    def parse(self):
        return self.expr()

# Interpreter:Converts AST into evaluated expression.

class NodeVisitor(object):
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))

class Interpreter(NodeVisitor):
    def __init__(self,parser):
        self.parser=parser

    def visit_BinOP(self,node):
        if node.op.type == 'Add':
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == 'Sub':
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == 'Mul':
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type == 'Div':
            return self.visit(node.left) / self.visit(node.right)
        elif node.op.type == 'Mod':
            return self.visit(node.left) % self.visit(node.right)

    def visit_Num(self, node):
        return node.value

    def interpret(self):
        tree = self.parser.parse()
        return self.visit(tree)

def main():
     while True:
         try:
             expr= input("")
             if expr=='q':
              break
         except EOFError:
             break
         tokens=Lexer(expr)
         parser=Parser(tokens)
         interpreter=Interpreter(parser)
         result=interpreter.interpret()
         print(str(result))

if __name__=="__main__":
  main()