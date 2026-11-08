# ITAI-4370 Midterm Projects — Explained in Plain Language

## How to run this in Google Colab

1. Open a new Colab notebook.
2. In the first cell, run this (it installs the three libraries):
   `!pip install simpy mesa scikit-learn`
3. Paste each `.py` file into its own cell and run it. Each file runs
   on its own — no other files needed.
4. When you submit on Canvas, upload the three `.py` files. That is
   what the assignment asks for (file upload only).

## Part 1 — Network Traffic Simulation with SimPy

Packets travel through three routers in a chain, one after the other.
Each router can only handle one packet at a time, and each one takes a
little time to process a packet. If a router is busy, the next packet
has to wait in line, and that waiting time counts toward its total
trip time. The program sends 100 packets with random gaps between
them and reports the average trip time. The key result: the average
trip is longer than just adding up the three processing delays,
because packets pile up behind the slowest router (Router B). That
waiting in line is the whole point — it is why real networks feel
slow even when every router is working fine.

## Part 2 — Agent-Based Network Modeling with Mesa

Here the routers and the users are "agents," meaning each one makes
its own little decisions. Every user starts on Router 0, the default
route, so it gets overloaded right away. Each step, any user on a
full router moves to the least-loaded router instead. After the
first step the load spreads out across all three routers and stays
balanced, and almost nobody needs to switch anymore. That is
adaptive rerouting: instead of one fixed rule, the users react to
congestion and the network fixes itself.

## Part 3 — Predictive Optimization with Machine Learning

This part has two stages. First, we fake up 500 measurements of
network traffic (how many packets per second, how full the router
was, what hour it was) and the delay that resulted, then we train
a model to predict delay from those conditions. The model learns
the important pattern: delay shoots up fast when the router is
almost full. Second, we use that model to choose routes. For new
traffic, we ask it how slow the current route will be and how slow
a longer alternate route would be (it adds 15 ms of detour but
carries much less load), and we take whichever is predicted faster.
At low load the model says stay put; at high load it says reroute,
even with the detour. So the prediction itself makes the routing
decision — that is the optimization.

## What you should see when you run them

- Part 1: 100 packets delivered, fastest trip 2.80 time units (the
  sum of the three processing delays, with zero waiting), average
  around 4.90, slowest around 21 — the slow ones are the ones that
  waited behind Router B.
- Part 2: 6 reroutes in the first step, then almost none, ending
  with the users split 4 / 3 / 3 across the three routers.
- Part 3: a small average prediction error (a few milliseconds) and
  a score close to 1, plus a routing table where high-load rows say
  "reroute to B" and low-load rows say "stay on A."

## If someone asks you what you did

"I simulated packets going through three routers and measured how
queueing adds delay. Then I built an agent model where users move
off congested routers on their own, so the load balances itself.
Then I trained a model to predict delay from traffic conditions
and used those predictions to pick the faster route."
