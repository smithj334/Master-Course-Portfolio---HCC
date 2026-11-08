# Module 5 — Open RAN and AI-Driven Networks

## What this module is about

Open RAN opens up the radio network so equipment from different vendors can work together, instead of one company controlling the whole stack. With that openness comes intelligent control: AI can watch the network and steer traffic in real time.

## What I worked on

- **Midterm Project, Part 2** — Mesa agent model: 10 users start on Router 0, the default route, so it congests right away. Any user on a full router moves to the least-loaded router instead. 6 reroutes in the first step, then almost none, ending split 4 / 3 / 3 across three routers. See [../projects/midterm/](../projects/midterm/).
- Coursework notebooks for this module are in [notebooks/](../notebooks/).

## What I took away

A network that reacts to congestion beats a network with one fixed rule. The users in my model were not told what to do from the top down — they reacted, and the network balanced itself. That is the idea Open RAN is built around.
