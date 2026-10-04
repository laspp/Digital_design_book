// The same adder written with the + operator.
module adder4bit_plus (
    input  logic [3:0] a, b,
    output logic [3:0] sum,
    output logic       carry_out
);
  assign {carry_out, sum} = a + b;
endmodule
