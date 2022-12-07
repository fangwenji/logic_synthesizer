module TestCase4 (input a, input b, output t0);
  input a;
  input b;
  output t0;
  wire t0;
  NAND g0 (
    .A(a),
    .B(b),
    .Y(t0)
  );
endmodule
