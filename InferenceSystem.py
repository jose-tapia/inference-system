from Resolution import resolve
from Parser import obtain_CNF

def satisfy(hypothesis, conclusion, print_kb=False):
    hyp_cnf = [obtain_CNF(hyp) for hyp in hypothesis]
    conc_cnf = obtain_CNF(conclusion)
    
    if print_kb:
        cnt = 1
        for hyp in hyp_cnf:
            print(f'{cnt}: {hyp}')
            cnt = cnt + 1
    
    idx_A = 0
    while idx_A < len(hyp_cnf):
        idx_B = idx_A + 1
        N = len(hyp_cnf)
        while idx_B < N:
            resolution = resolve(hyp_cnf[idx_A], hyp_cnf[idx_B])
            if resolution not in hyp_cnf and resolution is not None:
                hyp_cnf.append(resolution)
                if print_kb:
                    print(f'{cnt}: {resolution}')
                    cnt = cnt + 1
                if resolution == conc_cnf:
                    return True
            idx_B = idx_B + 1
        idx_A = idx_A + 1
    return False    
        
if __name__ == '__main__':
    hypothesis = ['P|Q', 
                  'P=>R']
    conclusion = 'Q|R'
    print(satisfy(hypothesis, conclusion, True))