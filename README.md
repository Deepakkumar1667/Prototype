# Prototype
# Smart Scan Strategy using Machine Learning

Mini project for Electronic Warfare course. The idea is to simulate a bunch
of frequency bands with emitters turning ON/OFF over time, and compare a
simple round-robin scanner (old method) against a Q-learning based scanner
(smart method) to see which one catches more emitters ON.

## Files

- `env.py` - simulates the RF environment (12 bands, some periodic emitters,
  some random emitters)
- `scanners.py` - has the round robin scanner, the Q-learning scanner, and
  a bonus function to detect if a band is periodic
- `main.py` - runs both scanners, prints results, plots comparison graphs

## How to run

```
pip install numpy matplotlib
python main.py
```

This will print hit/miss counts for both methods and save two plots:
- `comparison_plot.png` - cumulative hits over time (smart vs dumb)
- `bar_chart.png` - total hits comparison

## How it works (short version)

- Round robin just sweeps band 0,1,2...11,0,1... every time step, no logic.
- Q-learning keeps a table of Q-values for (last band checked, band to check
  next) and updates it using the Bellman equation after every scan. It uses
  epsilon-greedy so it mostly picks the best known band but sometimes
  explores a random one.
- Bonus part checks gaps between ON times for each band - if the gaps are
  consistent it guesses the band is periodic and predicts when it'll turn
  on next.

## Results

In my test run, Q-learning got more hits than round robin (121 vs 102 out
of 500 time steps) and correctly picked out which bands were periodic vs
random.

## Possible improvements (future work)

- Try different epsilon values / decay epsilon over time
- Track detection time per band instead of just globally
- Try a multi-armed bandit approach instead of full Q-learning and compare
