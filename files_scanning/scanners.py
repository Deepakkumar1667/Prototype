"""
scanners.py - has our two scanning strategies:
1. round robin (dumb, old method) - just sweeps bands in order 0,1,2...
2. q-learning scanner (smart method) - learns which band to check next
   using a simple table based Q-learning approach

Also has a bonus function to check if a band looks periodic.
"""

import random
import numpy as np


def run_round_robin(env):
    num_bands = env.num_bands
    total_time = env.total_time

    current_band = 0
    hit_count = 0
    miss_count = 0
    hit_times = []
    hits_over_time = []  # cumulative hit count, useful for plotting later

    for t in range(total_time):
        band = current_band

        if env.is_on(band, t):
            hit_count += 1
            hit_times.append(t)
            # print("Hit! band:", band, "time:", t)   # uncomment to debug
        else:
            miss_count += 1

        hits_over_time.append(hit_count)

        current_band = (current_band + 1) % num_bands  # move to next band

    return hit_count, miss_count, hit_times, hits_over_time


def run_q_learning(env, alpha=0.1, gamma=0.9, epsilon=0.2):
    num_bands = env.num_bands
    total_time = env.total_time

    # q_table[state][action] -> state = last band we scanned, action = band to scan next
    q_table = np.zeros((num_bands, num_bands))

    state = 0
    hit_count = 0
    miss_count = 0
    hit_times = []
    hits_over_time = []

    for t in range(total_time):
        # epsilon greedy - sometimes explore, mostly exploit
        if random.random() < epsilon:
            action = random.randint(0, num_bands - 1)
        else:
            action = np.argmax(q_table[state])  # pick band with best known q value

        band = action

        if env.is_on(band, t):
            reward = 1
            hit_count += 1
            hit_times.append(t)
            # print("Hit! band:", band, "time:", t)
        else:
            reward = 0
            miss_count += 1

        hits_over_time.append(hit_count)

        # update q value using bellman eqn
        next_state = action
        best_next_q = np.max(q_table[next_state])
        old_q = q_table[state][action]
        q_table[state][action] = old_q + alpha * (reward + gamma * best_next_q - old_q)

        state = next_state

    return hit_count, miss_count, hit_times, hits_over_time, q_table


def detect_periodic(env, band):
    # bonus part - check gaps between ON times for a band and see if
    # they're roughly the same (periodic) or all over the place (random)
    on_times = []
    for t in range(env.total_time):
        if env.activity[band][t]:
            on_times.append(t)

    if len(on_times) < 3:
        print("band", band, "- not enough on-times to tell, skipping")
        return None

    gaps = []
    for i in range(1, len(on_times)):
        gaps.append(on_times[i] - on_times[i - 1])

    avg_gap = sum(gaps) / len(gaps)
    variance = sum((g - avg_gap) ** 2 for g in gaps) / len(gaps)

    if variance < 1.0:  # arbitrary cutoff, seemed to work fine when testing
        predicted_next = on_times[-1] + avg_gap
        print("band", band, "-> looks PERIODIC, avg gap =", round(avg_gap, 2),
              ", predicted next ON time =", round(predicted_next, 2))
        return predicted_next
    else:
        print("band", band, "-> looks RANDOM, gap variance =", round(variance, 2))
        return None
