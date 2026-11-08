# Midterm Projects — ITAI-4370

**Submitted Oct 29, 2026. Individual work, file upload to Canvas.**

Three simulations, each in its own Python file, each runnable on its own in Google Colab. Setup: `!pip install simpy mesa scikit-learn`, then paste one file per cell and run.

## What I built

### Part 1 — Network Traffic Simulation with SimPy

`part1_simpy_routers.py`

Packets travel through three routers in a chain (A → B → C). Each router handles one packet at a time and adds its own processing delay. If a router is busy, the next packet waits in line, and that waiting time counts toward its total trip time. The program sends 100 packets with random gaps between them and reports the latency of every packet.

**Real run results (seed 42):**

- Packets delivered: 100
- Average total latency: 5.39 time units
- Fastest packet: 2.80 time units
- Slowest packet: 11.35 time units
- Average time spent waiting in line: 2.59 time units

**What it showed:** the average trip is longer than just adding up the three processing delays, because packets pile up behind the slowest router (Router B). That waiting in line is why real networks feel slow even when every router is working fine.

### Part 2 — Agent-Based Network Modeling with Mesa

`part2_mesa_agents.py`

Routers and users are agents — each one makes its own small decisions. Every user starts on Router 0, the default route, so it gets overloaded right away. Each step, any user on a full router moves to the least-loaded router instead.

**Real run results (10 users, 20 steps, seed 42):**

- 6 reroutes in the first step, then almost none
- Final split: 4 / 3 / 3 users across the three routers

**What it showed:** adaptive rerouting. Instead of one fixed rule, the users react to congestion and the network balances itself.

### Part 3 — Predictive Optimization with scikit-learn

`part3_sklearn_routing.py`

Two stages. First, 500 simulated traffic measurements (packets per second, router load, hour of day) and the latency that resulted, used to train a Random Forest model to predict latency from those conditions. The model learned the key pattern: delay shoots up fast when the router is almost full. Second, the model chooses routes. For new traffic, it predicts how slow the current route will be and how slow a longer alternate route would be (it adds a 15 ms detour but carries much less load), and takes whichever is predicted faster.

**What it showed:** at low load the model says stay put; at high load it says reroute, even with the detour. The prediction itself makes the routing decision — that is the optimization.

## Files

- `part1_simpy_routers.py` — SimPy routing simulation
- `part2_mesa_agents.py` — Mesa agent-based model (uses the Mesa 3.x API)
- `part3_sklearn_routing.py` — scikit-learn latency prediction and route selection
- `midterm-explained.md` — plain-language explanation of all three parts, including how to run them in Colab

## In my own words

"I simulated packets going through three routers and measured how queueing adds delay. Then I built an agent model where users move off congested routers on their own, so the load balances itself. Then I trained a model to predict delay from traffic conditions and used those predictions to pick the faster route."
