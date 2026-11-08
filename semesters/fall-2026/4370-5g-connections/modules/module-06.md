# Module 6 — AI for Network Optimization and Management

## What this module is about

Using AI to run a network better: predicting problems before they hit, and choosing the best route — not just the shortest one on paper, but the one that is actually fastest right now.

## What I worked on

- **Midterm Project, Part 3 (Stage 2)** — prediction-based routing. The trained model compares the current route with an alternate route (a 15 ms detour, but only 30% of the current load) and picks whichever is predicted faster. At low load it stays put; at high load it reroutes, even with the detour. See [../projects/midterm/](../projects/midterm/).
- Coursework notebooks for this module are in [notebooks/](../notebooks/).

## What I took away

The best route is the one that is actually fastest right now, and only a prediction can tell you that. A fixed rule cannot see congestion coming; a model can.
