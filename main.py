from VerilogParser import vlg_parser
from LogicSynthesis import *
def main():
    #======= Logic Expression Input ========
    expr = '~(!a | b)'
    outfile = 'TestCase'
    expr = 'a | ~a & b'



    #======= Logic Synthesis =========
    print('Input Expression:', expr)
    ast = vlg_parser(expr)
    print('AST:', ast)
    topname = outfile
    ls = LS(ast)
    ls.parseAST(ast)
    ls.write_verilog(topname)

if __name__ == '__main__':
  main()