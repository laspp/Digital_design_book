# Chapter 4 — SystemVerilog basics: outline

Working outline. Sections 1–3 were turned into the new chapter
`chapters/04-sv-basics.qmd` ("SystemVerilog Basics"); the remaining
sections stay in `chapters/05-sv-basics.qmd`. Not part of the book build.

**Sources**

- Old notes: `digital_design/04-IntrotoSV.md` (language history, HDLs)
- Lab text: `digital_design_lab/chapters/02-alu.qmd` (types, module, operators,
  `assign`, mux4to1, adder4bit)
- Current chapter: signals vs. variables, `always_comb`, `always_ff`, reset
  styles, "from syntax to the pipeline"

**Format convention (as in the current chapter):** every section has slide
bullets (`content-visible when-format="revealjs"`) and book prose
(`unless-format="revealjs"`). Figures marked 🛠 use the new pipelines.

---

## 1. Introduction to HDLs and SystemVerilog

### 1.1 Why a hardware description language

- Schematics stop scaling: a SoC has millions of gates, so we describe
  structure and behavior in text and let tools generate the netlist
- An HDL describes *hardware that exists concurrently*, not a program that
  runs (this is the "It looks like C. It isn't." slide already in the
  chapter, so move or reuse it here)
- Abstraction: say how the system operates without being consumed early by
  implementation details (quote from the old notes)

### 1.2 What HDLs are used for

One language, many levels (from the old notes):

- High-level behavioral modeling
- RTL (register-transfer level) modeling: **what this course writes**
- Gate- and transistor-level netlists
- Timing models for timing simulation
- Design verification (testbenches)

🛠 Suggested figure: abstraction ladder, behavioral → RTL → gate → transistor
(`images/blocks/abstraction.py` with schemdraw boxes, or a Graphviz diagram).

### 1.3 Simulation vs. synthesis

- The same source is used two ways: simulated (all constructs allowed) and
  synthesized (only a subset becomes hardware)
- Preview of the rule the rest of the chapter keeps returning to: if you
  can't picture the hardware, the synthesizer can't build it
- Point forward to the FPGA flow in chapter 3 (LUTs, flip-flops)

### 1.4 From Verilog to SystemVerilog

- Verilog introduced in 1984 for two purposes: modeling digital systems and
  writing testbenches
- Timeline table (from the old notes):

  | Standard | Year | Nickname |
  |---|---|---|
  | IEEE 1364-1995 | 1995 | Verilog-1995 |
  | IEEE 1364-2001 | 2001 | Verilog-2001 (RTL synthesis patch 1364.1-2002) |
  | IEEE 1364-2005 | 2005 | Verilog-2005, last Verilog standard |
  | IEEE 1800-2005 | 2005 | SystemVerilog-2005, extensions of Verilog-2005 |
  | IEEE 1800-2009, -2012, -2017, -2023 | | Each extends the previous one |

- Backward compatibility: a tool for SV-2005 accepts Verilog; a Verilog-2001
  tool rejects SV constructs
- What SV adds: design side (`logic`, `always_comb`/`always_ff`, enums,
  packed structs, interfaces) and verification side (assertions, OOP,
  constrained randomization, coverage)
- The old notes have a figure `img/04/sv_standard.png` (SV = hardware
  modeling + verification extensions of Verilog); redraw it or reuse it
- Scope of this course: a synthesizable subset only. Reasons: the whole
  language does not fit in a course, and the basics make new constructs
  easy to learn later

**Open question:** keep the 9-point "advantages of SystemVerilog" list that
is commented out in the lab text? Suggest a shortened 3-line version here,
since verification gets its own chapter (cocotb, chapter 8).

---

## 2. Basic SystemVerilog concepts

### 2.1 Anatomy of a module

- `module` … `endmodule`: the unit of hardware; hierarchy comes from
  instantiating modules inside modules
- ANSI-style port list: direction, type, optional width, name
- Port directions table: `input`, `output`, `inout` (with the one-line
  description of each from the lab text)
- Parameters in one line (`#(parameter W = 8)`), with a full treatment
  deferred
- Body: declarations, concurrent statements (`assign`, `always_*`),
  instances
