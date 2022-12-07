import re, random

bool_one = "1\'b1"
bool_zero = "1\'b0"

class LS(object):
    def __init__(self, logic):
        self.free_var = set()
        self.sub_dic = {}
        self.origin_oper = ['band', 'bor', 'bnot', 'and', 'or', 'not']
        self.oper = ['NAND', 'NOR']
        self.temp_cnt = 0
        self.invar = set()
        self.outvar = ''
        self.gate_num = 0
        self.temp = 't'
        self.buffer = {}
    
    def isNOTCandidate(self, logic):
        if (logic[0] in ['bnot', 'not']) and len(logic) == 2:
            return True
        else:
            return False
    
    def isNOTExpr(self, logic):
        if (logic[0] == 'NAND') and len(logic) == 3 and ((logic[1] == bool_one) or (logic[2] == bool_one)):
            return True
        else:
            return False

    def isANDCandidate(self, logic):
        if (logic[0] in ['band', 'and']) and len(logic) == 3:
            return True
        else:
            return False

    def isORCandidate(self, logic):
        if (logic[0] in ['bor', 'or']) and len(logic) == 3:
            return True
        else:
            return False 

    def eliminateNOT(self, logic):
        
        expr = logic[1]
        result = ['NAND', expr, '1\'b1']

        return result

    def eliminateAND(self, logic):
        
        expr = ['NAND', logic[1], logic[2]]
        result = ['NAND', expr, '1\'b1']

        return result
    
    def eliminateOR(self, logic):
        
        expr = ['NOR', logic[1], logic[2]]
        result = ['NAND', expr, '1\'b1']

        return result
    

    def parseNOT(self, logic):
        if self.isNOTCandidate(logic):
            logic = self.eliminateNOT(logic)

        for i in range(1, len(logic)):
            if len(logic[i]) > 1:
                logic[i] = self.parseNOT(logic[i])

        return logic
    
    def parseAND(self, logic):
        if self.isANDCandidate(logic):
            logic = self.eliminateAND(logic)

        for i in range(1, len(logic)):
            if len(logic[i]) > 1:
                logic[i] = self.parseAND(logic[i])

        return logic
    
    def parseOR(self, logic):
        if self.isORCandidate(logic):
            logic = self.eliminateOR(logic)

        for i in range(1, len(logic)):
            if len(logic[i]) > 1:
                logic[i] = self.parseOR(logic[i])

        return logic
    

    def isTree(self, logic):
        if ((logic[0] in self.origin_oper) and (len(logic) in [2, 3])):
            return True
        else:
            return False

    def get_free_var(self, logic):
        if(not self.isTree(logic)):
            if(logic not in self.origin_oper):
                self.free_var.add(str(logic))
        else:
            for expr in logic:
                self.get_free_var(expr)
        
        return self.free_var

    def get_invar(self, logic):
        free_var = self.get_free_var(logic)
        for var in free_var:
            search_res = re.search(r'(\d)+\'(\S)+(\d)+', str(var))
            if(not search_res):
                self.invar.add(var)
        return self.invar
    
    def isNOT(self, logic):
        if (logic[0] == 'NAND')  and (logic[1] == bool_one):
            if(logic[2][0] == 'NAND')  and (logic[2][1] == bool_one):
                return True
            elif(logic[2][0] == 'NAND') and (logic[2][2] == bool_one):
                return True
            else:
                return False
        elif(logic[0] == 'NAND')  and (logic[2] == bool_one):
            if(logic[1][0] == 'NAND')  and (logic[1][1] == bool_one):
                return True
            elif(logic[1][0] == 'NAND')  and (logic[1][2] == bool_one):
                return True
            else:
                return False
        else:
            return False

    
    def simplify_not(self, logic):
        # if (self.isNOTExpr(logic)):
        #     if(self.isNOTExpr(logic[1])):
        #         result = logic[1][2]
        if (logic[0] == 'NAND')  and (logic[1] == bool_one):
            if(logic[2][0] == 'NAND')  and (logic[2][1] == bool_one):
                logic = logic[2][2]
            elif(logic[2][0] == 'NAND') and (logic[2][2] == bool_one):
                logic = logic[2][1]
        elif(logic[0] == 'NAND')  and (logic[2] == bool_one):
            if(logic[1][0] == 'NAND')  and (logic[1][1] == bool_one):
                logic = logic[1][2]
            elif(logic[1][0] == 'NAND')  and (logic[1][2] == bool_one):
                logic = logic[1][1]
          
        
        
        for i in range(1, len(logic)):
            if len(logic[i]) > 1:
                logic[i] = self.simplify_not(logic[i])


        return logic

    def gen_temp(self):
        while(self.temp in self.free_var):
            self.temp = ''.join(random.sample(['z','y','x','w','v','u','t','s','r','q','p','o','n','m','l','k','j','i','h','g','f','e','d','c','b','a'], 5))

    def find_key(self, logic):
        return [k for k,v in self.sub_dic.items() if v == logic]

    def substitute(self, logic):
        result = [logic[0], logic[1], logic[2]]
        temp_key = self.find_key(result)
        if(temp_key == []):
            temp_key = str(self.temp) + str(self.temp_cnt)
            self.temp_cnt = self.temp_cnt + 1
            self.sub_dic[temp_key] = result
            self.outvar = temp_key
        else:
            temp_key = temp_key[0]


        return temp_key
    
    def simplify_sub(self, logic):
        if (logic[0] in self.oper) and (logic[1][0] not in self.oper) and (logic[2][0] not in self.oper):
            logic = self.substitute(logic)

        for i in range(1, len(logic)):
            if len(logic[i]) > 1:
                logic[i] = self.simplify_sub(logic[i])
        return logic
    
    def optimizeBasic(self, logic):
        # 1 /\ X = X (X /\ 1 = X)
        if(logic[0] == 'and'):
            if(logic[1] == bool_one):
                logic = logic[2]
            elif(logic[2] == bool_one):
                logic = logic[1]
        # 1 \/ X = 1 (X \/ 1 = 1)
        if(logic[0] == 'or'):
            if((logic[1] == bool_one) or (logic[2] == bool_one)):
                logic = bool_one
        
        # 0 /\ X = 0 (X /\ 0 = 0)
        if(logic[0] == 'and'):
            if((logic[1] == bool_zero) or (logic[2] == bool_zero)):
                logic = bool_zero
        
        # 0 \/ X = X (X \/ 0 = X)
        if(logic[0] == 'or'):
            if(logic[1] == bool_zero):
                logic = logic[2]
            elif(logic[2] == bool_zero):
                logic = logic[1]
        
        # X /\ X = X, X \/ X = X
        if(logic[0] in ['and', 'or']) and (logic[1] == logic[2]):
            logic = logic[1]

        # X /\ ~X = 0 (~X /\ X = 0)
        if(logic[0] == 'and'):
            if(logic[1][0] == 'not') and (logic[1][1] == logic[2]):
                logic = bool_zero
            elif(logic[2][0] == 'not') and (logic[2][1] == logic[1]):
                logic = bool_zero
        
        # X \/ ~X = 1 (~X \/ X = 1)
        if(logic[0] == 'or'):
            if(logic[1][0] == 'not') and (logic[1][1] == logic[2]):
                logic = bool_one
            elif(logic[2][0] == 'not') and (logic[2][1] == logic[1]):
                logic = bool_one
        
        for i in range(1, len(logic)):
            if len(logic[i]) > 1:
                logic[i] = self.optimizeBasic(logic[i])
        return logic

    def isFactorble(self, logic):
        if(logic[0] == 'or') and (logic[1] == 'and') and (logic[2] == 'and'):
            if(logic[1][1] == logic[2][1]) or (logic[1][2] == logic[2][1]) \
                or (logic[1][1] == logic[2][2]) or (logic[1][2] == logic[2][2]):
                return True
        else:
            return False
    
    def optimizeFactor(self, logic):
        if(logic[0] == 'or'):
            if(logic[1][0] == 'and'):
                if(logic[2] == logic[1][1]):
                    logic = ['and', logic[2], ['or', bool_one, logic[1][2]]]
                elif(logic[2] == logic[1][2]):
                    logic = ['and', logic[2], ['or', bool_one, logic[1][1]]]
            elif(logic[2][0] == 'and'):
                if(logic[1] == logic[2][1]):
                    logic = ['and', logic[1], ['or', bool_one, logic[2][2]]]
                elif(logic[1] == logic[2][2]):
                    logic = ['and', logic[1], ['or', bool_one, logic[2][1]]]
        
        if(logic[0] == 'or'):
            if(logic[1][0] == 'and') and (logic[2][0] == 'and'):
                if(logic[1][1] == logic[2][1]):
                    logic = ['and', logic[1][1], ['or', logic[1][2], logic[2][2]]]
                elif(logic[1][2] == logic[2][1]):
                    logic = ['and', logic[1][2], ['or', logic[1][1], logic[2][2]]]
                elif(logic[1][1] == logic[2][2]):
                    logic = ['and', logic[1][1], ['or', logic[1][2], logic[2][1]]]
                elif(logic[1][2] == logic[2][2]):
                    logic = ['and', logic[1][2], ['or', logic[1][1], logic[2][1]]]


        
        for i in range(1, len(logic)):
            if len(logic[i]) > 1:
                logic[i] = self.optimizeFactor(logic[i])
        return logic
    
    def optimizeDistribute(self, logic):
        if(logic[0] == 'or'):
            if(logic[1][0] == 'and'):
                logic = ['and', ['or', logic[2], logic[1][1]], ['or', logic[2], logic[1][2]]]
            elif(logic[2][0] == 'and'):
                logic = ['and', ['or', logic[1], logic[2][1]], ['or', logic[1], logic[2][2]]]
        for i in range(1, len(logic)):
            if len(logic[i]) > 1:
                logic[i] = self.optimizeDistribute(logic[i])
        return logic

    def optimizeLogic(self, logic):
        logic = self.optimizeBasic(logic)
        logic = str(logic).replace('band', 'and')
        logic = str(logic).replace('bor', 'or') 
        logic = str(logic).replace('bnot', 'not')
        logic = eval(logic)
        logic = self.optimizeFactor(logic)
        logic = self.optimizeBasic(logic)
        logic = self.optimizeFactor(logic)
        logic = self.optimizeBasic(logic)
        logic = self.optimizeDistribute(logic)
        logic = self.optimizeBasic(logic)


        return logic

    
    def parseAST(self, logic):
            
        #For Empty logic
        if len(logic) == 0:
            return logic
        #For logic with one Literal
        if len(logic) == 1:
            return logic[0]

        self.invar = self.get_invar(logic)
        logic = self.optimizeLogic(logic)
        print(logic)

        result = self.parseNOT(logic)
        result = self.parseAND(result)
        result = self.parseOR(result)

        result = self.simplify_not(result)
        result = self.simplify_not(result)
        print('Logic Mapping: ', result)
        self.gen_temp()
        while(result[0] in self.oper):
            result = self.simplify_sub(result)
        if(self.sub_dic == {}):
            self.buffer[self.temp] = result
            self.outvar = self.temp

        
    def write_verilog(self, topname):
        with open('./netlist/' + str(topname)+ '.v', "w") as f:
            line1 = 'module ' + str(topname) + ' ('
            f.write(line1)
            for invar in self.invar:
                line1_in = 'input {0}, '.format(invar)
                f.write(line1_in)
            line1_out = 'output {0});\n'.format(self.outvar)
            f.write(line1_out)

            for invar in self.invar:
                line_invar = '  input {0};\n'.format(invar)
                f.write(line_invar)
            line_outvar = '  output {0};\n'.format(self.outvar)
            f.write(line_outvar)

            for key,val in self.sub_dic.items():
                line_wire = '  wire {0};\n'.format(key)
                f.write(line_wire)
            
            for key,val in self.sub_dic.items():
                line_g1 = '  ' + val[0] + ' g' + str(self.gate_num) + ' (\n'
                self.gate_num = self.gate_num + 1
                f.write(line_g1)
                line_gin1 = '    .A(' + val[1] + '),\n'
                f.write(line_gin1)
                line_gin2 = '    .B(' + val[2] + '),\n'
                f.write(line_gin2)
                line_gout = '    .Y(' + key + ')\n  );\n'
                f.write(line_gout)
            if(self.sub_dic == {}):
                line_assign = '  assign {0} = {1};\n'.format(self.temp, self.buffer[self.temp])
                f.write(line_assign)
            line_end = 'endmodule\n'
            f.write(line_end)



