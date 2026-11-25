# Manual fixes in YouTube Studio

The YouTube token used by the runs has only the `youtube.upload` and `youtube.readonly` scopes. With those, the API can't change titles or descriptions, post or pin comments, set a Short's Related video, or add end screens. Everything below has to be done by hand in [YouTube Studio](https://studio.youtube.com) until the token is re-authorized (see the last section). Every change is logged in `retitles.json` with the old values, so it can be undone.

Tick items off as you go. Scheduled runs append new items to the **Ongoing** section at the bottom.

## 1. Retitle the 10 lowest-viewed long videos

Studio → Content → the video → Details. Replace the title, and replace **only the first paragraph** of the description with the new hook. Leave the chapters, links and sources as they are. Each new hook is the `new_description` first paragraph in `retitles.json`.

- [ ] **10-power-supplies-explained** (5 views), https://youtu.be/fJiCtrVyq04
  - Old title: Power Supplies Explained: Watts, 80 Plus Ratings, and Why Cheap Ones Fail
  - New title: **80 Plus Gold Doesn't Mean a Good Power Supply**
  - New first paragraph: An 80 Plus Gold sticker tells you about efficiency, not whether a power supply is built well. Follow 400 watts from the wall to your graphics card and learn what the label really promises, how many watts you need, and why cheap units fail first.

- [ ] **04-why-your-pc-is-slow** (8 views), https://youtu.be/8zRSmxnJTIA
  - Old title: Why Your PC Is Slow — and Why More RAM Usually Isn't the Fix
  - New title: **Slow PC? More RAM Probably Won't Fix It**
  - New first paragraph: Everyone says buy more RAM. Before you spend anything, use one free tool already on your PC to find the part that is actually slowing it down, and fix that instead.

- [ ] **09-bottlenecks-explained** (9 views), https://youtu.be/u_trO1M6UvI
  - Old title: Bottlenecks Explained: Is Your CPU Holding Back Your GPU?
  - New title: **Is Your CPU Holding Back Your GPU? 1-Minute Test**
  - New first paragraph: A top-end graphics card can lose almost half its frame rate to a slow processor. Here's how to tell in about a minute whether your CPU or your GPU is setting your FPS, and what to do about it for free.

- [ ] **05-ssd-vs-hdd-vs-nvme** (12 views), https://youtu.be/fau-c6M-M9I
  - Old title: SSD vs HDD vs NVMe: What Really Makes Games Load Faster
  - New title: **HDD to SSD Is Huge. SSD to NVMe Barely Matters**
  - New first paragraph: In one test a game loaded in 6 seconds from an SSD and 63 from a hard drive, yet a drive several times faster than another barely changed load times. Here's where your load-screen time really goes, and which drive upgrade is worth paying for.

- [ ] **03-every-type-of-ram** (13 views), https://youtu.be/KLsnJ17daJE
  - Old title: Every Type of RAM Explained: DDR3 to DDR5
  - New title: **Will This RAM Fit Your PC? DDR3 vs DDR4 vs DDR5**
  - New first paragraph: Old RAM stick, new motherboard: will it fit, and would it work? Learn to read any memory stick, laptop or graphics card and know exactly which kind of RAM it takes.

- [ ] **08-what-raises-fps** (42 views), https://youtu.be/lPsuXNrw0ho
  - Old title: What Actually Raises FPS (and 5 Myths That Don't)
  - New title: **48 FPS to the Mid 80s Without Buying a Part**
  - New first paragraph: One gaming PC goes from 48 fps to the mid 80s without buying anything, and five popular tricks people swear by barely move the number. Here's where your time is actually worth spending.

- [ ] **07-black-friday-pc-traps** (58 views), https://youtu.be/KutUk2MTViE
  - Old title: 7 Black Friday PC Part Traps (and How to Spot a Real Deal)
  - New title: **That Black Friday PC Deal Might Not Be a Deal**
  - New first paragraph: A cart that says you saved 400 dollars might have saved almost nothing. Push one shopping cart through seven common traps and learn to check any PC deal in about a minute, through Cyber Monday and beyond.

- [ ] **06-how-a-cpu-runs-code** (79 views), https://youtu.be/O14uJcxMIvU
  - Old title: How a CPU Runs Your Code, One Clock Cycle at a Time
  - New title: **Why Your CPU Waits Hundreds of Cycles to Add 10**
  - New first paragraph: Your processor can do the math in one clock tick, or sit waiting for hundreds. Follow one line of game code through a CPU core, cycle by cycle, and see exactly where the time goes.

- [ ] **11-why-vram-matters** (102 views), https://youtu.be/gnxWsFC82yU
  - Old title: Why VRAM Suddenly Matters So Much (8 GB vs 16 GB, Explained)
  - New title: **Same GPU, 66 FPS vs 27: The Difference Is VRAM**
  - New first paragraph: Two graphics cards with the same chip: one averaged 66 fps, the other 27. The only difference was video memory. Here's what fills it, what happens when it runs out, and how much you actually need.

- [ ] **01-every-pc-component** (109 views), https://youtu.be/IlvT-Sk3UiQ
  - Old title: Every PC Component Explained in 7 Minutes (Animated)
  - New title: **What Every Part in Your PC Actually Does**
  - New first paragraph: Follow one click through the whole machine and learn what every component does, which parts actually matter for speed, and where people waste money. Also add the line `Subscribe: https://www.youtube.com/@plainlysilicon?sub_confirmation=1` above Sources.

## 2. Shorts: link the long video (description line 1 + Related video)

For each Short: Studio → Content → Shorts → the Short → Details.
1. Paste the `Full video:` line as the **first line** of the description.
2. Under **Related video**, pick the long video named in the heading. This is the clickable link: links in Shorts descriptions aren't clickable.

### → What Every Part in Your PC Actually Does

First line to paste: `Full video: https://www.youtube.com/watch?v=IlvT-Sk3UiQ`

- [ ] Every PC Part Explained in Under a Minute #shorts (https://youtube.com/shorts/cjw9ANAxdFU)
- [ ] RAM vs Storage: Why Your PC Needs Both #shorts (https://youtube.com/shorts/rJ8u3qW4z1Q)
- [ ] Why Your GPU Has Thousands of Cores #shorts (https://youtube.com/shorts/9cedjC4MWNQ)
- [ ] The Tiny Battery Inside Your PC #shorts (https://youtube.com/shorts/idn5jaZlcU4)
- [ ] Your RAM Is Probably Slower Than the Box Says #shorts (https://youtube.com/shorts/XOUnoLxUz10)
- [ ] Why Some USB Ports Are Blue #shorts (https://youtube.com/shorts/ubzLlQX1v70)

### → HDD to SSD Is Huge. SSD to NVMe Barely Matters

First line to paste: `Full video: https://www.youtube.com/watch?v=fau-c6M-M9I`

- [ ] The One Upgrade That Revives an Old PC #shorts (https://youtube.com/shorts/lNcLXmt8Aco)
- [ ] Why Your 1 TB Drive Shows 931 GB #shorts (https://youtube.com/shorts/2uyLR9TcsMg)
- [ ] M.2 Is a Shape, Not a Speed #shorts (https://youtube.com/shorts/b8rh1SlQbkk)
- [ ] Why Your SSD Gets Slower When It's Full #shorts (https://youtube.com/shorts/mHeiAA2MNvc)
- [ ] Should You Defrag an SSD? Here's Why Not #shorts (https://youtube.com/shorts/Sqc_-RSNgWk)
- [ ] Why a Faster NVMe SSD Doesn't Load Games Faster #shorts (https://youtube.com/shorts/duUtCwDQWvg)

### → How to Clean Your PC Without Breaking It

First line to paste: `Full video: https://www.youtube.com/watch?v=tMnGPUovm7o`

- [ ] Why Your PC Gets Slower in Summer #shorts (https://youtube.com/shorts/5AbYNnuyQdc)
- [ ] How Much Thermal Paste Should You Use? #shorts (https://youtube.com/shorts/jeubgoxVY8g)
- [ ] Is 95°C Too Hot for a Ryzen CPU? #shorts (https://youtube.com/shorts/fwrX16y99Nk)

### → How a GPU Actually Works: One Frame in 16 Milliseconds (Animated)

First line to paste: `Full video: https://www.youtube.com/watch?v=oouhEJk4AVM`

- [ ] GPUs Aren't Just for Graphics #shorts (https://youtube.com/shorts/Nqu5acq4PDI)
- [ ] Your GPU Has 16 Milliseconds Per Frame #shorts (https://youtube.com/shorts/GY6rtDE3gY4)

### → 48 FPS to the Mid 80s Without Buying a Part

First line to paste: `Full video: https://www.youtube.com/watch?v=lPsuXNrw0ho`

- [ ] Is Your Monitor Plugged Into the Wrong Port? #shorts (https://youtube.com/shorts/ushi5uADzCY)
- [ ] Your 144 Hz Monitor Might Be Stuck at 60 #shorts (https://youtube.com/shorts/tebCj2WisqM)
- [ ] Frame Generation Doubles FPS. Why Doesn't It Feel Faster? #shorts (https://youtube.com/shorts/4C-YQbxa6PY)
- [ ] Ultra vs High: Free FPS You Won't Even Notice #shorts (https://youtube.com/shorts/4ldMo0funu4)

### → Will This RAM Fit Your PC? DDR3 vs DDR4 vs DDR5

First line to paste: `Full video: https://www.youtube.com/watch?v=KLsnJ17daJE`

- [ ] Why Two RAM Sticks Beat One #shorts (https://youtube.com/shorts/MXZFC-aeTRk)
- [ ] Why You Can't Upgrade Your Laptop's RAM 🔒 #shorts (https://youtube.com/shorts/wfQFbHfrDJQ)
- [ ] DDR4 vs DDR5: Why the Wrong RAM Won't Fit #shorts (https://youtube.com/shorts/6pAYa4B4_fY)

### → Why Your CPU Waits Hundreds of Cycles to Add 10

First line to paste: `Full video: https://www.youtube.com/watch?v=O14uJcxMIvU`

- [ ] What 4 GHz Actually Means #shorts (https://youtube.com/shorts/4dC_XYvz8MA)
- [ ] 3 nm Chips Aren't Actually 3 nm #shorts (https://youtube.com/shorts/_nJieW9jBfA)
- [ ] CPU Cache Explained: Why RAM Is 100x Slower #shorts (https://youtube.com/shorts/SCJ5yoN0vR8)
- [ ] Cores vs Threads: What Hyper-Threading Really Does #shorts (https://youtube.com/shorts/GbDlILezeZ8)
- [ ] Your CPU Guesses Your Code Before It Knows #shorts (https://youtube.com/shorts/-1pgOBFgQ6A)

### → 80 Plus Gold Doesn't Mean a Good Power Supply

First line to paste: `Full video: https://www.youtube.com/watch?v=fJiCtrVyq04`

- [ ] Your 850 W Power Supply Doesn't Use 850 W #shorts (https://youtube.com/shorts/Ioo98nWJ81o)
- [ ] Why Your Graphics Card Needs Extra Power Cables #shorts (https://youtube.com/shorts/-CJTjorPTiY)
- [ ] TDP Isn't How Much Power Your CPU Uses #shorts (https://youtube.com/shorts/LTcVBmWoAp0)

### → Slow PC? More RAM Probably Won't Fix It

First line to paste: `Full video: https://www.youtube.com/watch?v=8zRSmxnJTIA`

- [ ] Disk at 100% in Task Manager? It's Not About Space #shorts (https://youtube.com/shorts/dwJ0O23uMx4)
- [ ] Almost No Free RAM? Windows Does That on Purpose #shorts (https://youtube.com/shorts/wTM-lMHR8YY)

### → That Black Friday PC Deal Might Not Be a Deal

First line to paste: `Full video: https://www.youtube.com/watch?v=KutUk2MTViE`

- [ ] Is That Black Friday "Was" Price Real? Check This #shorts (https://youtube.com/shorts/CMdAyOdSfrI)
- [ ] One Name, Two GPUs: The RTX 3050 6GB Catch #shorts (https://youtube.com/shorts/BeOpZMSupmo)

### → Is Your CPU Holding Back Your GPU? 1-Minute Test

First line to paste: `Full video: https://www.youtube.com/watch?v=u_trO1M6UvI`

- [ ] Why CPU Reviews Test at 1080p With the Fastest GPU #shorts (https://youtube.com/shorts/j5vJwicvzcI)

## 3. First comments (pin each one)

Post from the channel account, then ⋮ → Pin. Do it once the video is public.

- [ ] 11-why-vram-matters, https://youtu.be/gnxWsFC82yU: "What GPU are you running right now, and how much VRAM does it have?"

## 4. End screens on long videos

Every long video should end on an end screen that points to the **next** long video, plus a Subscribe element. Studio → the video → Editor → End screen. The fastest way is **Import from video** (pick the previous long video), then change the video element.

- [ ] Each Saturday, when the new long video goes live: open **last week's** long video and point its end-screen video element at the new one, so the chain always leads forward.
- [ ] One-time setup for the existing videos: 01 → 02 → 03 → 04 → 05 → 06 → 07 → 08 → 09 → 10 → 11 → 12, each pointing at the next one in that order. 12 points to the Nov 28 video once it's uploaded.

## 5. Optional: let the runs do all of this automatically (free)

Re-authorize the YouTube token with the extra scope `https://www.googleapis.com/auth/youtube.force-ssl` (keep `youtube.upload` and `youtube.readonly`), then replace `YT_REFRESH_TOKEN` in the environment's settings. After that, `python3 youtube_update.py apply` makes sections 1 and 2's description changes, and runs post first comments with `youtube_update.py comment`. Pinning, the Related video and end screens still need Studio: the API has no way to set them.

## Ongoing (added by the scheduled runs)

<!-- Each run adds a line per upload: first comment to pin, Related video for Shorts, end-screen update for long videos. -->
- [x] (done Nov 24) By Fri Nov 27: **DELETE the old private upload of 23** https://youtu.be/iM69YHi2yAQ (Studio → Content → ⋮ → Delete forever). A new version with the subscribe ask uploads automatically just after midnight Nov 25, scheduled for Sat Nov 28 5:00 AM; if the old one isn't deleted it also goes public Sat 10:00 as a duplicate.
- [ ] Optional: Short 10s1 ("Why Cheap Power Supplies Die Early") is set to publish 12:00 Nov 25 by the vidIQ reminder on your MacBook. To move it to 5:00 AM, approve the updated reminder in a Claude conversation on that Mac, or change it in vidIQ.
- [ ] 2026-11-25 12-clean-your-pc https://youtu.be/tMnGPUovm7o (public Wed 5:00 AM): pin first comment "When did you last clean the dust out of your PC, and how bad was it?"; end screen: point its video element at 23 (https://youtu.be/15pV5fzsfSU) + Subscribe
- [ ] 2026-11-25 09s1 Short https://youtube.com/shorts/LK1bec3JH_A (public Wed 5:00 AM): Related video = Bottlenecks video (https://youtu.be/u_trO1M6UvI); pin first comment "What does your GPU usage sit at in the game you play most?"
- [ ] 2026-11-28 23-best-budget-gpu https://youtu.be/15pV5fzsfSU (public Sat 5:00 AM): pin first comment "What GPU are you running right now, and what did you pay for it?"; add an end screen (Subscribe + a video element)
