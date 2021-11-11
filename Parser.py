from os import error
from Clause import NestedClause, Operations, Literal
from CNF import CNF, simplify_clause

def parse_operation(symbol):
    if symbol in ['~', '!', '¬']:
        return Operations.Negation
    elif symbol in ['|', '+', '∨']:
        return Operations.Disjuntion
    elif symbol in ['&', '*', '∧']:
        return Operations.Conjuntion
    elif symbol in ['->', '>', '=>']:
        return Operations.Implication
    elif symbol in ['<-', '<', '<=']:
        return Operations.LeftImplication
    elif symbol in ['<->', '<>', '<=>']:
        return Operations.Equivalent
    else:
        return None

def possible_operation(symbol):
    if parse_operation(symbol) is not None:
        return True
    elif symbol in ['-', '<', '=', '<-', '<=']:
        return True
    else:
        return False

def obtain_operation(right_raw_string):
    lim_idx = 0
    while lim_idx + 1 < len(right_raw_string) and possible_operation(right_raw_string[:lim_idx + 1]):
        lim_idx = lim_idx + 1
    
    operation_string = right_raw_string[:lim_idx]
    operation = parse_operation(operation_string)
    if operation is None:
        raise error(f'Parsing a operation fail "{operation_string}"')
    
    return operation, right_raw_string[lim_idx:]

def parse_raw_clause(raw_string):
    raw_string = raw_string.replace(' ', '')
    if len(raw_string) == 0:
        raise error('Empty literal')
    
    is_negation = parse_operation(raw_string[0]) == Operations.Negation
    if is_negation:
        raw_string = raw_string[1:]
        
    if raw_string[0] == '(':
        cnt_open = 0
        for idx_c, c in enumerate(raw_string):
            if c == '(':
                cnt_open = cnt_open + 1
            elif c == ')':
                cnt_open = cnt_open - 1
            if cnt_open == 0:
                idx = idx_c
                break
        if cnt_open > 0:
            raise error('Syntaxis error related to parentheses')
        if idx == 1:
            raise error(f'Empty left clause, remained raw string = "{raw_string}"')
        left_clause = parse_raw_clause(raw_string[1:idx])
        right_raw_string = raw_string[idx+1:]
    else:
        idx = len(raw_string)
        for idx_c, c in enumerate(raw_string):
            if possible_operation(c):
                idx = idx_c
                break
        if idx == 0:
            raise error(f'Empty left clause, remained raw string = "{raw_string}"')
        left_clause = Literal(raw_string[:idx])
        right_raw_string = raw_string[idx:]
    
    if is_negation:
        left_clause.neg = not left_clause.neg 
    
    if len(right_raw_string) == 0:
        return left_clause    
    else:
        operation, right_raw_clause = obtain_operation(right_raw_string)
        right_clause = parse_raw_clause(right_raw_clause)
        return NestedClause(left_clause, right_clause, operation)

def obtain_CNF(raw_string):
    nested_clause = parse_raw_clause(raw_string)
    return CNF(nested_clause)

if __name__ == '__main__':
    
    A_str = '!(!(!(Add * (s)) + B) => A) <= A'
    A = parse_raw_clause(A_str)
    A_simp = simplify_clause(A.copy())
    A_cnf = CNF(A)
    print(A_str)
    print(str(A))
    print(str(A_simp)) 
    print(str(A_cnf))