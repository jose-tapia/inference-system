from enum import Enum
from os import error

class Operations(Enum):
    Negation = '¬'
    Disjuntion = '∨'
    Conjuntion = '∧'
    Implication = '=>'
    LeftImplication = '<='
    Equivalent = '<=>'

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

    def complement(self):
        return Literal(self.literal, not self.neg)

class Clause:
    def __init__(self, clauses=[], operation=Operations.Disjuntion):
        """
        Wrap a disjuntion or conjuntion of a list of clauses in CNF form
        
        Args:
            - clauses: List of clauses
            - operation: Indicates which operation is apply between clauses
        """
        self.clauses = clauses
        self.operation = operation
    
    def __str__(self):
        if len(self.clauses) == 0:
            return ''
        if len(self.clauses) == 1:
            return str(self.clauses[0])
        clauses_str = [f'({str(clause)})' for clause in self.clauses]
        return f' {self.operation.value} '.join(clauses_str)
    
    def __eq__(self, clause):
        # Support comparison with literals
        if isinstance(clause, Literal):
            clause = Clause([clause])
        # No supported other comparisons for now
        if not isinstance(clause, Clause):
            return False
        # If length of clauses are not equal, then the clauses are different
        if len(self.clauses) != len(clause.clauses):
            return False
        # Compare Literals
        if len(self.clauses) == 1:
            return self.clauses[0] == clause.clauses[0]
        # Check that has the same elements
        for clause in self.clauses:
            if clause not in clause.clauses:
                return False
        return True
    
    def complement(self):
        if self.operation == Operations.Disjuntion:
            self.operation = Operations.Conjuntion
        else:
            self.operation = Operations.Disjuntion

        self.clauses = [clause.complement() for clause in self.clauses]
            
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
        if self.neg:        
            return f'{Operations.Negation.value}(({str(self.left_clause)}) {self.operation.value} ({str(self.right_clause)}))'
        else:
            return f'({str(self.left_clause)}) {self.operation.value} ({str(self.right_clause)})'
        
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
            
            