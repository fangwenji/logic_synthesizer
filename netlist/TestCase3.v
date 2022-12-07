module TestCase3 (input a, input b, output t1);
  input a;
  input b;
  output t1;
  wire t0;
  wire t1;
  NOR g0 (
    .A(a),
    .B(b),
    .Y(t0)
  );
  NAND g1 (
    .A(t0),
    .B(1'b1),
    .Y(t1)
  );
endmodule
