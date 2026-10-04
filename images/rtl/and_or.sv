// Smallest module with all parts: ports, an internal signal, two assigns.
module and_or (
    input  logic a, b, c,
    output logic y
);
  logic t;
  assign t = a & b;
  assign y = t | c;
endmodule
