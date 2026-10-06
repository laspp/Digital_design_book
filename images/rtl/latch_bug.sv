// What synthesis builds for an if without an else: y keeps its old value
// when sel is 0, which takes a latch. Written as always_latch so every tool
// accepts it; the same code inside always_comb infers the same latch.
module latch_bug (
    input  logic       sel,
    input  logic [3:0] in1,
    output logic [3:0] y
);
  always_latch begin
    if (sel) y = in1;
  end
endmodule
