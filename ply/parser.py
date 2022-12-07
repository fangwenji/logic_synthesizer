# -*- coding: utf-8 -*-
"""
Created on Fri Feb  5 16:03:59 2021

@author: E.T.R.A
@version: PLY 3.11
"""

#from ply import lex
#from ply.lex import TOKEN

import lex as lex

class Lexer(object):
    """Verilog lexer"""
    
    """def __init__(self):
        pass
    """
    keywords = ("ACCEPT_ON","ALIAS","ALWAYS","ALWAYS_COMB","ALWAYS_FF","ALWAYS_LATCH","AND","ASSERT","ASSIGN","ASSUME","ATTRIBUTE",
                "AUTOMATIC","BEFORE","BEGIN","BIND","BINS","BINSOF","BIT","BREAK","BUF","BUFIF0","BUFIF1","BYTE","CASE","CASEX",
                "CASEZ","CELL","CHANDLE","CHECKER","CLASS","CLOCKING","CMOS","CONFIG","CONST","CONSTRAINT","CONTEXT","CONTINUE",
                "COVER","COVERGROUP","COVERPOINT","CROSS","DEASSIGN","DEFAULT","DEFPARAM","DESIGN","DISABLE","DIST","DO","EDGE",
                "ELSE","END","ENDATTRIBUTE","ENDCASE","ENDCHECKER","ENDCLASS","ENDCLOCKING","ENDCONFIG","ENDFUNCTION","ENDGENERATE",
                "ENDGROUP","ENDINTERFACE","ENDMODULE","ENDPACKAGE","ENDPRIMITIVE","ENDPROGRAM","ENDPROPERTY","ENDSEQUENCE","ENDSPECIFY",
                "ENDTABLE","ENDTASK","ENUM","EVENT","EVENTUALLY","EXPECT","EXPORT","EXTENDS","EXTERN","FINAL","FIRST_MATCH","FOR","FORCE",
                "FOREACH","FOREVER","FORK","FORKJOIN","FUNCTION","GENERATE","GENVAR","GLOBAL","HIGHZ0","HIGHZ1","IF","IFF","IFNONE",
                "IGNORE_BINS","ILLEGAL_BINS","IMPLEMENTS","IMPLIES","IMPORT","INCDIR","INCLUDE","INITIAL","INOUT","INPUT","INSIDE",
                "INSTANCE","INT","INTEGER","INTERCONNECT","INTERFACE","INTERSECT","JOIN","JOIN_ANY","JOIN_NONE","LARGE","LET","LIBLIST",
                "LIBRARY","LOCAL","LOCALPARAM","LOGIC","LONGINT","MACROMODULE","MATCHES","MEDIUM","MODPORT","MODULE","NAND","NEGEDGE",
                "NETTYPE","NEW","NEXTTIME","NMOS","NOR","NOSHOWCANCELLED","NOT","NOTIF0","NOTIF1","NULL","OR","OUTPUT","PACKAGE","PACKED",
                "PARAMETER","PMOS","POSEDGE","PRIMITIVE","PRIORITY","PROGRAM","PROPERTY","PROTECTED","PULL0","PULL1","PULLDOWN","PULLUP",
                "PULSESTYLE_ONDETECT","PULSESTYLE_ONEVENT","PURE","RAND","RANDC","RANDCASE","RANDSEQUENCE","RCMOS","REAL","REALTIME",
                "REF","REG","REJECT_ON","RELEASE","REPEAT","RESTRICT","RETURN","RNMOS","RPMOS","RTRAN","RTRANIF0","RTRANIF1","SCALARED",
                "SEQUENCE","SHORTINT","SHORTREAL","SHOWCANCELLED","SIGNED","SMALL","SOFT","SOLVE","SPECIFY","SPECPARAM","STATIC","STRING",
                "STRONG","STRONG0","STRONG1","STRUCT","SUPER","SUPPLY0","SUPPLY1","SYNC_ACCEPT_ON","SYNC_REJECT_ON","S_ALWAYS","S_EVENTUALLY",
                "S_NEXTTIME","S_UNTIL","S_UNTIL_WITH","TABLE","TAGGED","TASK","THIS","THROUGHOUT","TIME","TIMEPRECISION","TIMEUNIT","TRAN",
                "TRANIF0","TRANIF1","TRI","TRI0","TRI1","TRIAND","TRIOR","TRIREG","TYPE","TYPEDEF","UNION","UNIQUE","UNIQUE0","UNSIGNED",
                "UNTIL","UNTIL_WITH","UNTYPED","USE","VAR","VECTORED","VIRTUAL","VOID","WAIT","WAIT_ORDER","WAND","WEAK","WEAK0","WEAK1",
                "WHILE","WILDCARD","WIRE","WITH","WITHIN","WOR","XNOR","XO")
    
    sys_funcs = ("$acos","$acosh","$asin","$asinh","$assertcontrol","$assertkill","$assertoff","$asserton","$assertpasson","$assertpassoff",
                 "$assertfailon","$assertfailoff","$assertnonvacuouson","$assertvacuousoff","$asyn","$an",
                 "$nan","$no","$o",
                 "$atan","$atan2","$atanh","$bits","$bitstoreal","$bitstoshortreal","$cast","$ceil","$changed_gclk",
                 "$changing_gclk","$clog2","$comment","$cos","$cosh","$countdrivers","$countones","$coverage_control","$coverage_get",
                 "$coverage_get_max","$coverage_merge","$coverage_save","$date","$dimensions","$display","$displayb","$displayh",
                 "$displayo","$dist_chi_square","$dist_erlang","$dist_exponential","$dist_normal","$dist_poisson","$dist_t",
                 "$dist_uniform","$dumpall","$dumpfile","$dumpflush","$dumplimit","$dumpoff","$dumpon","$dumpportsall","$dumpportsflush",
                 "$dumpportslimit","$dumpportsoff","$dumpportson","$dumpvars","$end","$enddefinitions","$error","$exit","$exp",
                 "$falling_gclk","$fatal","$fclose","$fdisplay","$fdisplayb","$fdisplayh","$fdisplayo","$fell","$fell_gclk","$feof",
                 "$ferror","$fflush","$fgetc","$fgets","$finish","$floor","$fmonitor","$fmonitorb","$fmonitorh","$fmonitoro","$fopen",
                 "$fread","$fscanf","$fseek","$fstrobe","$ftell","$fullskew","$future_gclk","$fwrite","$fwriteb","$fwriteh","$fwriteo",
                 "$getpattern","$get_coverage","$high","$history","$hold","$hypot","$increment","$incsave","$info","$input",
                 "$isunbounded","$isunknown","$itor","$key","$left","$list","$ln","$load_coverage_db","$log","$log10","$low","$monitor",
                 "$monitorb","$monitorh","$monitoro","$monitoroff","$monitoron","$nochange","$nokey","$nolog","$onehot","$onehot0",
                 "$past","$past_gclk","$period","$pow","$printtimescale","$q_add","$q_exam","$q_full","$q_initialize","$q_remove",
                 "$random","$readmemb","$readmemh","$realtime","$realtobits","$recovery","$recrem","$removal","$reset","$reset_count",
                 "$reset_value","$restart","$rewind","$right","$rising_gclk","$root","$rose","$rose_gclk","$rtoi","$sampled","$save",
                 "$scale","$scope","$setup","$setuphold","$set_coverage_db_name","$sformat","$sformatf","$shortrealtobits","$showscopes",
                 "$showvariables","$showvars","$signed","$sin","$sinh","$size","$skew","$sqrt","$sreadmemb","$sreadmemh","$sscanf",
                 "$stable","$stable_gclk","$steady_gclk","$stime","$stop","$strobe","$strobeb","$strobeh","$strobeo","$swrite","$syn",
                 "$system","$tan","$tanh","$tes","$plusargs","$time","$timeformat",
                 "$timescale","$timeskew","$typename","$typeof","$uandom","$ungetc","$unit","$unpacked_dimensions","$unsigned",
                 "$upscope","$urandom_range","$valu","$var","$vcdclose","$version","$warning","$width","$write","$writeb",
                 "$writeh","$writememb","$writememh")
    
    operators = (
        'PLUS','MINUS','TIMES','DIVIDE',
        'LPAREN','RPAREN','LBRACKET','RBRACKET','LBRACE','RBRACE')
    
    # temp for test
    temp = (
        'MODULE','ENDMODULE')
    
    # List of token names. This is always required
    tokens = operators + temp
    # keywords + sys_funcs + 
    
    # Regular expression rules for simple tokens
    t_MODULE = r'module'
    t_ENDMODULE = r'endmodule'
    t_PLUS	= r'\+'
    t_MINUS	= r'-'
    t_TIMES	= r'\*'
    t_DIVIDE	= r'/'
    t_LPAREN	= r'\('
    t_RPAREN	= r'\)'
    
    # Define a rule so we can track line numbers
    def t_newline(self,t):
        r'\n+'
        t.lexer.lineno += len(t.value)
    
    # A string containing ignored characters (spaces and tabs)
    t_ignore = ' \t'
    
    # Error handling rule
    def t_error(self,t):
        print("Errors - undefined!")
        t.lexer.skip(1)
    
    # Build the lexer
    def build(self,**kwargs):
        self.lexer = lex.lex(module=self,**kwargs)
        
if __name__ == '__main__':
    m = Lexer()
    m.build()
    m.lexer.input("module 3 + 4 endmodule")
    