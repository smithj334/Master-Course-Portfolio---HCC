# part3_sklearn_routing.py
# ITAI-4370 Midterm Projects — Part 3: Predictive Optimization with scikit-learn
#
# COLAB SETUP (run this in its own cell first):
#   !pip install scikit-learn
#
# What this does (two stages):
#   1. TRAIN: we simulate network traffic data (traffic volume, router
#      load, hour of day) and the latency that resulted, then train a
#      machine-learning model to PREDICT latency from those conditions.
#   2. ROUTE: for new traffic, we ask the model "how slow will the
#      current route be?" and "how slow would the alternate route be?"
#      and send the traffic down whichever route is predicted faster.
#      The predictions change the routing — that is the optimization.
#
# How to run: paste this whole file into a Colab cell (after the pip
# cell) and run it. No other files are needed.

import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error


def make_traffic_data(n_samples=500, seed=42):
    """Simulate traffic measurements and the latency that resulted.

    Features (what the network looked like):
      - traffic: packets per second on the link
      - load:    how full the router was, in percent (0-100)
      - hour:    hour of the day (0-23), since traffic has daily patterns
    Target (what we want to predict):
      - latency: milliseconds for a packet to get through
    The latency formula below is the 'ground truth' of our simulated
    network: latency grows with traffic, and grows FASTER as the router
    fills up (that squared term is the queueing effect — a nearly-full
    router delays packets much more than a half-full one).
    """
    rng = np.random.default_rng(seed)
    traffic = rng.integers(100, 1000, size=n_samples)   # packets/sec
    load = rng.uniform(10, 95, size=n_samples)          # router load %
    hour = rng.integers(0, 24, size=n_samples)          # hour of day
    noise = rng.normal(0, 3, size=n_samples)            # random variation

    latency = (10 + 0.05 * traffic + 0.4 * load
               + 0.01 * load ** 2 + 2 * np.sin(hour / 24 * 2 * np.pi)
               + noise)
    X = np.column_stack([traffic, load, hour])
    return X, latency


def main():
    # ---------- Stage 1: train the model ----------
    X, y = make_traffic_data()
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42)

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    print(f"Test samples: {len(y_test)}")
    print(f"Mean absolute error: {mae:.2f} ms "
          f"(on average, predictions are off by this much)")
    print(f"Model score (R^2): {model.score(X_test, y_test):.3f} "
          f"(1.0 would be perfect)")
    print()

    # ---------- Stage 2: use predictions to choose routes ----------
    # New traffic scenarios the model has never seen. For each one we
    # compare two options:
    #   Route A (current): keep the traffic where it is.
    #   Route B (alternate): a longer path (+15 ms detour), but it only
    #     carries 30% of the current load, so it is much less congested.
    print("Routing decisions for 10 new traffic scenarios:")
    print("traffic  load | predicted A | predicted B | decision")
    rng = np.random.default_rng(7)
    saved = []
    rerouted = 0
    for _ in range(10):
        traffic = int(rng.integers(100, 1000))
        load = float(rng.uniform(10, 95))
        hour = int(rng.integers(0, 24))

        pred_a = model.predict([[traffic, load, hour]])[0]
        pred_b = model.predict([[traffic, load * 0.3, hour]])[0] + 15

        if pred_b < pred_a:
            decision = "reroute to B"
            rerouted += 1
            saved.append(pred_a - pred_b)
        else:
            decision = "stay on A"
        print(f"{traffic:7d} {load:5.0f}% | {pred_a:10.1f} ms | {pred_b:10.1f} ms | {decision}")

    print()
    print(f"Rerouted {rerouted} of 10 scenarios.")
    if saved:
        print(f"Average predicted time saved by rerouting: {np.mean(saved):.1f} ms")
    print()
    print("What this shows: the model learned that latency explodes when")
    print("the router is nearly full, so at high load the alternate route")
    print("wins even with its 15 ms detour — and at low load, staying put")
    print("wins. The prediction, not a fixed rule, makes the call.")


if __name__ == "__main__":
    main()
