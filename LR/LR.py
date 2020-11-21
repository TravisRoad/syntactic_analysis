import util.util as util

production_list = [
    {'S': ['E']},
    {'E': ["E", '+', "T"]},
    {"E": ["E", '-', "T"]},
    {"E": ["T"]},
    {'T': ["T", '*', "F"]},
    {"T": ["T", "/", "F'"]},
    {"T": ["F"]},
    {'F': ["(", "E", ")"]},
    {'F': ['num']}
]

action_list = [
    {'(': 'S4', 'num': 'S5'},  # 0
    {'+': 'S8', '-': 'S9', '$': 'ACC'},
    {'+': 'R3', '-': 'R3', ')': 'R3', '*': 'S10', '/': 'S11', '$': 'R3'},
    {'+': 'R6', '-': 'R6', ')': 'R6', '*': 'R6', '/': 'R6', '$': 'R6'},
    {'(': 'S4', 'num': 'S5'},  # 4
    {'+': 'R8', '-': 'R8', ')': 'R8', '*': 'R8', '/': 'R8', '$': 'R8'},
    {')': 'S7', '+': 'S8', '-': 'S9'},
    {'+': 'R7', '-': 'R7', ')': 'R7', '*': 'R7', '/': 'R7', '$': 'R7'},
    {'(': 'S4', 'num': 'S5'},  # 8
    {'(': 'S4', 'num': 'S5'},
    {'(': 'S4', 'num': 'S5'},
    {'(': 'S4', 'num': 'S5'},
    {')': 'R4', '+': 'R4', '-': 'R4', '$': 'R4'},  # 12
    {')': 'R5', '+': 'R5', '-': 'R5', '$': 'R5'},
    {'+': 'R1', '-': 'R1', ')': 'R1', '*': 'S10', '/': 'S11', '$': 'R1'},
    {'+': 'R2', '-': 'R2', ')': 'R2', '*': 'S10', '/': 'S11', '$': 'R2'}
]

goto_list = [
    {'E': 1, 'T': 2, 'F': 3},  # 0
    {},
    {},
    {},
    {'E': 6, 'T': 2, 'F': 3},  # 4
    {},
    {},
    {},
    {'T': 14, 'F': 3},  # 8
    {'E': 1, 'T': 5},
    {'F': 12},
    {'F': 13},
    {},
    {},
    {},
    {}
]

pre_analysis_format = (action_list, goto_list)
non_terminated_symbols = ['E', "T", "F"]
terminated_symbols = ['(', ')', '+', '-', '*', '/', 'num', '$']


def output_pre_analysis_list():
    line_num = 16
    i = 0
    col_num = len(non_terminated_symbols) + len(terminated_symbols)
    print('|index|' + '|'.join(terminated_symbols) + '|' + '|'.join(non_terminated_symbols) + '|')  # header
    lz = ['|'] * (col_num + 2)
    print(':---:'.join(lz))
    while i < line_num:
        lz.clear()
        lz.append(str(i))
        for symbol in terminated_symbols:
            if symbol in action_list[i]:
                lz.append(action_list[i][symbol])
            else:
                lz.append(' ')
        for symbol in non_terminated_symbols:
            if symbol in goto_list[i]:
                lz.append(str(goto_list[i][symbol]))
            else:
                lz.append(' ')
        print('|' + '|'.join(lz) + '|')
        i += 1


def generate_output_format(input_lz: list):
    state_stack = ['0']
    symbol_stack = []
    input_lz.append('$')
    ret_lz = []
    while True:
        state = int(state_stack[-1])
        symbol = input_lz[0]
        dic = action_list[state]
        output_string = ''
        state_stack_output = ' '.join(state_stack)
        symbol_stack_output = ' '.join(symbol_stack)
        input_lz_output = ''.join(input_lz)
        if symbol in dic.keys():
            string = dic[symbol]
            tmp_lz = list(string)
            if tmp_lz[0] == 'S' or tmp_lz[0] == 's':
                tmp_lz.pop(0)
                state_stack.append(''.join(tmp_lz))  # shift the state
                symbol_stack.append(input_lz.pop(0))  # shift the input string
                output_string = 'shift ' + ''.join(tmp_lz)
            elif tmp_lz[0] == 'R' or tmp_lz[0] == 'r':  # start with R
                tmp_lz.pop(0)
                production_index = int(''.join(tmp_lz))
                production = production_list[production_index]
                for key in production:
                    length = len(production[key])
                    for i in range(0, length):
                        state_stack.pop()
                        symbol_stack.pop()
                    state = int(state_stack[-1])
                    symbol_stack.append(key)
                    state_stack.append(str(goto_list[state][key]))
                    output_string = key + '->' + ''.join(production[key])
            elif action_list[state][symbol] == 'ACC':
                lz = [state_stack_output, symbol_stack_output, input_lz_output, 'ACC']
                ret_lz.append(lz)
                break
        else:
            print("error")
            return ret_lz
        lz = [state_stack_output, symbol_stack_output, input_lz_output, output_string]
        ret_lz.append(lz)
    return ret_lz


def output(output_format: list):
    lz = ['状态栈<br>符号栈', '输入', '输出']
    print('|' + '|'.join(lz) + '|')
    print('|:----|-----:|:----:|')
    for line in output_format:
        lz = [line[0] + '<br>   ' + line[1], line[2], line[3]]
        print('|' + '|'.join(lz) + '|')


if __name__ == '__main__':
    output_pre_analysis_list()
    # ret = generate_output_format(util.convert2list(r'../util/lexical.out'))
    ret = generate_output_format(util.convert2list('../util/lexical.out'))
    print("hello")
    output(ret)
