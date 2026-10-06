// Address decoder: one-hot slave select from the upper address bits, plus an
// error flag for unmapped addresses. Same logic as HIPV's obi_decoder, with
// the address map from hipv_soc_pkg written out as constants.
module addr_decoder (
    input  logic [31:0] Addr,
    output logic [4:0]  SlaveSel,
    output logic        DecErr
);
  always_comb begin
    SlaveSel = '0;                                     // default: nothing selected
    if (Addr[31:16] == 16'h0000)  SlaveSel[0] = 1'b1;  // instruction memory, 64 KiB
    if (Addr[31:16] == 16'h1000)  SlaveSel[1] = 1'b1;  // data memory, 64 KiB
    if (Addr[31:12] == 20'h20000) SlaveSel[2] = 1'b1;  // UART, 4 KiB
    if (Addr[31:12] == 20'h20001) SlaveSel[3] = 1'b1;  // timer, 4 KiB
    if (Addr[31:12] == 20'h20002) SlaveSel[4] = 1'b1;  // GPIO, 4 KiB
  end

  assign DecErr = ~|SlaveSel;
endmodule