- Comments (`//`, `/* */`) and naming conventions the book will use
  (`snake_case`, `_t` for types, `clk`/`rst` names)

Worked example, a small module with all parts labelled:

```systemverilog
module and_or (
    input  logic       a, b, c,
    output logic       y
);
  logic t;                 // internal signal
  assign t = a & b;
  assign y = t | c;
endmodule
```

🛠 Suggested figures: the same module as an RTL schematic
(`images/rtl/and_or.sv` → Yosys → netlistsvg), and an annotated "module as a
box with ports" drawing (`images/blocks/module_ports.py`).

### 2.2 Data types

**Value set (four-state logic)**

| Value | Meaning |
|---|---|
| `0` | logic low / false |
| `1` | logic high / true |
| `X` | unknown or conflicting |
| `Z` | high impedance (undriven, tri-state) |

- Where X comes from: uninitialized registers, two drivers disagreeing (link
  to the second `assign c = ...` example in section 3.1)
- Where Z comes from: tri-state buffers, undriven nets (link to the I/O block
  in chapter 3)
- 2-state vs. 4-state types: `bit` (0/1) vs. `logic` (0/1/X/Z)

🛠 Suggested figure: wave diagram of a net driven by two sources showing
`x`/`z` (`images/waves/xz.json`).

**Nets vs. variables**

- *Net* (`wire`): represents a physical connection; has no storage; its
  value is the resolved result of whatever drives it; driven by `assign` or
  a module output
- *Variable* (`logic`, `reg`, `int`, …): holds the last value assigned to
  it; written from procedural blocks
- `logic` is the SV unification: usable as either, with one rule: a
  `logic` may have only one driver (the compiler checks this); use `wire`
  where multiple drivers are legitimate (e.g. tri-state buses)
- Table: net vs. variable (storage, driven by, multiple drivers, typical
  keyword)
- Merge with the existing "Signals vs. variables" section. That section
  already says "a wire with memory", and the net/variable distinction should
  be stated precisely before it

> Caution for the lab text: it files `logic` under "Logic (NetList) Types"
> and again under "Variable Types". Fix this when porting: a `logic` is
> *not* a separate category, it is a data type that can sit on either side.

**Vectors and arrays**

- `logic [n-1:0]` packed vectors, bit-select `a[3]`, part-select `a[7:4]`
- Unsigned by default; `signed` keyword
- Mention packed vs. unpacked arrays in one slide, details later

**Integer and other types**

Table from the lab text, with an added column for synthesizability:

| Type | Width | Signed | States | Synthesizable |
|---|---|---|---|---|
| `bit` | 1 | no | 2 | yes |
| `logic` | 1 | no | 4 | yes |
| `byte` | 8 | yes | 2 | yes |
| `shortint` | 16 | yes | 2 | yes |
| `int` | 32 | yes | 2 | yes (loop indices, constants) |
| `longint` | 64 | yes | 2 | yes |
| `integer` | 32 | yes | 4 | legacy |
| `real` | 64 | n/a | n/a | **no** (simulation/testbench only) |

(Verify these cells against the standard before publishing.)

**`typedef`, `enum`, `struct packed`**: already in the current chapter;
decide whether they stay here or move to a later "Signals" section.

### 2.3 Constants and literals

- Literal syntax: `<size>'<base><value>`, with the four bases (`b`, `o`,
  `d`, `h`) and the examples from the lab text (all equal to decimal 10)
- Unsized literals and the width trap: `'1`, `'0`, `10` is a 32-bit signed
  decimal
- Underscores for readability: `16'hDEAD_BEEF`-style (use a 32-bit example)
- `x` and `z` in literals: `4'b10xz`
- Truncation and extension: `4'd20` loses bits, `-8'sd1` signed
- `parameter` vs. `localparam` vs. `` `define `` (one slide each)
- Exercise: write `8'b1100_1010` in hex, decimal, octal

---

## 3. Continuous assignment and operators

### 3.1 Continuous assignment: `assign`

- Definition: the right-hand side is evaluated continuously; the left-hand
  side is a net; models combinational logic
