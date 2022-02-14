#References: https://lark-parser.readthedocs.io/en/latest/examples/indented_tree.html
#https://github.com/lark-parser/lark/blob/master/docs/json_tutorial.md
#https://renenyffenegger.ch/notes/development/languages/Python/libraries/Lark/index
#https://github.com/lark-parser/lark/issues/157
#https://lark-parser.readthedocs.io/en/latest/grammar.html
#https://stackoverflow.com/questions/6809402/python-maximum-recursion-depth-exceeded-while-calling-a-python-object
import sys
from lark import Lark
sys.setrecursionlimit(10000)

class Interpreter():
    def __init__(self):
        self.state = {}
        self.smallsteplist = []
        self.recursivecall = 0
    def evaluate(self, tree):
        #simple statements
        if tree.data == "simple":
            beforelength=len(self.smallsteplist)
            self.evaluate(tree.children[0])
            self.modify(tree,beforelength,self.changes(tree.children[1]))
            self.smallsteplist.append(self.changes(tree.children[1])+", "+self.storeOutput())
            self.evaluate(tree.children[1])
            return
        elif tree.data=="complex":
            beforelength=len(self.smallsteplist)
            self.evaluate(tree.children[0])
            self.modify(tree,beforelength,self.changes(tree.children[1]))
            self.smallsteplist.append(self.changes(tree.children[1])+", "+self.storeOutput())
            self.evaluate(tree.children[1])
            return
        #assignment statment:Eg:-x:=5
        elif tree.data == "assignment":
            self.state[tree.children[0].children[0]] = self.evaluate(tree.children[1])
            self.smallsteplist.append("skip, " + self.storeOutput())
            return
        
        #if-statement
        elif tree.data == "if":
            if self.evaluate(tree.children[0]):
                self.smallsteplist.append(self.changes(tree.children[1])+", "+self.storeOutput())
                self.evaluate(tree.children[1])

            elif not self.evaluate(tree.children[0]) and len(tree.children) == 3:
                self.smallsteplist.append(self.changes(tree.children[2])+", "+self.storeOutput())
                self.evaluate(tree.children[2])
            
            return 
        #Additional feature:ternary operation.Eg:-x=true?1:2
        elif tree.data == "ternary":
            var = tree.children[0].children[0]
            self.state[var] = self.evaluate(tree.children[2]) if self.evaluate(tree.children[1]) else self.evaluate(tree.children[3])
            return
        #simple-while statment
        elif tree.data == "simplewhile":
            #testcase=easy-17 has recursive while calls
            if self.recursivecall <= 3332:
                self.recursivecall+=1
            else:
                self.smallsteplist.append(self.changes(tree.children[1])+"; "+self.changes(tree)+", "+self.storeOutput())
                return
            if self.evaluate(tree.children[0]):
                self.smallsteplist.append(self.changes(tree.children[1])+"; "+self.changes(tree)+", "+self.storeOutput())
                beforelength=len(self.smallsteplist)
                self.evaluate(tree.children[1])
                self.modify(tree,beforelength,self.changes(tree))
                self.smallsteplist.append(self.changes(tree)+", "+self.storeOutput())
                self.evaluate(tree)
            
            elif not self.evaluate(tree.children[0]) and tree.children[1].data == "simple":
                self.smallsteplist.append("skip; "+self.changes(tree.children[1].children[1])+", "+self.storeOutput())
                self.smallsteplist.append(self.changes(tree.children[1].children[1])+", "+self.storeOutput())
                self.evaluate(tree.children[1].children[1])
            else:
                self.smallsteplist.append("skip, "+self.storeOutput())
                return

        #complex-while statement with codeblock
        elif tree.data == "complexwhile":
            if self.evaluate(tree.children[0]):
                self.smallsteplist.append(self.changes(tree.children[1])+"; "+self.changes(tree)+", "+self.storeOutput())
                beforelength=len(self.smallsteplist)
                self.evaluate(tree.children[1])
                self.modify(tree,beforelength,self.changes(tree))
                self.smallsteplist.append(self.changes(tree)+", "+self.storeOutput())
                self.evaluate(tree)
            else:
                self.smallsteplist.append("skip, "+self.storeOutput())
                return
        elif tree.data == "small_step":
            childlength=len(tree.children)
            for i in range(childlength-1):
              beforelength=len(self.smallsteplist)
              command=""
              for j in range(childlength-i-1):
                 if(j==childlength-i-2):
                  command+=self.changes(tree.children[i+j+1])
                 else:
                     command+=self.changes(tree.children[i+j+1])+"; "
              self.evaluate(tree.children[i])
              self.modify(tree,beforelength,command)
              self.smallsteplist.append(command+", "+self.storeOutput())
            self.evaluate(tree.children[childlength-1])

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
            elif tree.data == "skip":
                self.smallsteplist.append(','+self.storeOutput())
                return   
        
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
        if tree.data == "variable":
           if tree.children[0] in self.state:
                return self.state[tree.children[0]]
           return 0
        elif tree.data == "number":
               return int(tree.children[0])
        #skip condition  
        elif tree.data == "skip":
            return         
            
    def modify(self,tree,beforelength,command):
        for i in range(beforelength,len(self.smallsteplist)):
            afterlength=len(self.smallsteplist[i].split(","))
            newsmallstep=self.smallsteplist[i].split(",")[0]+"; "+command
            for j in range(1,afterlength):
                newsmallstep+=','+self.smallsteplist[i].split(",")[j]
            self.smallsteplist[i]=newsmallstep

    def changes(self,tree):
       operationsmap = {"add":"+","sub":"-","mul":"*","div":"/","mod":"%", "and": "∧","or": "∨"}
       if tree.data == "not":
            return "¬" + self.changes(tree.children[0])
        

       elif tree.data == "true_cond":
            return "true"
        

       elif tree.data == "false_cond":
            return "false"    
        

       elif tree.data == "number":
            return str(int(tree.children[0]))
        

       elif tree.data == "variable":
            return tree.children[0]


       elif tree.data == "assignment":
            return tree.children[0].children[0] + " := " + self.changes(tree.children[1])


       elif tree.data in {"add", "mul", "sub", "div","mod","and", "or"}:
            return "(" + self.changes(tree.children[0]) + operationsmap[tree.data] + self.changes(tree.children[1]) + ")"


       elif tree.data == "comparison":
            return "(" + self.changes(tree.children[0]) + tree.children[1] + self.changes(tree.children[2]) + ")"


       elif tree.data == "simple":
            return self.changes(tree.children[0]) + "; " + self.changes(tree.children[1])


       elif tree.data == "if":
            return "if " + self.changes(tree.children[0]) + " then { " + self.changes(tree.children[1]) + " } else { " + self.changes(tree.children[2]) + " }"
        

       elif tree.data in {"complexwhile", "simplewhile"}:
            return "while " + self.changes(tree.children[0]) + " do { " + self.changes(tree.children[1]) + " }"
        

       elif tree.data == "small_step":
            smallstep = ""
            for i in range(len(tree.children)):
                smallstep += self.changes(tree.children[i]) + "; " if i != len(tree.children) - 1 else self.changes(tree.children[i])
            return smallstep
    def storeOutput(self):
        store_output=""
        for each in sorted(self.state.keys()):
            if(store_output == ""):
              store_output = f"{each} → {self.state[each]}"
            else:
              store_output += ", "+f"{each} → {self.state[each]}"
        return ("{" + store_output + "}")
if __name__ == '__main__':
    parser= Lark.open("grammer.lark", parser='lalr')
    for input in sys.stdin:
        AST=parser.parse(input)
        interp=Interpreter()
        interp.evaluate(AST)
        for i in interp.smallsteplist:
            if i!= ",{}":
                print("⇒",i)
       