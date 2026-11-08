# Video 06 — How a CPU Runs Your Code, One Clock Cycle at a Time

Length: 6:26 · Theme: sunset · Voice: Kokoro am_michael · Narration: `narration.txt`

Through-line: one tiny line of game code, `score = score + 10`, followed through a single CPU core: compiled instruction, program counter, the clock, fetch, decode into micro-ops, registers and the ALU, pipelining, out-of-order execution, the cache ladder, the high-score branch and its prediction, then IPC, and a replay of the whole trip. Visuals: a thin clock strip ticking over the core scenes, instruction capsules, a register file with changing values, a pipeline timing diagram, a cache ladder with latency counters and a forked road for the branch predictor.

## Title

How a CPU Runs Your Code, One Clock Cycle at a Time

## Description

When your game adds ten points to your score, your CPU can do the math in one clock tick, or wait hundreds of ticks for the data. This animated explainer follows that one line of code through a processor core, cycle by cycle: fetch, decode into micro-ops, registers and the ALU, pipelining, out-of-order execution, cache latency, branch prediction and IPC.

Chapters
0:00 Ten points, one core
0:22 From code to instructions
0:49 The clock: 5 GHz and 0.2 ns per tick
1:21 Fetch
1:45 Decode into micro-ops
2:17 Registers and the ALU
2:52 Pipelining
3:20 Out-of-order execution
3:55 The cache ladder: L1, L2, L3, RAM
4:29 Branch prediction and mispredictions
5:05 IPC: work per tick
5:45 The ten points, replayed
6:14 Up next

Watch next: https://www.youtube.com/watch?v=IlvT-Sk3UiQ

Subscribe: https://www.youtube.com/@plainlysilicon?sub_confirmation=1

Sources:
- Chips and Cheese, AMD's Zen 4 Part 2: Memory Subsystem (L1D 4 cycles, L2 14 cycles, ~73 ns DRAM, 5.7 GHz boost): https://chipsandcheese.com/p/amds-zen-4-part-2-memory-subsystem-and-conclusion
- TechPowerUp, AMD Zen 4 cache sizes and latencies (L2 14 cycles, L3 50 cycles): https://www.techpowerup.com/298338/amd-zen-4-dies-transistor-counts-cache-sizes-and-latencies-detailed
- Chips and Cheese, AMD's Zen 4 Part 1: Frontend and Execution Engine (320-entry reorder buffer, micro-op cache): https://chipsandcheese.com/p/amds-zen-4-part-1-frontend-and-execution-engine
- Chips and Cheese, Running Gaming Workloads through AMD's Zen 5 (448-entry ROB, 8-wide rename, 32 KB L1i, games are low-IPC): https://chipsandcheese.com/p/running-gaming-workloads-through
- 7-cpu.com, AMD Zen 2 (branch misprediction penalty 18 cycles): https://7-cpu.com/cpu/Zen2.html
- Stack Overflow, How much does a mispredicted conditional branch cost (Skylake ~16.5-20 cycles, Haswell 16-20): https://stackoverflow.com/questions/76839219/how-much-does-a-mispredicted-conditional-branch-cost
- uops.info, ADD (register) latency and throughput on Zen 4 and Alder Lake: https://uops.info/html-instr/ADD_01_R64_R64.html
- Stack Overflow, What happens when adding to memory from a register (add to memory = load + ALU add + store): https://stackoverflow.com/questions/36390747/what-happens-when-adding-to-memory-from-a-register
- Baeldung, The Fetch-Execute Cycle: https://www.baeldung.com/cs/fetch-execute-cycle
- Wikipedia: Instruction pipelining, Out-of-order execution, Branch predictor, Instructions per cycle, x86-64 (16 general-purpose 64-bit registers)
- Hackaday, Visualizing a nanosecond (Grace Hopper's 11.8-inch wire): https://hackaday.com/2012/02/27/visualizing-a-nanosecond/

#pchardware #techexplained

## Tags

how a cpu works, how cpu executes instructions, fetch decode execute, cpu pipeline explained, out of order execution, branch prediction explained, cpu cache explained, l1 l2 l3 cache, clock speed explained, what is ipc, micro-ops, cpu registers alu, computer architecture animation, pc hardware explained

## First comment

What CPU is in your PC right now, and what's its boost clock? Check it and tell us below.

## Thumbnail

`thumbnail.jpg`: "ONE TICK" in white and "0.2 ns" in orange on the sunset gradient, with a pink chip outline full of instruction capsules in pipeline rows and an orange clock wave along the bottom with one tick boxed.
