"""
env.py - fake RF environment for the EW mini project
Basically we make some frequency bands, each one has an "emitter" that
turns on/off over time. Half of them are periodic (turn on at fixed
intervals) and half are random (turn on with some probability each step).
The scanner will try to catch these emitters ON.
"""

import random

NUM_BANDS = 12
TOTAL_TIME = 500


class RFEnv:
    def __init__(self, num_bands=NUM_BANDS, total_time=TOTAL_TIME):
        self.num_bands = num_bands
        self.total_time = total_time

        self.band_type = []
        self.period = []
        self.phase = []
        self.on_prob = []

        for b in range(num_bands):
            # just alternating periodic/random so we get a good mix
            if b % 2 == 0:
                self.band_type.append("periodic")
                self.period.append(random.randint(3, 10))
                self.phase.append(random.randint(0, 5))
                self.on_prob.append(0)  # not used for periodic
            else:
                self.band_type.append("random")
                self.period.append(0)
                self.phase.append(0)
                self.on_prob.append(random.uniform(0.1, 0.4))

        # precompute the whole ON/OFF timeline so it doesn't change every time
        # we peek at it (a scanner and a "cheat" viewer should see the same thing)
        self.activity = self.generate_activity()

    def generate_activity(self):
        # activity[band][t] = True/False, whether emitter is on at time t
        activity = []
        for b in range(self.num_bands):
            band_activity = []
            if self.band_type[b] == "periodic":
                p = self.period[b]
                ph = self.phase[b]
                for t in range(self.total_time):
                    if (t + ph) % p == 0:
                        band_activity.append(True)
                    else:
                        band_activity.append(False)
            else:
                prob = self.on_prob[b]
                for t in range(self.total_time):
                    # random emitter, flips on with some probability
                    if random.random() < prob:
                        band_activity.append(True)
                    else:
                        band_activity.append(False)
            activity.append(band_activity)
        return activity

    def is_on(self, band, t):
        # checking if band is active at time t
        if t >= self.total_time:
            return False
        return self.activity[band][t]


# quick sanity check if you just run this file directly
if __name__ == "__main__":
    env = RFEnv()
    print("band types:", env.band_type)
    print("periods (for periodic bands):", env.period)
    print("on probs (for random bands):", env.on_prob)
