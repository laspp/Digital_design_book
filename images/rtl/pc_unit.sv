// The program-counter loop of HIPV's fetch unit (ifu.sv), reduced to the three
// generic cells it is built from: next-PC mux, PC register, PC+4 adder.
// yosys: flatten
`include "mux2.sv"
`include "flopenr.sv"
`include "adder.sv"

module pc_unit (
    input  logic        clk, reset,
    input  logic        PCEnF,
    input  logic        PCSrcE,
    input  logic [31:0] PCTargetE,
    output logic [31:0] PCF
);
  logic [31:0] PCNextF, PCPlus4F;

  // next PC selection: sequential or redirect from Execute
  mux2 #(32)    pcmux(.D0(PCPlus4F), .D1(PCTargetE), .S(PCSrcE), .Y(PCNextF));

  // PC register
  flopenr #(32) pcreg(.clk(clk), .reset(reset), .en(PCEnF), .D(PCNextF), .Q(PCF));

  // sequential PC
  adder #(32)   pcadd4(.A(PCF), .B(32'd4), .Y(PCPlus4F));
endmodule
