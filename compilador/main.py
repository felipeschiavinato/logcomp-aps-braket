import sys
import re
from abc import ABC, abstractmethod
# from graphviz import Digraph


class FileWriter:
    data = []

    @staticmethod
    def write(string):
        FileWriter.data.append(string)

    @staticmethod
    def write_to_file(filename, start_line):
        """
        Writes each element of the list to the file, starting at the specified line number.
        If the file has fewer lines than the start_line, it will append the data to the end.
        """
        with open('program_frame.asm', 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # Insert the data at the specified line number
        for index, item in enumerate(FileWriter.data):
            lines.insert(start_line - 1 + index, item + "\n")

        with open(filename, 'w', encoding='utf-8') as f:
            f.writelines(lines)

class Node(ABC):
    unique_id = 0
    def __init__(self, value=None, children=None):
        self.value = value
        self.children = children if children is not None else []

        self.id = Node.unique_id  # Set this node's id
        Node.unique_id += 1  # Increment the class-wide unique id

    @abstractmethod
    def evaluate(self, symbol_table):
        pass

    def to_graphviz(self, graph=None):
        if graph is None:
            graph = Digraph(comment='AST')
        
        # Add the current node
        label_value = self.value if self.value is not None else self.__class__.__name__
        graph.node(str(self.id), label=str(label_value))
        
        for child in self.children:
            # Add an edge from the current node to each child
            
            graph.edge(str(self.id), str(child.id))
            
            # Recur to add each child's subtree
            child.to_graphviz(graph)
        
        return graph

class SymbolTable:
    def __init__(self):
        self.table = {}
        self.current_line_value = 4  # Initializing the column value
    
    def set(self, identifier, value, type_):
        if type_ not in ["int", "str", None]:
            raise Exception(f"Invalid type {type_}")
        # If the identifier is not in the table, set the current_line_value
        if identifier not in self.table:
            line_value = self.current_line_value
            self.current_line_value += 4  # Increment the column value
        else:
            line_value = self.table[identifier][2]  # Keep the old value if it already exists
        
        # Se o valor é None, apenas armazene o tipo e o valor None
        if value is None and identifier not in self.table:
            self.table[identifier] = (None, type_, line_value)
        else:
            if type_ is None:
                # Se a variável já existe e tem um tipo especificado
                if identifier in self.table:
                    declared_type = self.get_type(identifier)
                    if declared_type != value[1]:
                        raise Exception(f"Invalid type {value[1]} for variable {identifier}")
                    # Armazene o valor e o tipo
                    self.table[identifier] = (value[0], declared_type, line_value)
                else:
                    raise Exception(f"Variable {identifier} not defined")
            else:
                if identifier in self.table and (type_ != None or type_ != self.get_type(identifier)):
                    raise Exception(f"Variable {identifier} already defined")
                else:
                    self.table[identifier] = (value[0], type_, line_value)
    
    def get(self, identifier):
        if identifier not in self.table:
            raise Exception(f"Variable {identifier} not defined")
        # Return the tuple (value, type)
        return self.table[identifier]
    
    def get_value(self, identifier):
        if identifier not in self.table:
            raise Exception(f"Variable {identifier} not defined")
        return self.table[identifier][0]
    
    def get_type(self, identifier):
        if identifier not in self.table:
            raise Exception(f"Variable {identifier} not defined")
        return self.table[identifier][1]

class BinOp(Node):
    OPERATIONS = {
        'PLUS': lambda a, b: a + b,
        'MINUS': lambda a, b: a - b,
        'MULT': lambda a, b: a * b,
        'DIV': lambda a, b: a // b,
        'AND': lambda a, b: a and b,
        'OR': lambda a, b: a or b,
        'EQ': lambda a, b: a == b,
        'GT': lambda a, b: a > b,
        'LT': lambda a, b: a < b,
        'DOT': lambda a, b: str(a) + str(b)
    }

    def evaluate(self, symbol_table):
        operation = self.OPERATIONS.get(self.value)
        if operation is None:
            raise Exception(f"Invalid operation {self.value}")
        

        
        b = self.children[1].evaluate(symbol_table)
        writter.write(f'PUSH EAX')
        a = self.children[0].evaluate(symbol_table)
        
        writter.write(f'POP EBX')
        

        if (a[1] != b[1]) and self.value != "DOT":
            raise Exception(f"Invalid operation {self.value} between types {a[1]} and {b[1]}")

        
        op = operation(a[0], b[0])

        if op == True:
            op = 1
        elif op == False:
            op = 0
        else:
            op = op

        if self.value == "PLUS":
            writter.write(f'ADD EAX, EBX')

        elif self.value == "MINUS":
            writter.write(f'SUB EAX, EBX')
        elif self.value == "MULT":
            writter.write(f'IMUL EBX')
        elif self.value == "DIV":
            writter.write(f'CDQ')
            writter.write(f'IDIV EBX')
        elif self.value == "AND":
            # Convert EAX to boolean
            writter.write('TEST EAX, EAX')  # sets ZF flag if EAX is zero
            writter.write('SETNZ AL')       # AL = 1 if EAX was not zero, else AL = 0
            writter.write('AND EAX, 1')     # zero out all but lowest bit of EAX

            # Convert EBX to boolean
            writter.write('TEST EBX, EBX')  
            writter.write('SETNZ BL')       
            writter.write('AND EBX, 1')     

            # Perform boolean AND
            writter.write('AND EAX, EBX')   

        elif self.value == "OR":
            # Convert EAX to boolean
            writter.write('TEST EAX, EAX')  
            writter.write('SETNZ AL')       
            writter.write('AND EAX, 1')     

            # Convert EBX to boolean
            writter.write('TEST EBX, EBX')  
            writter.write('SETNZ BL')       
            writter.write('AND EBX, 1')     

            # Perform boolean OR
            writter.write('OR EAX, EBX')
        elif self.value == "EQ":
            writter.write(f'CMP EAX, EBX')
            writter.write(f'CALL binop_je')
        elif self.value == "GT":
            writter.write(f'CMP EAX, EBX')
            writter.write(f'CALL binop_jg')
        elif self.value == "LT":
            writter.write(f'CMP EAX, EBX')
            writter.write(f'CALL binop_jl')

        return (op, "int") if self.value != "DOT" else (op, "str")

class UnOp(Node):
    
    def evaluate(self, symbol_table):
        a = self.children[0].evaluate(symbol_table)
        if a[1] != "int":
            raise Exception(f"Invalid operation {self.value} on non-integer")
        if self.value == 'PLUS':
            return (a[0], "int")	
        elif self.value == 'MINUS':
            writter.write('NEG EAX')
            return (-a[0], "int")
        elif self.value == 'NOT':
            # Convert EAX to boolean 0 or 1
            writter.write('TEST EAX, EAX')  # sets ZF flag if EAX is zero
            writter.write('SETNZ AL')       # AL = 1 if EAX was not zero, else AL = 0
            writter.write('AND EAX, 1')     # zero out all but the lowest bit of EAX

            # Invert the boolean value
            writter.write('XOR EAX, 1')     # toggle the lowest bit (0 becomes 1, 1 becomes 0)
            return (not a[0], "int")

class IntVal(Node):
    def evaluate(self, symbol_table):
        writter.write(f'MOV EAX, {self.value}')
        return (self.value, "int")
    
class StringVal(Node):
    def evaluate(self, symbol_table):
        return (self.value, "str")
    
class NoOp(Node):
    def __init__(self):
        super().__init__()

    def evaluate(self, symbol_table):
        pass

class Identifier(Node):
    def __init__(self, value):
        super().__init__(value)

    def evaluate(self, symbol_table):
        writter.write(f'MOV EAX, [EBP-{symbol_table.table[self.value][2]}]')
        return symbol_table.get(self.value)

class Type(Node):
    def __init__(self, value):
        super().__init__(value)

    def evaluate(self, symbol_table):
        return self.value

class Assignment(Node):
    def __init__(self, children):
        super().__init__(children=children)

    def evaluate(self, symbol_table):
        identifier = self.children[0].value

        if self.children[1].__class__.__name__ == "NoOp":
            value = None
        else:
            child = self.children[1].evaluate(symbol_table)
            value = child
        
        if self.children[2].__class__.__name__ == "NoOp":
            type_ = None
        else:
            type_ = self.children[2].value


        if value == None:
            writter.write(f'PUSH DWORD 0')
        elif identifier not in symbol_table.table:
            writter.write(f'PUSH DWORD 0')
        else:
            writter.write(f'MOV [EBP-{symbol_table.table[identifier][2]}], EAX')

        symbol_table.set(identifier, value, type_)
        return value

class Block(Node):
    def __init__(self, children):
        super().__init__(children=children)

    def evaluate(self, symbol_table):
        for child in self.children:
            child.evaluate(symbol_table)

class Program(Node):
    def __init__(self, children):
        super().__init__(children=children)

    def evaluate(self, symbol_table):
        for child in self.children:
            child.evaluate(symbol_table)

class Print(Node):
    def __init__(self, children):
        super().__init__(children=children)

    def evaluate(self, symbol_table):
        value = self.children[0].evaluate(symbol_table)[0]
        # print(value)
        # writter.write(f'PUSH EAX')
        # # writter.write(f'PUSH formatout')
        # writter.write(f'CALL print')

        writter.write(f"PUSH EBX")
        writter.write(f"CALL println")
        writter.write(f"POP EBX")

class Scanln(Node):
    def evaluate(self, symbol_table):
        writter.write(f'PUSH scanint')
        writter.write(f'PUSH formatin')
        writter.write(f'CALL scanf')
        writter.write(f'ADD ESP, 8')
        writter.write(f'MOV EAX, DWORD [scanint]')
        return(int(input()), "int")


class PrePro:
    @staticmethod
    def filter(source):
        # Remove single-line comments
        source = re.sub(r'\/\/[^\n]*', '', source)

        if re.search(r'\d\s+\d', source):
            raise Exception('Ambiguous expression due to spaces between digits')
        return source

class IfStatement(Node):
    def __init__(self, children):
        super().__init__(children=children)
    def evaluate(self, symbol_table):

        condition = self.children[0]
        condition.evaluate(symbol_table)
        writter.write(f'CMP EAX, False')
        writter.write(f'JE ELSE_{self.id}')
        self.children[1].evaluate(symbol_table)
        writter.write(f'JMP ENDIF_{self.id}')
        writter.write(f'ELSE_{self.id}:')
        if len(self.children) == 3:
            self.children[2].evaluate(symbol_table)
        writter.write(f'ENDIF_{self.id}:')

        # condition = self.children[0].evaluate(symbol_table)[0]
        # if condition:
        #     self.children[1].evaluate(symbol_table)
        # else:
        #     if len(self.children) == 3:
        #         self.children[2].evaluate(symbol_table)

class ForLoop(Node):
    def __init__(self, children):
        super().__init__(children=children)
    def evaluate(self, symbol_table):
        self.children[0].evaluate(symbol_table)
        writter.write(f'LOOP_{self.id}:')
        self.children[1].evaluate(symbol_table)
        writter.write(f'CMP EAX, False')
        writter.write(f'JE EXIT_{self.id}')
        self.children[3].evaluate(symbol_table)
        self.children[2].evaluate(symbol_table)
        writter.write(f'JMP LOOP_{self.id}')
        writter.write(f'EXIT_{self.id}:')


class Token:
    def __init__(self, token_type, value):
        self.token_type = token_type
        self.value = value
        

class Tokenizer:

    RESERVED_WORDS = {
        'se': 'IF',
        'senao': 'ELSE',	
        'para': 'FOR',
        'Imprime': 'PRINTLN',
        'Entra': 'SCANLN',
        'inteiro': 'TINT',
        'variavel': 'VAR'
    }
    def __init__(self, source):
        self.source = source
        self.position = 0
        self.select_next()

    def select_next(self):
        

        if self.position >= len(self.source):
            self.next_token = Token(token_type='EOF', value=None)
            return

        char = self.source[self.position]
        while char == ' ' or char == '\t':
            self.position += 1
            if self.position >= len(self.source):
                self.next_token = Token(token_type='EOF', value=None)
                return
            char = self.source[self.position]
            
    
        if char == '+':
            self.next_token = Token(token_type='PLUS', value=None)
        elif char == '-':
            self.next_token = Token(token_type='MINUS', value=None)
        elif char == '.':
            self.next_token = Token(token_type='DOT', value=None)
        elif char == '*':
            self.next_token = Token(token_type='MULT', value=None)
        elif char == '/':
            self.next_token = Token(token_type='DIV', value=None)
        elif char == '(':
            self.next_token = Token(token_type='LPAREN', value=None)
        elif char == ')':
            self.next_token = Token(token_type='RPAREN', value=None)
        elif char == '=':
            if self.source[self.position + 1] == '=':
                self.position += 1
                self.next_token = Token(token_type='EQ', value=None)
            else:
                self.next_token = Token(token_type='ASSIGN', value=None)
        elif char == ';':
            self.next_token = Token(token_type='SEMICOLON', value=None)
        elif char == '{':
            self.next_token = Token(token_type='LBRACE', value=None)
        elif char == '}':
            self.next_token = Token(token_type='RBRACE', value=None)
        elif char == '&':
            if self.source[self.position + 1] == '&':
                self.position += 1
                self.next_token = Token(token_type='AND', value=None)
            else:
                raise Exception("Invalid syntax: expected &&")
        elif char == '|':
            if self.source[self.position + 1] == '|':
                self.position += 1
                self.next_token = Token(token_type='OR', value=None)
            else:
                raise Exception("Invalid syntax: expected ||")
        elif char == '!':
            self.next_token = Token(token_type='NOT', value=None)
        elif char == '>':
            self.next_token = Token(token_type='GT', value=None)
        elif char == '<':
            self.next_token = Token(token_type='LT', value=None)
        elif char == '\n':
            self.next_token = Token(token_type='NEWLINE', value=None)
        elif char == '"':
            string = ''
            self.position += 1
            while self.position < len(self.source) and self.source[self.position] != '"':
                string += self.source[self.position]
                self.position += 1
            if self.position >= len(self.source):
                raise Exception("Invalid syntax: expected closing quotation mark")
            self.next_token = Token(token_type='STRING', value=string)
        elif char.isdigit():
            number = char
            while self.position + 1 < len(self.source) and self.source[self.position + 1].isdigit():
                self.position += 1
                number += self.source[self.position]
            self.next_token = Token(token_type='INT', value=int(number))
        elif char.isalpha() or char == '_':
            identifier = char
            while self.position + 1 < len(self.source) and self.source[self.position + 1].isalnum() or self.source[self.position + 1] == '_':
                self.position += 1
                identifier += self.source[self.position]

            # Check if it is a reserved word or an identifier
            token_type = Tokenizer.RESERVED_WORDS.get(identifier, 'ID')

            if token_type == 'TINT':
                value = 'int'
            elif token_type == 'TSTRING':
                value = 'str'
            elif token_type == 'ID':
                value = identifier
            else:
                value = None
            
            self.next_token = Token(token_type=token_type, value=value)
        else:
            raise Exception(f'Invalid character encountered: {char}')
        

        self.position += 1

        


class Parser:

    @staticmethod
    def bool_expr(tokenizer):
        node = Parser.bool_term(tokenizer)
        while tokenizer.next_token.token_type in ['OR']:
            op_type = tokenizer.next_token.token_type
            tokenizer.select_next()
            node = BinOp(op_type, [node, Parser.bool_term(tokenizer)])
        return node

    def bool_term(tokenizer):
        node = Parser.rel_expr(tokenizer)

        while tokenizer.next_token.token_type in ['AND']:
            op_type = tokenizer.next_token.token_type
            tokenizer.select_next()
            node = BinOp(op_type, [node, Parser.rel_expr(tokenizer)])
        return node
    
    def rel_expr(tokenizer):
        node = Parser.parse_expression(tokenizer)
        while tokenizer.next_token.token_type in ['EQ', 'GT', 'LT']:
            op_type = tokenizer.next_token.token_type
            tokenizer.select_next()
            node = BinOp(op_type, [node, Parser.parse_expression(tokenizer)])
        return node

    @staticmethod
    def parse_statement(tokenizer):
        
        
        if tokenizer.next_token.token_type == 'VAR':
            tokenizer.select_next()
            if tokenizer.next_token.token_type != 'ID':
                raise Exception("Expected identifier")
            identifier = Identifier(tokenizer.next_token.value)
            tokenizer.select_next()
            if tokenizer.next_token.token_type == "TINT":
                type_ = Type(tokenizer.next_token.value)
            elif tokenizer.next_token.token_type == "TSTRING":
                type_ = Type(tokenizer.next_token.value)
            else:
                raise Exception("Invalid type or expected type")
            tokenizer.select_next()
            if tokenizer.next_token.token_type == 'NEWLINE':
                noop_node = NoOp()
                return Assignment([identifier, noop_node, type_])
            elif tokenizer.next_token.token_type == 'ASSIGN':
                tokenizer.select_next()
                value_node = Parser.bool_expr(tokenizer)
                return Assignment([identifier,value_node, type_])
            else:
                raise Exception("Expected newline or assignment operator")
        
        elif tokenizer.next_token.token_type == 'ID':
            identifier = Identifier(tokenizer.next_token.value)
            tokenizer.select_next()
            if tokenizer.next_token.token_type == 'ASSIGN':
                tokenizer.select_next()
                value_node = Parser.bool_expr(tokenizer)
                noop_node = NoOp()
                return Assignment([identifier, value_node, noop_node])
            else:
                raise Exception("Expected assignment operator")

        elif tokenizer.next_token.token_type == 'PRINTLN':
            tokenizer.select_next()
            if tokenizer.next_token.token_type == 'LPAREN':
                tokenizer.select_next()
                print_node = Print([Parser.bool_expr(tokenizer)])
                if tokenizer.next_token.token_type != 'RPAREN':
                    raise Exception('Missing closing parenthesis')
                tokenizer.select_next()
            else:
                raise Exception("Expected opening parenthesis")
            return print_node
        
        elif tokenizer.next_token.token_type == 'IF':
            tokenizer.select_next()

            condition = Parser.bool_expr(tokenizer)
            true_block = Parser.parse_block(tokenizer)
            
            false_block = None
            if tokenizer.next_token.token_type == 'ELSE':
                tokenizer.select_next()
                if tokenizer.next_token.token_type != 'LBRACE':
                    raise Exception("Expected opening brace for else block")
                
                false_block = Parser.parse_block(tokenizer)
                
            return IfStatement([condition, true_block, false_block] if false_block else [condition, true_block])

        elif tokenizer.next_token.token_type == 'FOR':
            tokenizer.select_next()
            init = Parser.parse_statement(tokenizer)
            
            if tokenizer.next_token.token_type != 'SEMICOLON':
                raise Exception("Expected semicolon in for statement")
            tokenizer.select_next()
            condition = Parser.bool_expr(tokenizer)
            
            if tokenizer.next_token.token_type != 'SEMICOLON':
                raise Exception("Expected semicolon in for statement")
            tokenizer.select_next()
            update = Parser.parse_statement(tokenizer)
            
            if tokenizer.next_token.token_type != 'LBRACE':
                raise Exception("Expected opening brace for for block")
            
            body = Parser.parse_block(tokenizer)
            
                  
            return ForLoop([init, condition, update, body])
        elif tokenizer.next_token.token_type == 'NEWLINE':
            tokenizer.select_next()
            return NoOp()

        else:
            print(tokenizer.next_token.token_type)
            raise Exception("Invalid statement")

    @staticmethod
    def parse_expression(tokenizer):
        node = Parser.parse_term(tokenizer)

        while tokenizer.next_token.token_type in ['PLUS', 'MINUS', 'DOT']:
            op_type = tokenizer.next_token.token_type
            tokenizer.select_next()
            node = BinOp(op_type, [node, Parser.parse_term(tokenizer)])

        return node

    @staticmethod
    def parse_term(tokenizer):
        node = Parser.parse_factor(tokenizer)

        while tokenizer.next_token.token_type in ['MULT', 'DIV']:
            op_type = tokenizer.next_token.token_type
            tokenizer.select_next()
            node = BinOp(op_type, [node, Parser.parse_factor(tokenizer)])

        return node

    @staticmethod
    def parse_factor(tokenizer):
        if tokenizer.next_token.token_type in ['MINUS', 'PLUS', 'NOT']:
            op_type = tokenizer.next_token.token_type
            tokenizer.select_next()
            node = UnOp(op_type, [Parser.parse_factor(tokenizer)])
        elif tokenizer.next_token.token_type == 'LPAREN':
            tokenizer.select_next()
            node = Parser.bool_expr(tokenizer)
            if tokenizer.next_token.token_type != 'RPAREN':
                raise Exception('Missing closing parenthesis')
            tokenizer.select_next()
        elif tokenizer.next_token.token_type == 'INT':
            node = IntVal(tokenizer.next_token.value)
            
            tokenizer.select_next()
        elif tokenizer.next_token.token_type == 'ID':
            node = Identifier(tokenizer.next_token.value)
            tokenizer.select_next()
           
        elif tokenizer.next_token.token_type == 'SCANLN':
            tokenizer.select_next()
            if tokenizer.next_token.token_type == 'LPAREN':
                tokenizer.select_next()
                scanln_node = Scanln()
                if tokenizer.next_token.token_type != 'RPAREN':
                    raise Exception('Missing closing parenthesis')
                tokenizer.select_next()
            else:
                raise Exception("Expected opening parenthesis")
            return scanln_node
        elif tokenizer.next_token.token_type == 'STRING':
            node = StringVal(tokenizer.next_token.value)
            tokenizer.select_next()
        else:
            raise Exception('Invalid syntax')

        return node

    @staticmethod
    def parse_block(tokenizer):
        statements = []
        if tokenizer.next_token.token_type != 'LBRACE':
            raise Exception("Expected opening brace")
        tokenizer.select_next()
        if tokenizer.next_token.token_type != 'NEWLINE':
            raise Exception("Expected newline after opening brace")
        
        while tokenizer.next_token.token_type not in ['EOF', 'RBRACE']:
            statements.append(Parser.parse_statement(tokenizer))

        tokenizer.select_next()
        if tokenizer.next_token.token_type != 'NEWLINE' and tokenizer.next_token.token_type != 'ELSE':
            raise Exception("Expected newline after closing brace")
        
            
        return Block(statements)
    
    def parse_program(tokenizer):
        statements = []
        while tokenizer.next_token.token_type != 'EOF':
            statements.append(Parser.parse_statement(tokenizer))
        return Program(statements)

            

    @staticmethod
    def run(source_str):
        source_str = PrePro.filter(source_str)
        tokenizer = Tokenizer(source_str)
        
        program = Parser.parse_program(tokenizer)

        if tokenizer.next_token.token_type != 'EOF':
            raise Exception('Invalid syntax')
        return program

if __name__ == '__main__':
    # ... (same as before)
    # Check for the correct number of command line arguments
    if len(sys.argv) < 2:
        print("Usage: python your_script.py <file_name>")
        sys.exit(1)


    file_name = sys.argv[1]

    # Check for the .go extension (optional)
    # if not file_name.endswith('.go'):
    #     print("The file should have a .go extension")
    #     sys.exit(1)

    try:
        # Open and read the file
        with open(file_name, 'r') as f:
            source_str = f.read()
    except FileNotFoundError:
        print(f"The file {file_name} was not found.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

    # Generate the AST and evaluate it
    writter = FileWriter()
    symbol_table = SymbolTable()
    ast = Parser.run(source_str)
    # graph = ast.to_graphviz()
    # graph.render('ast_graph', view=True)  # Saves to 'ast_graph.pdf' and opens it
    ast.evaluate(symbol_table)
    file_name = file_name.replace('.go', '')
    writter.write_to_file(f'{file_name}.asm', 145)