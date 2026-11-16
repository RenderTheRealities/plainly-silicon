# Your CPU Guesses Your Code Before It Knows #shorts

## Description
At every if-statement a CPU's branch predictor guesses which way the code will go and runs ahead; a wrong guess flushes the pipeline and costs roughly 15 to 20 clock cycles on recent desktop chips.
Full video: How a CPU Runs Your Code, One Clock Cycle at a Time
#shorts #cpu #pchardware

## Tags
branch prediction, branch predictor, branch misprediction, cpu pipeline, how a cpu works, speculative execution, pc hardware explained

## First comment
Did you know your CPU was guessing? What CPU are you running right now?

## Related video
06-how-a-cpu-runs-code: https://www.youtube.com/watch?v=O14uJcxMIvU

## Sources
- Stack Overflow, "How much does a mispredicted conditional branch cost?" (about 16.5 to 20 cycles on Skylake-class cores, citing 7-cpu.com measurements; 14 cycles on Cortex-A76): https://stackoverflow.com/questions/76839219/how-much-does-a-mispredicted-conditional-branch-cost
- Johnny's Software Lab, "How branches influence the performance of your code" (misprediction flushes speculative work, roughly 15 to 20 cycles): https://johnnysswlab.com/how-branches-influence-the-performance-of-your-code-and-what-can-you-do-about-it/
- Chips and Cheese, "AMD's Zen 4 Part 1: Frontend and Execution Engine" (how a modern branch predictor uses past behavior): https://chipsandcheese.com/p/amds-zen-4-part-1-frontend-and-execution-engine
