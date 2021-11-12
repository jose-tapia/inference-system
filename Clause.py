from os import error
from Format import *

class Literal:
    # Literal class
    def __init__(self, literal:str='', neg:bool=False):
        """
        Literal wrapper
        
        Args:
            - literal = Name of the literal
            - neg = Determine if its the negation of the literal
        """
        self.literal = literal
        self.neg = neg

    def __str__(self):
        return (Operations.Negation.value if self.neg else '') + self.literal

    def __eq__(self, literal):
        return isinstance(literal, Literal) and self.literal == literal.literal and self.neg == literal.neg

    def copy(self):
        return Literal(self.literal, self.neg)
    
    def complement(self):
        return Literal(self.literal, not self.neg)
    
    def simplify(self):
        return self.copy()

class Clause:
    def __init__(self, clauses=[], operation=Operations.Disjuntion, type=ClauseType.Clause):
        """
        Wrap a disjuntion or conjuntion of a list of clauses in CNF form
        
        Args:
            - clauses: List of clauses
            - operation: Indicates which operation is apply between clauses
        """
        self.clauses = clauses
        if operation == Operations.Disjuntion or operation == Operations.Conjuntion:
            self.operation = operation
        else:
            raise error(f'Operation not supported yet "{self.operation.name}"')
        self.type = type

    def __str__(self):
        if self.type == ClauseType.T or self.type == ClauseType.F:
            return self.type.value
        
        if len(self.clauses) == 0:
            return ''
        if len(self.clauses) == 1:
            return str(self.clauses[0])
        clauses_str = [str(clause) if isinstance(clause, Literal) or len(clause.clauses) == 1 else f'({str(clause)})' for clause in self.clauses]
        return f' {self.operation.value} '.join(clauses_str)
    
    def __eq__(self, clause):
        # Support comparison with literals
        if isinstance(clause, Literal):
            clause = Clause([clause])
        # No supported other comparisons for now
        if not isinstance(clause, Clause):
            return False
        
        if self.type != clause.type:
            return False
        if self.type != ClauseType.Clause:
            return True
        
        # If length of clauses are not equal, then the clauses are different
        if len(self.clauses) != len(clause.clauses):
            return False
        
        if len(self.clauses) > 1 and self.operation != clause.operation:
            return False
        
        # Compare Literals
        if len(self.clauses) == 1:
            return self.clauses[0] == clause.clauses[0]
        # Check that has the same elements
        for clause_int in self.clauses:
            if clause_int not in clause.clauses:
                return False
        return True
    
    def copy(self):
        if self.type != ClauseType.Clause:
            return Clause(type=self.type)
        clauses_copy = [clause.copy() for clause in self.clauses]
        return Clause(clauses_copy, self.operation)
    
    def complement(self):
        if self.operation == Operations.Disjuntion:
            operation_comp = Operations.Conjuntion
        else:
            operation_comp = Operations.Disjuntion

        clauses_comp = [clause.complement() for clause in self.clauses]
        if len(clauses_comp) == 1:
            operation_comp = Operations.Disjuntion
        return Clause(clauses_comp, operation_comp)
        
    def simplify(self):
        if self.type == ClauseType.T or self.type == ClauseType.F:
            return Clause(type=self.type)
        
        clauses_unique = []
        exists_complement = False
        exists_T = False
        exists_F = False
        for clause in self.clauses:
            if isinstance(clause, Clause) and clause.type != ClauseType.Clause:
                if clause.type == ClauseType.T:
                    exists_T = True
                elif clause.type == ClauseType.F:
                    exists_F = True                
            elif clause.complement() in self.clauses:
                exists_complement = True
            else:
                if clause not in clauses_unique:
                    clauses_unique.append(clause)
        if self.operation == Operations.Disjuntion:
            if exists_complement or exists_T:
                return Clause(type=ClauseType.T)
            return Clause(clauses_unique, Operations.Disjuntion)
        else:
            if exists_complement or exists_F:
                return Clause(type=ClauseType.F)
            return Clause(clauses_unique, Operations.Conjuntion)
                            
class NestedClause:
    def __init__(self, left_clause=Clause(), right_clause=Clause(), operation=Operations.Disjuntion, neg=False):
        """
        Clause class that support complex structures of clauses
        
        The structure of the clause is recurisvely defined as
            clause := (left_clause) operation (right_clause)
            
        As additional argument, neg indicates if is necessary to add a negation
        """
        self.left_clause = left_clause
        self.right_clause = right_clause
        self.operation = operation
        self.neg = neg
    
    def __str__(self):
        if isinstance(self.left_clause, Literal):
            left_str = str(self.left_clause)
        else:
            left_str = f'({str(self.left_clause)})'
        
        if isinstance(self.right_clause, Literal):
            right_str = str(self.right_clause)
        else:
            right_str = f'({str(self.right_clause)})'
        
        clause_str = f'{left_str} {self.operation.value} {right_str}'
        return f'{Operations.Negation.value}({clause_str})' if self.neg else clause_str
    
    def copy(self):
        return NestedClause(self.left_clause.copy(), self.right_clause.copy(), self.operation, self.neg)
    
    def complement(self):
        # Only works if all operations are disjuntions or conjuntions
        if self.operation == Operations.Disjuntion or self.operation == Operations.Conjuntion:
            left_clause_comp = self.left_clause.complement()
            right_clause_comp = self.right_clause.complement()
            
            if self.operation == Operations.Disjuntion:
                operation_comp = Operations.Conjuntion
            else:
                operation_comp = Operations.Disjuntion
                
            return NestedClause(left_clause_comp, right_clause_comp, operation_comp)            
        else:
            raise error(f'Operation not supported yet "{self.operation.name}"')
            
            