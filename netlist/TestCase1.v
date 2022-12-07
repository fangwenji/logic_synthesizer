module TestCase1 (input a, input b, output t1);
  input a;
  input b;
  output t1;
  wire t0;
  wire t1;
  NAND g0 (
    .A(a),
    .B(1'b1),
    .Y(t0)
  );
  NOR g1 (
    .A(t0),
    .B(b),
    .Y(t1)
  );
endmodule
