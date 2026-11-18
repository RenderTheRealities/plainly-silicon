# Video 11 — Why VRAM Suddenly Matters So Much

Length: 7:07 · Theme: graphite · Voice: Kokoro · Narration: `narration.txt`

Through-line: two RTX 5060 Ti cards with the same chip (8 GB vs 16 GB) and why one ran Dragon Age: The Veilguard at 66 fps and the other at 27. VRAM is a suitcase: we pack one 4K texture (64 MB raw, 16 MB as BC7, about 21 MB with mips), then everything else (frame buffers, models, shaders, ray tracing BVH, frame generation), explain why console memory budgets made 8 GB tight, show what happens when it overflows (data moves to system RAM over an 8-lane PCIe link: 32 GB/s vs 448 GB/s), why that shows up as stutter and 1% lows, how the PCIe generation changes the damage, which settings matter, and how much to buy. Visuals: editorial print layout; VRAM is a memory-map suitcase of 64 tiles (128 MB each), bandwidth pipes drawn to scale, frame-time strip charts, a kitchen and a shop down the street, a Task Manager-style usage graph.

## Title

Why VRAM Suddenly Matters So Much (8 GB vs 16 GB, Explained)

## Description

Two graphics cards with the same chip: one averaged 66 fps, the other 27. The only difference was VRAM. Here's what fills your graphics card's memory, what happens when it runs out, and how much you actually need.

Chapters
0:00 Same chip, different results
0:21 What VRAM is
1:04 Packing one texture
1:49 Everything else in VRAM
2:28 Why now: consoles set the budget
3:03 When VRAM runs out
3:51 Stutter and 1% lows
4:41 Your PCIe slot matters
5:13 It depends on the game
5:52 How much VRAM you need
6:34 Check your own card

Watch next: https://www.youtube.com/watch?v=oouhEJk4AVM

Subscribe: https://www.youtube.com/@plainlysilicon?sub_confirmation=1

Test results are from the reviews below (RTX 5060 Ti 8 GB vs 16 GB); the "VRAM it costs" bars in chapter 9 are illustrative. Texture sizes are worked out from the formats' bits per pixel.

Sources:
- TechSpot, "Nvidia RTX 5060 Ti PCIe benchmark: 8GB vs 16GB" (x8 link; 448 GB/s VRAM; PCIe 3.0/4.0/5.0 x8 = 16/32/64 GB/s; DDR5-6000 ~96 GB/s; Dragon Age, Monster Hunter Wilds, Indiana Jones, The Last of Us Part II results): https://www.techspot.com/review/3004-nvidia-rtx-5060-ti-pcie-benchmark/
- PC Gamer, "My real-world testing shows 8 GB GPUs are still enough for gaming in 2026..." (Cyberpunk 2077 1% lows; 16 GB cards using about 9-11 GB): https://www.pcgamer.com/hardware/graphics-cards/my-real-world-testing-shows-8-gb-gpus-are-still-enough-for-gaming-in-2026-but-im-surprised-at-just-how-much-faster-the-16-gb-versions-are
- Tom's Hardware, "PS5 Specs Revealed" (16 GB GDDR6): https://www.tomshardware.com/news/ps5-specs-revealed-cpu-gpu
- Resonite Wiki, "Texture compression formats" (BC7 8 bpp, RGBA32 32 bpp, mipmaps): https://wiki.resonite.com/Texture_compression_formats
- Unity Manual, "Texture compression formats": https://docs-alpha.unity3d.com/2023.2/Documentation/Manual/texture-compression-formats.html

#pchardware #techexplained

## Tags

vram explained, what is vram, how much vram do i need, 8gb vs 16gb vram, rtx 5060 ti 8gb vs 16gb, is 8gb vram enough, vram stutter, 1% lows explained, pcie 4.0 vs 5.0 gpu, gpu memory explained, texture quality vram, pc hardware explained, graphics card buying guide

## First comment

How much VRAM does your graphics card have, and have you ever watched it hit the limit in a game? Tell us below.

Related: How a GPU actually works, one frame in 16 milliseconds: https://www.youtube.com/watch?v=oouhEJk4AVM

## Thumbnail

`thumbnail.jpg`: "8 GB" in white and "ENOUGH?" in red on the graphite dot background; an overfull memory-map suitcase with red tiles at the bottom and red tiles spilling out to the left; a white pill reads "Why VRAM matters now".