- It is **not** a statement that runs once. Keep the two examples from the
  lab text, they are the best teaching material in it:
  1. `assign b = a; assign c = b;` → synthesis removes `b`, giving
     `c = a` (order does not matter)
  2. `assign c = a; assign c = b;` → two drivers on one net → `X`
     whenever `a != b`. "Must be avoided at all costs"
- Tie back to chapter 1's "It looks like C. It isn't." slide
- Order independence: shuffle the lines and nothing changes

🛠 Suggested figure: wave diagram for example 2 showing `c` going to `x`
when `a` and `b` disagree (`images/waves/two_drivers.json`).

### 3.2 Operators

Organize by *what the operator returns*, since that is where beginners go
wrong. One slide each, with a code line and a result:

| Family | Operators | Result width |
|---|---|---|
| Arithmetic | `+ - * / %` | max of operand widths (watch carry) |
| Bitwise | `& \| ^ ~ ~^` | same as operands, bit by bit |
| Reduction | `& \| ^ ~& ~\| ~^` (unary) | 1 bit |
| Logical | `&& \|\| !` | 1 bit (true/false) |
| Relational | `== != < <= > >=` | 1 bit |
| Shift | `<< >> <<< >>>` | width of the left operand |
| Conditional | `? :` | width of the branches |
| Concatenation, replication | `{a,b}` `{n{a}}` | sum of parts |

**Key comparison slide: logical vs. bitwise.** For `a = 4'b1010`,
`b = 4'b0101`: `a & b` is `4'b0000`, but `a && b` is `1'b1`, since both
are non-zero. Most common beginner error; give it its own slide and
exercise.

- Logical operators (the topic named in the plan): `&&`, `||`, `!`; treat
  each operand as true/false; result is 1 bit; X propagation rules
- Equality: `==` vs. `===` (case equality, simulation only); X behaviour
- Reduction operators example: `&a`, `|a`, `^a` (parity!), tie to wide
  gates
- Operator precedence table (short), with the advice "use parentheses"
- Signed vs. unsigned in comparisons and shifts (`>>` vs. `>>>`)

> Fix when porting: the lab text has an unfinished `assign c` line in the
> relational example, and a typo `cc` in the conditional example.

### 3.3 Worked examples

1. **4-bit 4:1 mux** (`mux4to1`), nested conditional operator. Add the
   explanation bullets from the lab text, and contrast with the 2:1 mux
   `always_comb` version already in this chapter (@fig-mux2).
   🛠 RTL schematic from the real module.
2. **4-bit adder** (`adder4bit`), built from half- and full-adder equations
   with explicit carry wires. Then show the one-line version
   `assign {carry_out, sum} = a + b;` and let the synthesizer pick the
   structure.
   🛠 Side-by-side RTL schematics (gate-level equations vs. `+`).
3. Optional: small ALU slice that selects between `+`, `&`, `|`, `^` by an
   opcode, setting up the pipeline's EX stage later.

### 3.4 Where this leads

- Everything so far is combinational, built from `assign`
- Next sections (already written): `always_comb` for larger combinational
  descriptions, then `always_ff` for state
- One-line summary of the rule: `assign` / `always_comb` for logic,
  `always_ff` for registers

---

## Existing content: where it goes

| Current section | Proposed place |
|---|---|
| Goal for this week | Rewrite once the outline is final |
| It looks like C. It isn't. | 1.1 (or 3.1) |
| Signals vs. variables | Merge into 2.2 |
| `always_comb` | After section 3 (new section 4) |
| `always_ff` | New section 5 |
| Reset styles | New section 6 |
| From syntax to the pipeline | Stays last |

## Not covered here (decide scope)

- Lab-text parts on Vivado constraint files, switches and LEDs belong to
  the lab, not this chapter.
- Hierarchy/instantiation and `parameter` in detail: later chapter?
- Testbenches: chapter 8 (cocotb).

## Suggested order of work

1. Section 1 (mostly written in your old notes; needs polish)
2. Section 3.1 and 3.2 (the lab text is nearly complete)
3. Section 2 (needs the most new writing: nets vs. variables, literals)
4. Figures: abstraction ladder, `x`/`z` wave, RTL schematics for the
   examples
