from os import error
from Clause import Literal, Clause, NestedClause, Operations, ClauseType

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
            clause.operation = Operations.Disjuntion
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


def distributive_conjuntion(left_clause, right_clause):
    if isinstance(left_clause, Clause) and left_clause.type == ClauseType.F:
        return Clause(type=ClauseType.F)
    if isinstance(left_clause, Clause) and left_clause.type == ClauseType.T:
        return right_clause
    if isinstance(right_clause, Clause) and right_clause.type == ClauseType.F:
        return Clause(type=ClauseType.F)
    if isinstance(right_clause, Clause) and right_clause.type == ClauseType.T:
        return left_clause
    
    if isinstance(left_clause, Literal):
        if isinstance(right_clause, Literal):
            return Clause([left_clause, right_clause], Operations.Conjuntion)

        elif right_clause.operation == Operations.Conjuntion:
            return Clause([left_clause]+right_clause.clauses, Operations.Conjuntion)

        else:
            clauses_dist = [distributive_conjuntion(left_clause, clause).simplify() for clause in right_clause.clauses]
            return Clause(clauses_dist, Operations.Disjuntion)

    if isinstance(right_clause, Literal):
        return distributive_conjuntion(right_clause, left_clause)

    if left_clause.operation == Operations.Conjuntion:
        if right_clause.operation == Operations.Conjuntion:
            clauses_dist = left_clause.clauses + right_clause.clauses
            return Clause(clauses_dist, Operations.Conjuntion)
        
        else:
            clauses_dist = [distributive_conjuntion(left_clause, clause).simplify() for clause in right_clause.clauses]
            return Clause(clauses_dist, Operations.Disjuntion)
        
    else:
        clauses_dist = [distributive_conjuntion(clause, right_clause).simplify() for clause in left_clause.clauses]
        return Clause(clauses_dist, Operations.Disjuntion) 

def union_disjuntion(left_clause, right_clause):
    if isinstance(left_clause, Clause) and left_clause.type == ClauseType.T:
        return Clause(type=ClauseType.T)
    if isinstance(left_clause, Clause) and left_clause.type == ClauseType.F:
        return right_clause
    
    if isinstance(right_clause, Clause) and right_clause.type == ClauseType.T:
        return Clause(type=ClauseType.T)
    if isinstance(right_clause, Clause) and right_clause.type == ClauseType.F:
        return left_clause
    
    if isinstance(left_clause, Literal):
        if isinstance(right_clause, Literal):
            return Clause([left_clause, right_clause], Operations.Disjuntion)
        
        elif right_clause.operation == Operations.Disjuntion:
            return Clause([left_clause] + right_clause.clauses, Operations.Disjuntion)
        
        else:
            return Clause([left_clause, right_clause], Operations.Disjuntion)
    
    if isinstance(right_clause, Literal):
        return union_disjuntion(right_clause, left_clause)
    
    if left_clause.operation == Operations.Conjuntion:
        if right_clause.operation == Operations.Conjuntion:
            return Clause([left_clause, right_clause], Operations.Disjuntion)

        else:
            return Clause([left_clause] + right_clause.clauses, Operations.Disjuntion)
    
    else:
        if right_clause.operation == Operations.Conjuntion:
            return Clause(left_clause.clauses + [right_clause], Operations.Disjuntion)
        
        else:
            clauses_dist = left_clause.clauses + right_clause.clauses
            return Clause(clauses_dist, Operations.Disjuntion)                    

def flat_clause(clause):
    if isinstance(clause, NestedClause):
        left_clause = flat_clause(clause.left_clause)
        right_clause = flat_clause(clause.right_clause)
        if clause.operation == Operations.Disjuntion:
            result = union_disjuntion(left_clause, right_clause).simplify()
        elif clause.operation == Operations.Conjuntion:
            result = distributive_conjuntion(left_clause, right_clause).simplify()
        return result
    else:
        return clause
        
def CNF(clause):
    """
    Given a nested clause, transform it to a CNF
    """
    clause_simplified = simplify_clause(clause) 
    return flat_clause(clause_simplified)   

if __name__ == '__main__':
    
    a = Literal('a')
    b = Literal('b')
    na = Literal('a', True)
    A = NestedClause(a, b, Operations.Disjuntion)
    B = NestedClause(a, b, Operations.Conjuntion)
    C = NestedClause(a, b, Operations.Implication)
    D = NestedClause(a, b, Operations.Equivalent)
    
    #print(str(A), str(B), str(C), str(D), sep='\n')
    
    E = CNF(B)
    F = CNF(C)
    G = CNF(D)
    #print(str(G))
    print(str(E), str(F), str(G), sep='\n')