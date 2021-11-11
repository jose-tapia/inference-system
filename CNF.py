from os import error
from Clause import Literal, Clause, NestedClause, Operations

def simplify_clause(clause):
    if isinstance(clause, NestedClause):
        if clause.neg:
            clause.neg = False
            simplified_clause = simplify_clause(clause)
            return simplified_clause.complement()
        
        elif clause.operation == Operations.Disjuntion or clause.operation == Operations.Conjuntion:
            clause.left_clause = simplify_clause(clause.left_clause)
            clause.right_clause = simplify_clause(clause.right_clause)
            return clause
        
        elif clause.operation == Operations.Implication:
            clause.left_clause = simplify_clause(clause.left_clause).complement()
            clause.right_clause = simplify_clause(clause.right_clause)
            clause.operation = Operations.Conjuntion
            return clause

        elif clause.operation == Operations.LeftImplication:
            clause.left_clause, clause.right_clause = clause.right_clause, clause.left_clause
            clause.operation = Operations.Implication
            return simplify_clause(clause)
        
        elif clause.operation == Operations.Equivalent:
            left_clause  = NestedClause(clause.left_clause, clause.right_clause, Operations.Implication)
            right_clause = NestedClause(clause.right_clause, clause.left_clause, Operations.Implication)
            equivalent_clause = NestedClause(left_clause, right_clause, Operations.Conjuntion)
            return simplify_clause(equivalent_clause)

        else:
            raise error(f'Operation not supported yet "{clause.operation.name}"')
    else:
        return clause


def distributive_conjuntion(clause):
    pass

def flat_clause(clause):
    pass 

def CNF(clause):
    """
    Given a nested clause, transform it to a CNF
    """
    clause_simplified = simplify_clause(clause) 
    return flat_clause(clause_simplified)   