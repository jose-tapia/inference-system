from Clause import Clause, Literal, Operations, ClauseType
from Parser import obtain_CNF
from CNF import distributive_conjuntion

def resolve(left_cnf, right_cnf):
    if isinstance(left_cnf, Literal):
        left_cnf = Clause([left_cnf])
    
    if isinstance(right_cnf, Literal):
        right_cnf = Clause([right_cnf])
    
    if left_cnf.type != ClauseType.Clause or right_cnf.type != ClauseType.Clause:
        return None

    if left_cnf.operation == Operations.Conjuntion:
        if len(left_cnf.clauses) > 1:
            left_cnf = Clause([left_cnf])
        else:
            left_cnf.operation = Operations.Disjuntion
    
    if right_cnf.operation == Operations.Conjuntion:
        if len(right_cnf.clauses) > 1:
            right_cnf = Clause([right_cnf])
        else:
            right_cnf.operation = Operations.Disjuntion

    conjuntion_complement_left = 0
    complement_pairs_left = 0
    forgiven_clauses = []
    for clause in left_cnf.clauses:
        clause_comp = clause.complement().simplify()
        if isinstance(clause_comp, Clause) and clause_comp.operation == Operations.Conjuntion:
            clause_comp = distributive_conjuntion(clause_comp)
        if isinstance(clause_comp, Clause) and clause_comp.operation == Operations.Disjuntion:
            clauses_comp = clause_comp.clauses
        else:
            clauses_comp = [clause_comp]
        
        if all(clause_comp_ in right_cnf.clauses for clause_comp_ in clauses_comp):
            complement_pairs_left = complement_pairs_left + 1
            if len(clauses_comp) > 1:
                conjuntion_complement_left = conjuntion_complement_left + 1
            forgiven_clauses = forgiven_clauses + clauses_comp + [clause]
        
    
    conjuntion_complement_right = 0
    complement_pairs_right = 0
    for clause in right_cnf.clauses:
        clause_comp = clause.complement()
        if isinstance(clause_comp, Clause) and clause_comp.operation == Operations.Conjuntion:
            clause_comp = distributive_conjuntion(clause_comp)
        if isinstance(clause_comp, Clause) and clause_comp.operation == Operations.Disjuntion:
            clauses_comp = [clause_comp.clauses]
        else:
            clauses_comp = [clause_comp]
        
        if all(clause_comp_ in left_cnf.clauses for clause_comp_ in clauses_comp):
            complement_pairs_right = complement_pairs_right + 1
            if len(clauses_comp) > 1:
                conjuntion_complement_right = conjuntion_complement_right + 1
            forgiven_clauses = forgiven_clauses + clauses_comp + [clause]
    
    if complement_pairs_left + conjuntion_complement_right != 1 or complement_pairs_right + conjuntion_complement_left != 1:
        return None
    
    good_clauses = [clause for clause in left_cnf.clauses + right_cnf.clauses if clause not in forgiven_clauses]
    
    return Clause(good_clauses).simplify()

if __name__ == '__main__':
    A = 'R|P&Q'
    B = 'R|!(P&Q)'
    C = '!(Q|R)'
    
    A_cnf = obtain_CNF(A)
    B_cnf = obtain_CNF(B)
    C_cnf = obtain_CNF(C)
    print(A_cnf, B_cnf, C_cnf, sep='\n')
    
    res = resolve(A_cnf, B_cnf)
    print(res)