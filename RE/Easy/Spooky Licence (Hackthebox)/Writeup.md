This challenge was proposed during cyberapocalypse 2023 and was an easy reversing challenge. 

First, let's fire up the challenge in Ghidra to see what we'll deal with : 

![Ghidra](/Images/Ghidra.png)

We can first see that the input should be 32 characters long and than then a lots of checks are made on the input.
This is a perfect challenge for angr (or Z3)

Once you know some basics of angr, this challenge becomes pretty easy. Here's a breakdown of the script : 

```python
project = angr.Project("./spookylicence",main_opts={'base_addr' : base_address}, load_options={'auto_load_libs': False},)
```

We first load the binary into an angr project. We specify the base address and we also specify that we don't want to load the libraries because we don't need them.

```python
known_flag = "HTB{"
flag_length = 32
known_chars=[claripy.BVV((known_flag[i])) for i in range(len(known_flag))]
flag_chars = [claripy.BVS(f"flag_{i}",8) for i in range(flag_length-len(known_flag))]
flag = claripy.Concat(*known_chars+flag_chars)
```
The more info we'll give to angr, the faster it'll find the solution. So here we can exploit the fact that we know the beginning of the flag and also the length of it. 

```python
base_address = 0x00100000
avoid_address = 0x100000+0x1890
good_address = 0x100000+0x187d
```
We also know that the flag is good if the program reaches the address 0x100000+0x187d and that it's bad if it reaches the address 0x100000+0x1890. These address correspond to the print of "License Correct" and "License Invalid".

```python
state=project.factory.full_init_state(args=["./spookylicence",flag], add_options={angr.sim_options.ZERO_FILL_UNCONSTRAINED_REGISTERS,angr.sim_options.ZERO_FILL_UNCONSTRAINED_MEMORY})
```
We then create a state with the binary and the flag as arguments. We also specify that we want to fill the unconstrained registers and memory with zeros. This is a good practice to avoid some errors.

```python
for i in range(4, 32):
    state.solver.add(flag.get_byte(i) >= 33)
    state.solver.add(flag.get_byte(i) <= 125)
```

We finally add the last constraints on the flag. We know that the flag is composed of printable characters so we add this constraint.

```python
sm = project.factory.simulation_manager(state)

sm.explore(find = good_address, avoid = avoid_address)
if(len(sm.found)>0):
	print(sm.found[0].solver.eval(flag,cast_to=bytes))
else:
	print("Not found :(")
```

The last step is to create a simulation manager and we tell it to find the good address and to avoid the bad address. If the simulation manager finds a solution, we print it, otherwise we print "Not found :(".

We can know run the script and get the flag in less than one second ! 

Here's the complete script : 

```python
import angr
import claripy

#For base_address, try to find an address below the fgets or the code which read our input
base_address = 0x00100000
avoid_address = 0x100000+0x1890
good_address = 0x100000+0x187d

known_flag = "HTB{"
flag_length = 32

project = angr.Project("./spookylicence",main_opts={'base_addr' : base_address}, load_options={'auto_load_libs': False},)

known_chars=[claripy.BVV((known_flag[i])) for i in range(len(known_flag))]
flag_chars = [claripy.BVS(f"flag_{i}",8) for i in range(flag_length-len(known_flag))]
flag = claripy.Concat(*known_chars+flag_chars)


state=project.factory.full_init_state(args=["./spookylicence",flag], add_options={angr.sim_options.ZERO_FILL_UNCONSTRAINED_REGISTERS,angr.sim_options.ZERO_FILL_UNCONSTRAINED_MEMORY})

for i in range(4, 32):
    state.solver.add(flag.get_byte(i) >= 33)
    state.solver.add(flag.get_byte(i) <= 125)

sm = project.factory.simulation_manager(state)

sm.explore(find = good_address, avoid = avoid_address)
if(len(sm.found)>0):
	print(sm.found[0].solver.eval(flag,cast_to=bytes))
else:
	print("Not found :(")
```	
