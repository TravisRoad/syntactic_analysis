import util.util as util
"""
已经生成了FOLLOW和FIRST集合


{
    E -> E+T | E-T | T
    T -> T*F | T/F | F
    F -> (E) | num
}

change to

E  -> TE'
E' -> +TE'
E' -> -TE'
E' -> epsilon
T  -> FT'
T' -> *FT'
T' -> /FT'
T' -> epsilon
F -> (E) | num

|      |      First      |     Follow      |
| :--: | :-------------: | :-------------: |
|  E   |      (,num      |       $,)       |
|  E'  | +,-,epsilon |        $,)        |
|  T   |      (,num      | +,-,$,)|
|  T'  | *,/,epsilon | +,-,$,)|
|  F   |      (,num      | *,/,+,-,$,)|

"""


first_dict = {
    'E': ['(', 'num'],
    "E'": ['+', '-', r'\varepsilon'],
    'T': ['(', 'num'],
    "T'": ['*', '/', r'\varepsilon'],
    'F': ['(', 'num'],
    '(': ['('], 'num': ['num'], '+': ['+'], '-': ['-'], '*': ['*'], '/': ['/'], r'\varepsilon': [r'\varepsilon']
}

follow_dict = {
    'E': ['$', ')'],
    "E'": ['$', ')'],
    'T': ['+', '-', '$', ')'],
    "T'": ['+', '-', '$', ')'],
    'F': ['*', '/', '$', ')', '+', '-']
}

production_list = [
    {'E': ["T", "E'"]},
    {"E'": ["+", "T", "E'"]},
    {"E'": ["-", "T", "E'"]},
    {"E'": [r"\varepsilon"]},
    {'T': ["F", "T'"]},
    {"T'": ["*", "F", "T'"]},
    {"T'": ["/", "F", "T'"]},
    {"T'": [r"\varepsilon"]},
    {'F': ["(", "E", ")"]},
    {'F': ['num']}
]

non_terminated_symbols = ['E', "E'", "T", "T'", "F"]
terminated_symbols = ['+', '-', '*', '/', r'\varepsilon', '(', ')', 'num', '$']


def build_format(first: dict, follow: dict, production: list) -> dict:
    pre_analysis_format = dict()
    for dict_production in production:
        key = list(dict_production.keys())[0]
        if key not in pre_analysis_format.keys():
            pre_analysis_format[key] = {}
        first_symbol = dict_production[key][0]
        for a in first[first_symbol]:
            if a != r'\varepsilon':
                pre_analysis_format[key][a] = dict_production
            else:
                for b in follow[key]:
                    pre_analysis_format[key][b] = dict_production
    return pre_analysis_format


def output_format(pre_analysis_format: dict):
    lz = []
    print('|' + '|'.join(terminated_symbols) + '|')
    for a in terminated_symbols:
        lz.append(":-----:")
    print('|' + '|'.join(lz) + '|')
    lz.clear()
    for symbol in non_terminated_symbols:
        line = pre_analysis_format[symbol]
        for a in terminated_symbols:
            if a not in line.keys():
                lz.append('')
                continue
            right_part = line[a]
            lz.append(symbol + '->' + ''.join(right_part))
        print('|' + '|'.join(lz) + '|')
        lz.clear()


def output_result(input_lz: list, pre_analysis_format: dict):
    input_lz.append('$')
    stack = ['$', non_terminated_symbols[0]]
    output_lz = ['stack', 'input', 'output']
    print('|' + '|'.join(output_lz) + '|')
    output_lz = [':---', '---:', ':---:']
    print('|' + '|'.join(output_lz) + '|')
    while True:
        output_lz.clear()
        output_lz.append(''.join(stack))
        output_lz.append(''.join(input_lz))
        x = stack.pop()
        a = input_lz[0]
        production = {}
        if x in non_terminated_symbols:
            production = pre_analysis_format[x][a]
            string = ''.join(production[x])
            for ch in production[x][::-1]:
                if ch != r'\varepsilon':
                    stack.append(ch)
                else:
                    string = r'$\varepsilon$'
            output_lz.append(x + '->' + string)
        elif x in terminated_symbols:
            if x == a:
                input_lz.pop(0)
                output_lz.append(' ')
            else:
                print('error')
                return -1
        else:
            print('error')
            return -1
        print('|' + '|'.join(output_lz) + '|')
        if x == '$':
            break
    return 1


if __name__ == '__main__':
    ret = build_format(first_dict, follow_dict, production_list)
    output_format(ret)
    print(" ")
    output_result(util.convert2list('../util/lexical.out'), ret)
