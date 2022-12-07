module TestCase6 (input c, input a, input d, input e, input b, output t9);
  input c;
  input a;
  input d;
  input e;
  input b;
  output t9;
  wire t0;
  wire t1;
  wire t2;
  wire t3;
  wire t4;
  wire t5;
  wire t6;
  wire t7;
  wire t8;
  wire t9;
  NAND g0 (
    .A(a),
    .B(b),
    .Y(t0)
  );
  NAND g1 (
    .A(d),
    .B(1'b1),
    .Y(t1)
  );
  NAND g2 (
    .A(e),
    .B(1'b1),
    .Y(t2)
  );
  NAND g3 (
    .A(t0),
    .B(1'b1),
    .Y(t3)
  );
  NOR g4 (
    .A(c),
    .B(t1),
    .Y(t4)
  );
  NAND g5 (
    .A(t4),
    .B(1'b1),
    .Y(t5)
  );
  NOR g6 (
    .A(t5),
    .B(t2),
    .Y(t6)
  );
  NAND g7 (
    .A(t6),
    .B(1'b1),
    .Y(t7)
  );
  NAND g8 (
    .A(t3),
    .B(t7),
    .Y(t8)
  );
  NAND g9 (
    .A(t8),
    .B(1'b1),
    .Y(t9)
  );
endmodule
