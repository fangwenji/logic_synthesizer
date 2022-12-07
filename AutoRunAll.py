from VerilogParser import vlg_parser
from LogicSynthesis import *
def AutoRunAll():
    tc1 = '~(!a | b)'
    tc2 = 'b | (b&c)'
    tc3 = 'a | !a & b'
    tc4 = '~(a&b)'
    tc5 = '!(c || d)'
    tc6 = 'a&b&c | (a&b&!d) | (a&b&~e)'

    test_case_list = [tc1, tc2, tc3, tc4, tc5, tc6]
    outfile_list = ['TestCase1', 'TestCase2', 'TestCase3', 'TestCase4', 'TestCase5', 'TestCase6']
    assert(len(test_case_list) == len(outfile_list))

    for idx in range(len(test_case_list)):
        print('-'*30)
        expr = test_case_list[idx]
        print('Input Expression:', expr)
        ast = vlg_parser(expr)
        print('AST:', ast)
        topname = outfile_list[idx]
        ls = LS(ast)
        ls.parseAST(ast)
        ls.write_verilog(topname)
        # print('-'*10)
        print('\n')

if __name__ == '__main__':
  AutoRunAll()