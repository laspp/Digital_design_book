// 4-bit counter, "next-state" style: the combinational logic computes
// count_next, and a plain register stores it.
module counter4_next (
    input  logic       clk,
    input  logic       reset,
    output logic [3:0] count
);
  logic [3:0] count_next;

  always_comb begin
    count_next = count + 1;
  end

  always_ff @(posedge clk) begin
    if (reset) count <= 4'b0000;
    else       count <= count_next;
  end
endmodule
