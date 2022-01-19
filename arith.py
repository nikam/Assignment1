# Code reference: https://ruslanspivak.com/lsbasi-part1/

# Token types
INTEGER, PLUS, MINUS, MUL, DIV, SPACE, EOF = 'INTEGER', 'PLUS', 'MINUS', 'MUL', 'DIV', 'SPACE', 'EOF'

# Token class
class Token():
    def __init__(self, type, value):
        self.type = type
        self.value = value


# Lexer
class Lexer():
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Error')

    # Skips the whitespaces in between
    def skip_whitespaces(self):
        while self.current_char is not None and self.current_char.isspace():
            self.next_character()

    # Returns the next character in the input string
    def next_character(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None  # Indicates end of input
        else:
            self.current_char = self.text[self.pos]

    # To get the multiple digit numbers
    def get_complete_integer(self):
        integer_value = ''
        while self.current_char is not None and self.current_char.isdigit():
            integer_value += self.current_char
            self.next_character()
        return int(integer_value)

    # Returns the next token
    def get_next_token(self):
        text = self.text

        if self.pos > len(text)-1:
            return Token(EOF, None)

        while self.current_char is not None:
            if self.current_char.isdigit():
                token = Token(INTEGER, self.get_complete_integer())
                return token
            if self.current_char.isspace():
                self.skip_whitespaces()
                continue
            if self.current_char == '+':
                token = Token(PLUS, self.current_char)
                self.next_character()
                return token
            if self.current_char == '-':
                token = Token(MINUS, self.current_char)
                self.next_character()
                # Handling the negative numbers
                if self.current_char.isdigit():
                    token = Token(INTEGER, -1*self.get_complete_integer())
                return token
            if self.current_char == '*':
                token = Token(MUL, self.current_char)
                self.next_character()
                return token
            if self.current_char == '/':
                token = Token(DIV, self.current_char)
                self.next_character()
                return token

            self.error()
        return Token(EOF, None)


# Parser --> Builds an AST

class OperationNode():
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

# Number node of the AST
class NumberNode():
    def __init__(self, token):
        self.token = token

class Parser():
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Error')

    # Processes the current token and returns the next token
    def eat(self, token_type):
        # print('eat:: token_type:', token_type)
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    # Evaluates to Number
    def eval_num(self):
        # print('Evaluating Number:', self.current_token.value)
        if self.current_token.type == INTEGER:
            num_node = NumberNode(self.current_token)
            self.eat(INTEGER)
        else:
            self.error()

        return num_node


    # Multiplication or Division

   
    def mul_div(self):
     

        node = self.eval_num()
        while self.current_token.type in (MUL, DIV):
            token = self.current_token
            if self.current_token.type == MUL:
                self.eat(self.current_token.type)

            elif self.current_token.type == DIV:
                self.eat(self.current_token.type)
           

            node = OperationNode(left = node, op = token, right = self.eval_num())

        return node

    # Computes the Addition or Subtraction
    def add_sub(self):

        # Setting the precedence
       
        node = self.mul_div()

        # print('computing addition/subtraction')
        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if self.current_token.type == PLUS:
                self.eat(self.current_token.type)
              
            elif self.current_token.type == MINUS:
                self.eat(self.current_token.type)
          

            node = OperationNode(left = node, op = token, right = self.mul_div())

        return node


# Interpreter
class Interpreter():
    def __init__(self, parserAST):
        self.parserAST = parserAST

    def error(self):
        raise Exception('Error')

    # Parsing the AST and calculating the value
    def interpret(self, node):
        # print('Interpret node: ', node.__class__.__name__)
        if node.__class__.__name__ == 'NumberNode':
            return node.token.value
        elif node.__class__.__name__ == 'OperationNode':
  
            if node.op.type == MUL:
                return (self.interpret(node.left) * self.interpret(node.right))
            elif node.op.type == DIV:
                return (self.interpret(node.left) / self.interpret(node.right))
            elif node.op.type == PLUS:
                return (self.interpret(node.left) + self.interpret(node.right))
            elif node.op.type == MINUS:
                return (self.interpret(node.left) - self.interpret(node.right))

    def calculate(self):
        return self.interpret(self.parserAST)


def main():
    while True:
        try:
            text = input()
   
        except EOFError:
            break
        if not text:
            continue

        lexer = Lexer(text)
        parser = Parser(lexer)
        ast = parser.add_sub()

        interpreter = Interpreter(ast)
        result = interpreter.calculate()
        print(result)

if __name__ == '__main__':
    main()







