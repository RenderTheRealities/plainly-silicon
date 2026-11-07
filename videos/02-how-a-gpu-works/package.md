# Video 02 — How a GPU Actually Works

Publish: Sat Nov 7, 2026 16:00 America/Cambridge_Bay · Length: 6:42 · Theme: neon · Voice: Kokoro am_michael

Through-line: one frame of a game travels the whole GPU pipeline inside its 16.7 ms budget (CPU draw calls -> vertices -> rasterization -> pixel shading -> warps -> memory -> ray tracing/tensor cores -> frame buffer). A pipeline track at the top of each stage scene shows where the frame is.

## Title

How a GPU Actually Works: One Frame in 16 Milliseconds (Animated)

## Description

Your graphics card has about 16 milliseconds to draw every frame at 60 fps. This animated explainer follows one single frame through the GPU: draw calls from the CPU, vertex shaders, rasterization, pixel shaders, warps of 32 threads, memory bandwidth, ray tracing and tensor cores, and the frame buffer swap.

Chapters
0:00 Sixteen milliseconds per frame
0:18 The job: millions of pixels
0:55 The CPU sends draw calls
1:19 Vertices and the vertex shader
1:49 Rasterization
2:26 Pixel shaders
3:00 Cores and warps (RTX 4060)
3:40 Hiding memory latency and branch divergence
4:25 Memory bandwidth and VRAM
4:56 Ray tracing and tensor cores
5:32 Frame buffer and output
6:03 One frame, replayed

Watch next: https://www.youtube.com/watch?v=IlvT-Sk3UiQ

Subscribe: https://www.youtube.com/@plainlysilicon?sub_confirmation=1

Sources:
- Tom's Hardware, Nvidia GeForce RTX 4060 review (specs: 24 SMs x 128 CUDA cores, 8 GB, 128-bit, 272 GB/s, 24 MB L2, 24 RT cores, 96 tensor cores): https://www.tomshardware.com/reviews/nvidia-geforce-rtx-4060-review-asus-dual
- GameDev.net, Introduction to the Graphics Pipeline: https://www.gamedev.net/articles/programming/graphics/introduction-to-the-graphics-pipeline-r3344
- Introduction to CUDA Programming, Understanding Warps in CUDA: https://intro-to-cuda.readthedocs.io/en/latest/tutorial/warps.html
- Alex Dillhoff, CUDA Architecture notes (warp scheduling, control divergence): https://ajdillhoff.github.io/notes/cuda_architecture/

#pchardware #techexplained

## First comment

What graphics card are you running right now, and what resolution do you play at?

## Tags

how a gpu works, how gpu works, gpu explained, graphics card explained, how does a graphics card work, gpu architecture, graphics pipeline, rasterization explained, shaders explained, cuda cores explained, warps gpu, vram explained, ray tracing cores, tensor cores explained, pc hardware explained
