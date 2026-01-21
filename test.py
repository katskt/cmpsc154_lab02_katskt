import pyrtl

mem = pyrtl.MemBlock(bitwidth=8, addrwidth=2)

# Write to each address, starting from address 1.
write_addr = pyrtl.Register(name="write_addr", bitwidth=2, reset_value=1)
write_addr.next <<= write_addr + 1

mem[write_addr] <<= write_addr + 10  # Creates a write port.

# Read from each address, starting from address 0.
read_addr = pyrtl.Register(name="read_addr", bitwidth=2)
read_addr.next <<= read_addr + 1

read_data = pyrtl.Output(name="read_data")
read_data <<= mem[read_addr]  # Creates a read port.

sim = pyrtl.Simulation()
sim.step_multiple(nsteps=6)
sim.tracer.trace["write_addr"]

sim.tracer.trace["read_addr"]

sim.tracer.trace["read_data"]
