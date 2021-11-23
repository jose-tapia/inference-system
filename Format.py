from enum import Enum

operations_list = ['Negation', 'Disjuntion', 'Conjuntion', 'Implication', 'LeftImplication', 'Equivalent']

# Format's type
operations_str = dict({
    'minimalist': {
        'Negation': '!',
        'Disjuntion': '+',
        'Conjuntion': '*',
        'Implication': '>',
        'LeftImplication': '<',
        'Equivalent': '<>'
    },
    'computer': {
        'Negation': '~',
        'Disjuntion': '|',
        'Conjuntion': '&',
        'Implication': '->',
        'LeftImplication': '<-',
        'Equivalent': '<->'
    },
    'mixed': {
        'Negation': '!',
        'Disjuntion': '|',
        'Conjuntion': '&',
        'Implication': '=>',
        'LeftImplication': '<=',
        'Equivalent': '<=>'
    },
    'formal': {
        'Negation': '¬',
        'Disjuntion': '∨',
        'Conjuntion': '∧',
        'Implication': '=>',
        'LeftImplication': '<=',
        'Equivalent': '<=>'
    }
})

# Conjuntion of all the format's type
all_symbols = dict()
for operation in operations_list:
    symbol_formats = []
    for format in operations_str:
        symbol_formats.append(operations_str[format][operation])
    all_symbols[operation] = symbol_formats

# Define the print format
print_format = 'formal'
class Operations(Enum):
    Negation = operations_str[print_format]['Negation']
    Disjuntion = operations_str[print_format]['Disjuntion']
    Conjuntion = operations_str[print_format]['Conjuntion']
    Implication = operations_str[print_format]['Implication']
    LeftImplication = operations_str[print_format]['LeftImplication']
    Equivalent = operations_str[print_format]['Equivalent']

# Clause, True, and False classes
class ClauseType(Enum):
    Clause = ''
    T = 'T'
    F = 'F'

# Hierarchy of logical operators
hierarchy_operators = ['Equivalent', 'Implication', 'LeftImplication', 'Conjuntion', 'Disjuntion', 'Negation']