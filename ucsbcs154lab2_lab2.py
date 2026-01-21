import pyrtl

### DECLARE WIRE VECTORS, INPUT, MEMBLOCK ###
instr = pyrtl.Input(bitwidth = 32, name = "instr")

op = pyrtl.WireVector(bitwidth=6, name='op')
rs = pyrtl.WireVector(bitwidth=5, name='rs')
rt = pyrtl.WireVector(bitwidth=5, name='rt')
rd = pyrtl.WireVector(bitwidth=5, name='rd')
sh = pyrtl.WireVector(bitwidth=5, name='sh')
func = pyrtl.WireVector(bitwidth=6, name='func')
imm = pyrtl.WireVector(bitwidth=16, name='imm')
addr = pyrtl.WireVector(bitwidth=26, name='addr')

rf = pyrtl.MemBlock(bitwidth = 32, addrwidth = 5, max_write_ports = 1, max_read_ports = 2) # only alu_out is trying to change data 
# readport< what is rt? 3
# addrwidth is 5 because 2^5 = 32 registers. 
# Each register has 32 bits so bitwidth is 32. 
data0 = pyrtl.WireVector(bitwidth = 32, name = "data0")
data1 = pyrtl.WireVector(bitwidth = 32, name = "data1")

data0 <<= rf[rt]
data1 <<= rf[rs]


alu_out = pyrtl.WireVector(bitwidth = 32, name = "alu_out")

### DECODE INSTRUCTION AND RETRIEVE RF DATA ###
op <<= instr[26:32]
rs <<= instr[21:26]
rt <<= instr[16:21]
rd <<= instr[11:16] 
sh <<= instr[6:11] 
func <<= instr[0:6]
imm <<= instr[0:17] 
addr <<= instr[0:26]  
### ADD ALU LOGIC HERE ###
# ADD, SUB, AND, OR, XOR, SLL, SRL, SRA, and SLT
with pyrtl.conditional_assignment:
    with func == 0x20: # ADD
        alu_out |= data0 + data1
    with func == 0x22: # SUB
        alu_out |= data1 - data0
    with func == 0x24: # AND
        alu_out |= data0 & data1
    with func == 0x25: # OR
        alu_out |= data0 | data1
    with func == 0x26: # XOR
        alu_out |= data0 ^ data1
    with func == 0x00: # SLL
        alu_out |= pyrtl.shift_left_logical(data0, sh)
    with func == 0x02: # SRL
        alu_out |= pyrtl.shift_right_logical(data0, sh)
    with func == 0x3: # SRA
        alu_out |= pyrtl.shift_right_arithmetic(data0, sh)
    with func == 0x2a: # SLT
        with pyrtl.signed_lt(data1, data0):
            alu_out |= 1
        with pyrtl.otherwise:
            alu_out |= 0
### WRITEBACK ###
rf[rd] <<= alu_out

# simulate

