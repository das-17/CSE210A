#References: https://lark-parser.readthedocs.io/en/latest/examples/indented_tree.html
#https://github.com/lark-parser/lark/blob/master/docs/json_tutorial.md
#https://renenyffenegger.ch/notes/development/languages/Python/libraries/Lark/index
#https://github.com/lark-parser/lark/issues/157
#https://lark-parser.readthedocs.io/en/latest/grammar.html
import sys
from lark import Lark

class Interpreter():
    def __init__(self):
        self.state = {}
    def evaluate(self, tree):
        #simple statements
        if tree.data == "simple":
            self.evaluate(tree.children[0])
            self.evaluate(tree.children[1])
            return
        #assignment statment:Eg:-x:=5
        elif tree.data == "assignment":
            self.state[tree.children[0].children[0]] = self.evaluate(tree.children[1])
            return
        
        #if-statement
        elif tree.data == "if":
            if self.evaluate(tree.children[0]):
                self.evaluate(tree.children[1])

            elif not self.evaluate(tree.children[0]) and len(tree.children) == 3:
                self.evaluate(tree.children[2])
            
            return 
        #Additional feature:ternary operation.Eg:-x=true?1:2
        elif tree.data == "ternary":
            var = tree.children[0].children[0]
            self.state[var] = self.evaluate(tree.children[2]) if self.evaluate(tree.children[1]) else self.evaluate(tree.children[3])
            return
        #simple-while statment
        elif tree.data == "simplewhile":
            if self.evaluate(tree.children[0]):
                self.evaluate(tree.children[1])
                self.evaluate(tree)
            
            elif not self.evaluate(tree.children[0]) and tree.children[1].data == "simple":
                self.evaluate(tree.children[1].children[1])
            return
        #comples-while statement with codeblock
        elif tree.data == "complexwhile":
            if self.evaluate(tree.children[0]):
                self.evaluate(tree.children[1])
                self.evaluate(tree)
            return
        #simple arithmatic operations:+,-,*,/,%
        elif tree.data in {"add", "sub", "mul", "div"}:
            Left = self.evaluate(tree.children[0])
            Right = self.evaluate(tree.children[1])
            
            if tree.data == 'add':
                return Left + Right
            
            elif tree.data == 'mul':
                return Left * Right
            
            elif tree.data == 'sub':
                return Left - Right
            
            elif tree.data == 'div':
                return round(Left / Right)

            elif tree.data == 'mod':
                return (Left % Right)    
        
        #comparison operators
        elif tree.data == "comparison":
            conditionaloperator = tree.children[1]
            Left = self.evaluate(tree.children[0])
            Right = self.evaluate(tree.children[2])
            if conditionaloperator =='<':
                return Left < Right
            elif conditionaloperator == "=":
                return Left == Right
            elif conditionaloperator == '>':
                return Left > Right
        #negation
        elif tree.data == "not":
            if not self.evaluate(tree.children[0]):
                return 1
            else:
                return 0
        #logic operators:and,or
        elif tree.data == "and":
            return self.evaluate(tree.children[0]) and self.evaluate(tree.children[1])
        
        elif tree.data == "or":
            return self.evaluate(tree.children[0]) or self.evaluate(tree.children[1])
           
       
        elif tree.data == "true_cond":
            return 1
        
        elif tree.data == "false_cond":
            return 0
        elif tree.data == "variable":
           if tree.children[0] in self.state:
                return self.state[tree.children[0]]
           else:
                return 0
        elif tree.data == "number":
           
                return int(tree.children[0])
        #skip condition  
        elif tree.data == "skip":
            return         



if __name__ == '__main__':
    parser= Lark.open("grammer.lark", parser='lalr')
    for input in sys.stdin:
        AST=parser.parse(input)
        #print(AST)
        interp=Interpreter()
        interp.evaluate(AST)
        store_output=""
        keys = interp.state.keys()
        for each in sorted(keys):
            if(store_output == ""):
              store_output = f"{each} → {interp.state[each]}"
            else:
              store_output += ", "+f"{each} → {interp.state[each]}"
        print("{" + store_output + "}")
         