"""
<(,->
<num,3>
<*,->
<num,2>
<),->
<+,->
<num,1>
<+,->
<num,2>
<+,->
<num,3>
"""


def convert2list(filename: str):
    with open(filename, "r") as f_lexical:
        lz = f_lexical.readlines()
        lz.pop(0)
        lz.pop()
        ret_lz = []
        for line in lz:
            string = line.split(',')[0]
            tmp_lz = list(string)
            tmp_lz.pop(0)
            symbol = ''.join(tmp_lz)
            ret_lz.append(symbol)
        return ret_lz


if __name__ == '__main__':
    ret = convert2list("lexical.out")
    print(ret)
