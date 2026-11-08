# part2_mesa_agents.py
# ITAI-4370 Midterm Projects — Part 2: Agent-Based Network Modeling with Mesa
#
# COLAB SETUP (run this in its own cell first):
#   !pip install mesa
#
# What this does:
#   Routers and users are agents. Every user sends traffic through one
#   router. Each router can handle a limited number of users at once
#   (its capacity). When a router gets congested, users notice and move
#   to the least-loaded router. That is adaptive rerouting: the network
#   rebalances itself instead of letting one router stay overloaded.
#
# How to run: paste this whole file into a Colab cell (after the pip
# cell) and run it. No other files are needed.
#
# NOTE: this uses the Mesa 3.x API (an Agent is created with just the
# model, and the model steps its agents itself). The pip install above
# gets Mesa 3.x.

from mesa import Agent, Model
from mesa.datacollection import DataCollector


class RouterAgent(Agent):
    """A router that carries traffic for the users connected to it."""

    def __init__(self, model, router_id, capacity):
        super().__init__(model)
        self.router_id = router_id
        self.capacity = capacity  # max users it can handle without congestion
        self.load = 0             # users currently routed through it

    def reset(self):
        """Called at the start of every step: last step's load is gone."""
        self.load = 0

    def is_congested(self):
        return self.load >= self.capacity


class UserAgent(Agent):
    """A user sending traffic through one router at a time."""

    def __init__(self, model, user_id, router):
        super().__init__(model)
        self.user_id = user_id
        self.router = router      # the router this user is using right now
        self.reroutes = 0         # how many times this user has switched

    def step(self):
        # If my router is full, move to the least-loaded router instead.
        if self.router.is_congested():
            least_loaded = min(self.model.routers, key=lambda r: r.load)
            if least_loaded is not self.router:
                self.router = least_loaded
                self.reroutes += 1
        # Send my traffic through (whichever) router I am on now.
        self.router.load += 1


class NetworkModel(Model):
    """The whole network: 3 routers and a group of users."""

    def __init__(self, num_users=10, seed=42):
        super().__init__(seed=seed)
        # Three routers, each able to handle 4 users at once.
        self.routers = [RouterAgent(self, i, capacity=4) for i in range(3)]
        # Everyone starts on Router 0 (the default route). That is what
        # creates the congestion the model then fixes by rerouting.
        self.users = [UserAgent(self, i, self.routers[0]) for i in range(num_users)]
        self.step_reroutes = 0

        self.datacollector = DataCollector(
            model_reporters={
                "Reroutes": lambda m: m.step_reroutes,
                "Max load": lambda m: max(r.load for r in m.routers),
                "Congested routers": lambda m: sum(
                    1 for r in m.routers if r.is_congested()
                ),
            }
        )

    def step(self):
        # Phase 1: every router starts the step empty.
        for router in self.routers:
            router.reset()
        # Phase 2: users act in a random order (so no user always goes
        # first), each one picking a router and adding their traffic.
        before = sum(u.reroutes for u in self.users)
        order = self.users[:]
        self.random.shuffle(order)
        for user in order:
            user.step()
        self.step_reroutes = sum(u.reroutes for u in self.users) - before
        self.datacollector.collect(self)


def main():
    model = NetworkModel(num_users=10, seed=42)
    for _ in range(20):
        model.step()

    results = model.datacollector.get_model_vars_dataframe()
    print("Step-by-step results (first 10 steps):")
    print(results.head(10))
    print()
    print(f"Total reroutes over 20 steps: {sum(u.reroutes for u in model.users)}")
    print("Final users per router:", [r.load for r in model.routers])
    print()
    print("What happened: everyone started on Router 0, so it congested")
    print("immediately. Users moved to the emptier routers until the load")
    print("spread out across all three — that is adaptive rerouting.")


if __name__ == "__main__":
    main()
