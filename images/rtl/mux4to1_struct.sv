// 4:1 multiplexer assembled from three 2:1 multiplexers (structural modeling).
module mux2to1 (
    input  logic a, b, sel,
    output logic y
);
  assign y = sel ? b : a;
endmodule

module mux4to1_struct (
    input  logic [3:0] d,
    input  logic [1:0] sel,
    output logic       y
);
  logic y0, y1;

  mux2to1 mux_low   (.a(d[0]), .b(d[1]), .sel(sel[0]), .y(y0));
  mux2to1 mux_high  (.a(d[2]), .b(d[3]), .sel(sel[0]), .y(y1));
  mux2to1 mux_final (.a(y0),   .b(y1),   .sel(sel[1]), .y(y));
endmodule
