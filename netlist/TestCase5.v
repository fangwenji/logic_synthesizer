module TestCase5 (input c, input d, output t0);
  input c;
  input d;
  output t0;
  wire t0;
  NOR g0 (
    .A(c),
    .B(d),
    .Y(t0)
  );
endmodule
