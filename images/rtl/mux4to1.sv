// 4-bit 4:1 multiplexer built with a chain of conditional operators.
module mux4to1 (
    input  logic [3:0] in0, in1, in2, in3,
    input  logic [1:0] sel,
    output logic [3:0] out
);
  assign out = (sel == 2'b00) ? in0 :
               (sel == 2'b01) ? in1 :
               (sel == 2'b10) ? in2 :
                                in3;
endmodule
