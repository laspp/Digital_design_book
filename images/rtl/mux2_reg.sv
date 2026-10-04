// 2-to-1 mux feeding a register: the simplest piece of a pipeline stage.
module mux2_reg (
    input  logic       clk,
    input  logic       sel,
    input  logic [7:0] in0,
    input  logic [7:0] in1,
    output logic [7:0] q
);
  logic [7:0] y;

  always_comb begin
    if (sel) y = in1;
    else     y = in0;
  end

  always_ff @(posedge clk) q <= y;
endmodule
