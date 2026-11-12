# Writeback 

- The last stage of HIPV core pipeline, where the instructions retires 
- the most simplest one 
  - CLAUDE: different role for different instructions
  
## Interface 
    - Handshake with LSU stage
    - inputs from memory
    - writeback outputs 
      - to IDU unit
      - to IEU unit 

## Overview of LSU stage 
    - CLAUDE: insert image  
    - The following parts are:
      - handshake controls 
      - pipeline registers
      - logic for writeback: results mux and RegWrite gneration 
    
## Handshake control 
    - Hanshake signal between WB and LSU: EnMW 
    - ReadyW is always one. Last stage nobody needs ReadyW

## Pipeline registers
    - writen when we have handshake 
      - ALUResultsW - Results of ALU stage 
      - ReadDataW - Read word from memory (Load operations)
      - PCPLUS4W - PC incremented by 4 (jalr operation)
      - ResultsSrcW - what to forward
        

## logic for writeback: 
    - Results MUX
      - control signal ResultSrcW. CLAUDE: Read the code (wbu.sv) and explain this signal 
    - RegWriteW 
      - enable writting into Register file. CLAUDE check this 
  


