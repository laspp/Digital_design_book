# EXE unit

- This the heart of every CPU. It contains logic for performing the basic operation
  - CLAUDE: write some general thing about EXE stage that explain their aim and role and CPU. State that HIPV supports only RV32I, and list arithmetic operations and jumps that are handled here
## Interface of EXE unit. 
- We can divide into
    - Handshake signals with IDU
    - Signals produced in IDU stage. we can divide them into:
      - ALU operations
      - branches 
      - memwrite 
      - data operands registers, immediate and PC 
    - Forwarding data mechanism
      - from Mem stage 
      - from Wb stage 
      - control signals produced by hazzard unit
    - Feedback signals to Fetch and decode
      - PCSrcE, PCTargetE
    - To memory stage
      - Handshake signals 
      - outputs to memory stage

## Design of EXE unit

- Overview of EXE stage can be illustrated with bellow image
  - CLAUDE add diagram of EXE which you already generated

- Roughly we can divide the EXE stage in following parts:
  - Handshake logic and pipeline registers
  - Forwarding mechanism 
  - ALU unit 
  - Jump mechanism
  
## Handshake logic 

- Similar as in IDU without PSrcE
- CLAUDE: put explanation of involved signals here and set diagram simmilar for IDU stage 

- pipelin registers used to store outputs of IDU stage 
  - stored on the handshake between IDU and IEU stage

## Forwarding mechanism 

- Two muxes FWDAMUX and FWDBMUX
  - implemented as three way MUX
    - add code here 
  - data inputs:     
    - from D/E pipeline register 
    - from M stage
    - from E stage 
  - selection signal: 
    - Forward(A/B)E explain the enum type 

- Refreshing with forwarding values 
  - we can lose forwarded data if we rely on operands from IDU stage if the M stage stalls 
    - when M is not read 
    - when IEU stage has valid  
    - if would keep only stored operands from IDU stage we will lose the forwarded values 
  - Solution
    - feedback loop that stretches from the output of mux forwarding to the registers for pipeline
    - CLAUDE insert image HoldE.pdf and add correnspondig code in ieu.sv. The code should be first then say that this describes this thing
    - Explanatioon:
      - First mux rd1mux choses what will be saved in the rd1reg
        - EnDE = 1 the data from IDU stage is saved in the pipeline register
        - EnDE = 0 the data from the forwarding mux is saved in the pipeline register
        - Rationale: EnDE = 1 means that handshake between IDU and IEU stage is valid, so we can save the data from IDU stage. EnDE = 0 means that handshake is not valid, so we need to save the forwarded data to avoid losing it.
      - Register rd1reg is used to store the data from IDU stage or forwarded data. 
        - enable signals is active either the EnDE =1 or the HoldE is equal to 1
          - HoldE denotes that stage is in hold, it has valid instruction in it, however the mem stage is not valid 
          - CLAUDE: check how I labeled mem stage and used it across the chapter 
      - fwdamux
        - same mux described 
        - it also choses what will be stored value of rd1reg in case of holdE = 1:
          - either forwarded values from M or WB or previous instruction
- ALU stage
  - workhorse: CLAUDE add couple of details about the ALU in general 
  - Inputs 
    - A and B, obtained from mux that choses either:
      - SrcAE: FwdAE, PCE, 0 (for every input add corrensponding assembly)
      - SrcBE: WriteDatAE of extended immediate 
  - Output 
    - ALUResult E
  - Code:
    - CLAUDE: explain, connect with lab exercises 

- Jump mechanism 
  -  branchmp for conditional jumps
  -  generating PCsrcE
  -  producing jump adress PCTargetE 
  



  