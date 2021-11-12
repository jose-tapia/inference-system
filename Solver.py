from InferenceSystem import satisfy_resolution
import argparse
import os

if __name__ == '__main__':    
    # Receive the filename via command line
    parser = argparse.ArgumentParser(
        description="Run certain propositional logic problem")
    parser.add_argument('problem_name_txt', metavar='problem_filename', type=str, nargs='?', default='example',
                        help='Name of the problem')
    
    # Retrieve problem filename
    args = parser.parse_args()
    file_name = args.problem_name_txt
    folder_name = 'problems'
    file_path = folder_name + '/' + file_name + '.txt'

    # Read problem file    
    hypotheses = []
    conclusions = []
    with open(file_path, 'r') as file:
        for line in file:
            
            line_splitted = line.replace('\n', '').replace(' ', '').split(':')
            if len(line_splitted) != 2:
                raise os.error(f'Syntaxis error in line "{line}"')
            if 'C' in line_splitted[0]:
                conclusions.append(line_splitted)
            else:
                hypotheses.append(line_splitted[1])
    
    # Per each conclusion, determine if it satisfy or not
    for conclusion in conclusions:
        print(f'Given the hypotheses, the conclussion {conclusion[0]} is {satisfy_resolution(hypotheses, conclusion[1], print_kb=True)}')