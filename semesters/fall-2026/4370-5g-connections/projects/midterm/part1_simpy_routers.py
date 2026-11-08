# part1_simpy_routers.py
# ITAI-4370 Midterm Projects — Part 1: Network Traffic Simulation with SimPy
#
# COLAB SETUP (run this in its own cell first):
#   !pip install simpy
#
# What this does:
#   Packets travel through three routers in a chain (A -> B -> C).
#   Each router can only handle one packet at a time, and each one adds
#   its own processing delay. We measure the total latency of every
#   packet: the time from when it is created to when it leaves the
#   last router.
#
# How to run: paste this whole file into a Colab cell (after the pip
# cell) and run it. No other files are needed.

import random
import simpy

# --- Settings (change these to experiment) ---
RANDOM_SEED = 42        # fixed seed so the results are repeatable
NUM_PACKETS = 100       # how many packets to send through the chain
ARRIVAL_MEAN = 1.5      # average time between new packets
ROUTER_DELAYS = [0.8, 1.2, 0.8]  # processing delay at Router A, B, C


def packet(env, packet_id, routers, results):
    """One packet travelling through the whole chain of routers."""
    arrival_time = env.now  # the clock time this packet was created

    # Visit each router in order. A router is a Resource with capacity 1,
    # so if it is busy, the packet waits in line (that waiting time is
    # part of the packet's total latency).
    for router, delay in zip(routers, ROUTER_DELAYS):
        with router.request() as request:
            yield request             # wait until the router is free
            yield env.timeout(delay)  # the router processes the packet

    # The packet has left the last router: record its total latency.
    results.append(env.now - arrival_time)


def packet_source(env, routers, results):
    """Creates packets one at a time, with random gaps between them."""
    for i in range(NUM_PACKETS):
        env.process(packet(env, i, routers, results))
        # Random gap until the next packet (exponential distribution,
        # which is the standard way to model random network arrivals).
        yield env.timeout(random.expovariate(1.0 / ARRIVAL_MEAN))


def main():
    random.seed(RANDOM_SEED)
    env = simpy.Environment()

    # Three routers in a chain. Capacity 1 = one packet at a time.
    routers = [simpy.Resource(env, capacity=1) for _ in range(3)]

    results = []  # total latency of every packet
    env.process(packet_source(env, routers, results))
    env.run()  # run until all packets have finished

    # --- Results ---
    average = sum(results) / len(results)
    minimum_possible = sum(ROUTER_DELAYS)  # latency with zero waiting

    print(f"Packets delivered: {len(results)}")
    print(f"Minimum possible latency (no waiting): {minimum_possible:.2f} time units")
    print(f"Average total latency: {average:.2f} time units")
    print(f"Fastest packet: {min(results):.2f} time units")
    print(f"Slowest packet: {max(results):.2f} time units")
    print(f"Average time spent waiting in line: {average - minimum_possible:.2f} time units")
    print()
    print("Why the average is higher than the minimum: Router B is the")
    print("slowest router, so packets sometimes queue up behind it. That")
    print("waiting time is what pushes total latency above the sum of the")
    print("processing delays.")


if __name__ == "__main__":
    main()
