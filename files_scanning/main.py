"""
main.py - Smart Scan Strategy using ML (EW mini project)
Runs the round robin (old) scanner and the Q-learning (smart) scanner
on the same fake RF environment, compares how many emitters they catch,
and plots the results. Also runs the bonus periodic-detection check.
"""

import random
import matplotlib.pyplot as plt

from env import RFEnv
from scanners import run_round_robin, run_q_learning, detect_periodic

random.seed(42)  # keeping this fixed so results dont change every run


def avg_gap(hit_times):
    # average time between consecutive hits, kinda like avg detection time
    if len(hit_times) < 2:
        return None
    gaps = []
    for i in range(1, len(hit_times)):
        gaps.append(hit_times[i] - hit_times[i - 1])
    return sum(gaps) / len(gaps)


if __name__ == "__main__":
    env = RFEnv()

    rr_hits, rr_miss, rr_hit_times, rr_curve = run_round_robin(env)
    q_hits, q_miss, q_hit_times, q_curve, q_table = run_q_learning(env)

    print("----- ROUND ROBIN (old method) -----")
    print("hits:", rr_hits)
    print("misses:", rr_miss)
    print("avg gap between hits:", avg_gap(rr_hit_times))

    print()
    print("----- Q-LEARNING (smart method) -----")
    print("hits:", q_hits)
    print("misses:", q_miss)
    print("avg gap between hits:", avg_gap(q_hit_times))

    print()
    print("--- bonus: checking which bands are periodic ---")
    for b in range(env.num_bands):
        detect_periodic(env, b)

    # plot 1 - cumulative hits over time, smart vs dumb
    plt.figure(figsize=(10, 5))
    plt.plot(rr_curve, label="round robin (dumb)")
    plt.plot(q_curve, label="q-learning (smart)")
    plt.xlabel("time step")
    plt.ylabel("cumulative hits")
    plt.title("Smart vs Dumb Scanning - cumulative hits over time")
    plt.legend()
    plt.tight_layout()
    plt.savefig("comparison_plot.png")
    plt.show()

    # plot 2 - just a simple bar chart, total hits
    plt.figure()
    plt.bar(["round robin", "q-learning"], [rr_hits, q_hits], color=["gray", "green"])
    plt.ylabel("total hits")
    plt.title("Total hits comparison")
    plt.tight_layout()
    plt.savefig("bar_chart.png")
    plt.show()
